"""
Authentication utilities for Jardiner Simplement.
Le stockage est délégué à utils/database.py.
"""

import re
import hashlib
import secrets
import streamlit as st
from typing import Dict, Optional, Any

from utils.database import (
    user_exists,
    get_user,
    insert_user,
    update_favorites as _db_update_favorites,
    update_garden as _db_update_garden,
)


# ─── Hachage ───────────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """Hache un mot de passe avec PBKDF2-HMAC-SHA256 (310 000 itérations)."""
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 310_000)
    return f"pbkdf2${salt}${dk.hex()}"


def verify_password(password: str, hashed: str) -> bool:
    """Vérifie un mot de passe (supporte PBKDF2 et l'ancien SHA-256)."""
    try:
        if hashed.startswith("pbkdf2$"):
            _, salt, stored = hashed.split("$", 2)
            dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 310_000)
            return secrets.compare_digest(dk.hex(), stored)
        else:
            # Ancien format SHA-256 : salt$hash
            salt, stored = hashed.split("$", 1)
            test = hashlib.sha256((password + salt).encode()).hexdigest()
            return secrets.compare_digest(test, stored)
    except (ValueError, IndexError):
        return False


# ─── Validation ────────────────────────────────────────────────────────────────

def sanitize_username(username: str) -> str:
    """Supprime tout caractère non autorisé (protection path traversal)."""
    return re.sub(r"[^a-zA-Z0-9_-]", "", username)


# ─── Gestion des utilisateurs ──────────────────────────────────────────────────

def create_user(username: str, password: str) -> bool:
    return insert_user(username, hash_password(password))


def authenticate_user(username: str, password: str) -> bool:
    user = get_user(username)
    if not user or not user.get("password_hash"):
        return False
    return verify_password(password, user["password_hash"])


def load_user_data(username: str) -> Optional[Dict[str, Any]]:
    """Charge les données d'un utilisateur (favoris, jardin, etc.)."""
    return get_user(username)


# ─── Session ───────────────────────────────────────────────────────────────────

def get_current_user() -> Optional[str]:
    return st.session_state.get("current_user")


def is_authenticated() -> bool:
    return "current_user" in st.session_state and st.session_state.current_user is not None


def login_user(username: str, password: str) -> bool:
    if authenticate_user(username, password):
        st.session_state.current_user = username
        user_data = load_user_data(username)
        if user_data:
            st.session_state.favorites = user_data.get(
                "favorites", {"legumes": [], "associations": [], "nuisibles": []}
            )
            st.session_state.mon_jardin = user_data.get("mon_jardin", [])
        return True
    return False


def logout_user():
    for key in ("current_user", "favorites", "mon_jardin", "selected_legume", "selected_nuisible"):
        st.session_state.pop(key, None)


def register_user(username: str, password: str, confirm_password: str) -> tuple[bool, str]:
    """Inscrit un nouvel utilisateur. Retourne (succès, message)."""
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
    return False, "Erreur lors de la création du compte."


# ─── Raccourcis de mise à jour ─────────────────────────────────────────────────

def update_user_favorites(username: str, favorites: Dict[str, list]) -> bool:
    return _db_update_favorites(username, favorites)


def update_user_garden(username: str, garden: list) -> bool:
    return _db_update_garden(username, garden)
