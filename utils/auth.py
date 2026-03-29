"""
Authentication utilities for Jardiner Simplement.
Simple file-based user management with password hashing.
"""

import json
import hashlib
import shutil
import streamlit as st
from pathlib import Path
from typing import Optional, Dict, Any
import secrets

USERS_DIR = Path("users")


def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with a salt."""
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${password_hash}"


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    try:
        salt, stored_hash = hashed.split("$")
        test_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return test_hash == stored_hash
    except (ValueError, IndexError):
        return False


def ensure_users_dir():
    """Ensure the users directory exists."""
    USERS_DIR.mkdir(exist_ok=True)


def user_file_path(username: str) -> Path:
    """Get the path to a user's data file."""
    return USERS_DIR / f"{username}.json"


def user_exists(username: str) -> bool:
    """Check if a user exists."""
    return user_file_path(username).exists()


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
    
    with open(user_file_path(username), "w", encoding="utf-8") as f:
        json.dump(user_data, f, indent=2, ensure_ascii=False)
    
    return True


def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate a user.
    Returns True if credentials are valid, False otherwise.
    """
    if not user_exists(username):
        return False
    
    user_path = user_file_path(username)
    backup_path = user_path.with_suffix('.json.backup')
    
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
        
        # If file is corrupted and no backup, delete it
        if user_path.exists():
            try:
                user_path.unlink(missing_ok=True)
                st.error("❌ Votre fichier de compte est corrompu et ne peut être récupéré. Veuillez recréer un compte.")
            except Exception:
                st.error(f"❌ Erreur lors du chargement du compte : {e}")
        else:
            st.error(f"❌ Erreur lors du chargement du compte : {e}")
        return False
    
    return verify_password(password, user_data["password_hash"])


def load_user_data(username: str) -> Optional[Dict[str, Any]]:
    """Load a user's data (favorites, garden, etc.)."""
    if not user_exists(username):
        return None
    
    user_path = user_file_path(username)
    backup_path = user_path.with_suffix('.json.backup')
    
    try:
        with open(user_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        # If file is corrupted and we have a backup, restore it
        if user_path.exists() and backup_path.exists():
            try:
                shutil.copy2(backup_path, user_path)
                st.warning("⚠️ Fichier utilisateur corrompu restauré depuis la sauvegarde.")
                with open(user_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        
        # If still failing or no backup, create fresh user data if file exists and is corrupted
        if user_path.exists():
            st.error(f"❌ Fichier de données corrompu. Un nouveau fichier a été créé.")
            fresh_data = {
                "username": username,
                "password_hash": "",
                "favorites": {"legumes": [], "associations": [], "nuisibles": []},
                "mon_jardin": []
            }
            try:
                with open(user_path, "w", encoding="utf-8") as f:
                    json.dump(fresh_data, f, indent=2, ensure_ascii=False)
                return fresh_data
            except Exception:
                return None
        return None


def save_user_data(username: str, user_data: Dict[str, Any]) -> bool:
    """Save a user's data to file."""
    try:
        with open(user_file_path(username), "w", encoding="utf-8") as f:
            json.dump(user_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde : {e}")
        return False


def get_current_user() -> Optional[str]:
    """Get the currently logged in username from session state."""
    return st.session_state.get("current_user")


def is_authenticated() -> bool:
    """Check if a user is currently authenticated."""
    return "current_user" in st.session_state and st.session_state.current_user is not None


def login_user(username: str, password: str) -> bool:
    """
    Attempt to log in a user.
    Sets session state if successful.
    """
    if authenticate_user(username, password):
        st.session_state.current_user = username
        # Load user preferences into session
        user_data = load_user_data(username)
        if user_data:
            st.session_state.favorites = user_data.get("favorites", {"legumes": [], "associations": [], "nuisibles": []})
            st.session_state.mon_jardin = user_data.get("mon_jardin", [])
        return True
    return False


def logout_user():
    """Log out the current user and clear session."""
    if "current_user" in st.session_state:
        del st.session_state.current_user
    # Clear user-specific session data
    if "favorites" in st.session_state:
        del st.session_state.favorites
    if "mon_jardin" in st.session_state:
        del st.session_state.mon_jardin
    if "selected_legume" in st.session_state:
        del st.session_state.selected_legume
    if "selected_nuisible" in st.session_state:
        del st.session_state.selected_nuisible


def register_user(username: str, password: str, confirm_password: str) -> tuple[bool, str]:
    """
    Register a new user.
    Returns (success, message).
    """
    if not username or not password:
        return False, "Nom d'utilisateur et mot de passe requis."
    
    if len(username) < 3:
        return False, "Le nom d'utilisateur doit faire au moins 3 caractères."
    
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