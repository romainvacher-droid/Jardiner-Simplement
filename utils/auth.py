"""
Authentication utilities for Jardiner Simplement.
Simple file-based user management with password hashing.
"""

import json
import hashlib
import re
import os
import shutil
import tempfile
import streamlit as st
from datetime import date
from pathlib import Path
from typing import Optional, Dict, Any
import secrets

USERS_DIR = Path("users")


# ─── JSON helpers ──────────────────────────────────────────────────────────────

class _DateEncoder(json.JSONEncoder):
    """JSON encoder that serialises date objects as ISO-8601 strings."""
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


def _parse_garden_dates(garden: list) -> list:
    """Convert ISO date strings back to date objects in garden entries."""
    result = []
    for plant in garden:
        entry = dict(plant)
        if isinstance(entry.get("date_plantation"), str):
            try:
                entry["date_plantation"] = date.fromisoformat(entry["date_plantation"])
            except ValueError:
                pass
        result.append(entry)
    return result


# ─── Password hashing ──────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """Hash a password using PBKDF2-HMAC-SHA256 with a random salt."""
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 310_000)
    return f"pbkdf2${salt}${dk.hex()}"


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash (supports PBKDF2 and legacy SHA-256)."""
    try:
        if hashed.startswith("pbkdf2$"):
            _, salt, stored = hashed.split("$", 2)
            dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 310_000)
            return secrets.compare_digest(dk.hex(), stored)
        else:
            # Legacy SHA-256 format: salt$hash
            salt, stored = hashed.split("$", 1)
            test = hashlib.sha256((password + salt).encode()).hexdigest()
            return secrets.compare_digest(test, stored)
    except (ValueError, IndexError):
        return False


# ─── Path helpers ──────────────────────────────────────────────────────────────

def sanitize_username(username: str) -> str:
    """Strip characters that could cause path traversal."""
    return re.sub(r"[^a-zA-Z0-9_-]", "", username)


def ensure_users_dir():
    """Ensure the users directory exists."""
    USERS_DIR.mkdir(exist_ok=True)


def user_file_path(username: str) -> Path:
    """Get the path to a user's data file (raises ValueError for invalid names)."""
    safe = sanitize_username(username)
    if not safe:
        raise ValueError("Nom d'utilisateur invalide.")
    return USERS_DIR / f"{safe}.json"


def user_exists(username: str) -> bool:
    """Check if a user exists."""
    try:
        return user_file_path(username).exists()
    except ValueError:
        return False


# ─── User CRUD ─────────────────────────────────────────────────────────────────

def create_user(username: str, password: str) -> bool:
    """
    Create a new user with hashed password and empty preferences.
    Returns True if successful, False if user already exists.
    """
    if user_exists(username):
        return False

    ensure_users_dir()

    user_data = {
        "username": username,
        "password_hash": hash_password(password),
        "favorites": {
            "legumes": [],
            "associations": [],
            "nuisibles": []
        },
        "mon_jardin": []
    }

    return _atomic_write(user_file_path(username), user_data)


def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate a user.
    Returns True if credentials are valid, False otherwise.
    """
    if not user_exists(username):
        return False

    user_path = user_file_path(username)
    backup_path = user_path.with_suffix(".json.backup")

    try:
        with open(user_path, "r", encoding="utf-8") as f:
            user_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        # Try to restore from backup
        if user_path.exists() and backup_path.exists():
            try:
                shutil.copy2(backup_path, user_path)
                st.warning("⚠️ Fichier utilisateur corrompu restauré depuis la sauvegarde. Essayez de vous reconnecter.")
                return False
            except Exception:
                pass

        # Cannot recover — delete the corrupted file (do NOT silently unlock the account)
        try:
            user_path.unlink(missing_ok=True)
            st.error("❌ Votre fichier de compte est corrompu et ne peut être récupéré. Veuillez recréer un compte.")
        except Exception:
            st.error(f"❌ Erreur lors du chargement du compte : {e}")
        return False

    password_hash = user_data.get("password_hash", "")
    if not password_hash:
        return False

    return verify_password(password, password_hash)


def load_user_data(username: str) -> Optional[Dict[str, Any]]:
    """Load a user's data (favorites, garden, etc.) with date deserialisation."""
    if not user_exists(username):
        return None

    user_path = user_file_path(username)
    backup_path = user_path.with_suffix(".json.backup")

    try:
        with open(user_path, "r", encoding="utf-8") as f:
            user_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Attempt backup restore
        if user_path.exists() and backup_path.exists():
            try:
                shutil.copy2(backup_path, user_path)
                st.warning("⚠️ Fichier utilisateur corrompu restauré depuis la sauvegarde.")
                with open(user_path, "r", encoding="utf-8") as f:
                    user_data = json.load(f)
            except Exception:
                return None
        else:
            return None

    # Convert date strings in mon_jardin back to date objects
    if "mon_jardin" in user_data:
        user_data["mon_jardin"] = _parse_garden_dates(user_data["mon_jardin"])

    return user_data


