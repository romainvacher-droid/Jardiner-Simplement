"""
Couche d'accès base de données pour Jardiner Simplement.

- Production (Heroku) : PostgreSQL via la variable d'environnement DATABASE_URL
- Développement local : SQLite (fichier jardiner.db créé automatiquement)
"""

import os
import json
import sqlite3
from contextlib import contextmanager
from datetime import date
from typing import Any, Dict, List, Optional

DATABASE_URL = os.environ.get("DATABASE_URL", "")
_SQLITE_PATH = "jardiner.db"


# ─── Sérialisation JSON ────────────────────────────────────────────────────────

class _DateEncoder(json.JSONEncoder):
    """Sérialise les objets date Python en chaîne ISO-8601."""
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


def _parse_garden_dates(garden: list) -> list:
    """Convertit les chaînes ISO en objets date dans les entrées du jardin."""
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


def _dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, cls=_DateEncoder)


# ─── Connexion ─────────────────────────────────────────────────────────────────

def _is_pg() -> bool:
    return bool(DATABASE_URL)


def _ph() -> str:
    """Placeholder de paramètre SQL : %s (PostgreSQL) ou ? (SQLite)."""
    return "%s" if _is_pg() else "?"


@contextmanager
def _conn():
    """Context manager : connexion DB avec commit ou rollback automatique."""
    if _is_pg():
        import psycopg2
        url = DATABASE_URL
        # Heroku génère des URLs postgres:// que psycopg2 n'accepte plus
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        conn = psycopg2.connect(url)
    else:
        conn = sqlite3.connect(_SQLITE_PATH)

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ─── Schéma ────────────────────────────────────────────────────────────────────

def init_db() -> None:
    """Crée la table users si elle n'existe pas. À appeler au démarrage."""
    with _conn() as conn:
        conn.cursor().execute("""
            CREATE TABLE IF NOT EXISTS users (
                username      VARCHAR(50) PRIMARY KEY,
                password_hash TEXT        NOT NULL,
                favorites     TEXT        NOT NULL
                              DEFAULT '{"legumes":[],"associations":[],"nuisibles":[]}',
                mon_jardin    TEXT        NOT NULL DEFAULT '[]'
            )
        """)


# ─── CRUD ──────────────────────────────────────────────────────────────────────

def user_exists(username: str) -> bool:
    ph = _ph()
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM users WHERE username = {ph}", (username,))
        return cur.fetchone() is not None


def get_user(username: str) -> Optional[Dict[str, Any]]:
    """Retourne le dict de l'utilisateur ou None si introuvable."""
    ph = _ph()
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute(
            f"SELECT username, password_hash, favorites, mon_jardin"
            f" FROM users WHERE username = {ph}",
            (username,),
        )
        row = cur.fetchone()
    if row is None:
        return None
    return {
        "username": row[0],
        "password_hash": row[1],
        "favorites": json.loads(row[2]),
        "mon_jardin": _parse_garden_dates(json.loads(row[3])),
    }


def insert_user(username: str, password_hash: str) -> bool:
    """Insère un nouvel utilisateur. Retourne False si le nom est déjà pris."""
    ph = _ph()
    try:
        with _conn() as conn:
            conn.cursor().execute(
                f"INSERT INTO users (username, password_hash) VALUES ({ph}, {ph})",
                (username, password_hash),
            )
        return True
    except Exception:
        return False


def update_favorites(username: str, favorites: Dict[str, list]) -> bool:
    ph = _ph()
    try:
        with _conn() as conn:
            conn.cursor().execute(
                f"UPDATE users SET favorites = {ph} WHERE username = {ph}",
                (_dumps(favorites), username),
            )
        return True
    except Exception:
        return False


def update_garden(username: str, garden: List[dict]) -> bool:
    ph = _ph()
    try:
        with _conn() as conn:
            conn.cursor().execute(
                f"UPDATE users SET mon_jardin = {ph} WHERE username = {ph}",
                (_dumps(garden), username),
            )
        return True
    except Exception:
        return False