def save_user_data(username: str, user_data: Dict[str, Any]) -> bool:
    """Save a user's data to file atomically."""
    try:
        return _atomic_write(user_file_path(username), user_data)
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde : {e}")
        return False


def _atomic_write(target: Path, data: Dict[str, Any]) -> bool:
    """Write data to a temp file then rename — prevents partial writes."""
    try:
        fd, tmp_path = tempfile.mkstemp(dir=target.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False, cls=_DateEncoder)
            os.replace(tmp_path, target)
            return True
        except Exception:
            os.unlink(tmp_path)
            raise
    except Exception as e:
        st.error(f"Erreur lors de l'écriture : {e}")
        return False


# ─── Session helpers ───────────────────────────────────────────────────────────

def get_current_user() -> Optional[str]:
    """Get the currently logged in username from session state."""
    return st.session_state.get("current_user")


def is_authenticated() -> bool:
    """Check if a user is currently authenticated."""
    return "current_user" in st.session_state and st.session_state.current_user is not None


def login_user(username: str, password: str) -> bool:
    """Attempt to log in a user. Sets session state if successful."""
    if authenticate_user(username, password):
        st.session_state.current_user = username
        user_data = load_user_data(username)
        if user_data:
            st.session_state.favorites = user_data.get(
                "favorites", {"legumes": [], "associations": [], "nuisibles": []}
            )
            # load_user_data already converts date strings to date objects
            st.session_state.mon_jardin = user_data.get("mon_jardin", [])
        return True
    return False


def logout_user():
    """Log out the current user and clear session."""
    for key in ("current_user", "favorites", "mon_jardin", "selected_legume", "selected_nuisible"):
        st.session_state.pop(key, None)


def register_user(username: str, password: str, confirm_password: str) -> tuple[bool, str]:
    """Register a new user. Returns (success, message)."""
    if not username or not password:
        return False, "Nom d'utilisateur et mot de passe requis."

    if len(username) < 3:
        return False, "Le nom d'utilisateur doit faire au moins 3 caractères."

    if not re.match(r"^[a-zA-Z0-9_-]+$", username):
        return False, "Le nom d'utilisateur ne peut contenir que des lettres, chiffres, - et _."

    if len(password) < 6:
        return False, "Le mot de passe doit faire au moins 6 caractères."

    if password != confirm_password:
        return False, "Les mots de passe ne correspondent pas."

    if user_exists(username):
        return False, "Ce nom d'utilisateur existe déjà."

    if create_user(username, password):
        return True, "Compte créé avec succès ! Vous pouvez maintenant vous connecter."
    else:
        return False, "Erreur lors de la création du compte."


# ─── Data update shortcuts ─────────────────────────────────────────────────────

def update_user_favorites(username: str, favorites: Dict[str, list]) -> bool:
    """Update a user's favorites."""
    user_data = load_user_data(username)
    if user_data:
        user_data["favorites"] = favorites
        return save_user_data(username, user_data)
    return False


def update_user_garden(username: str, garden: list) -> bool:
    """Update a user's garden data."""
    user_data = load_user_data(username)
    if user_data:
        user_data["mon_jardin"] = garden
        return save_user_data(username, user_data)
    return False
