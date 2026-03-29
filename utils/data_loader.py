"""
Data loading utilities with caching for the Jardiner Simplement app.
"""

import json
import streamlit as st
from pathlib import Path
from typing import Dict, Any, List


def _load_json(path: str) -> Any:
    """Load and return a JSON file, raising a clear error on failure."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"❌ Fichier de données manquant : {path}")
        raise
    except json.JSONDecodeError as e:
        st.error(f"❌ Fichier de données corrompu ({path}) : {e}")
        raise


@st.cache_data
def load_conseils() -> List[str]:
    """Load daily gardening tips."""
    return _load_json("data/conseils.json")["conseils_du_jour"]


@st.cache_data
def load_calendrier() -> Dict[str, Any]:
    """Load the 12-month gardening calendar."""
    return _load_json("data/calendrier.json")["calendrier"]


@st.cache_data
def load_legumes() -> Dict[str, Any]:
    """Load vegetable guide data."""
    return _load_json("data/legumes.json")["legumes"]


@st.cache_data
def load_associations() -> List[Dict[str, str]]:
    """Load companion planting associations."""
    return _load_json("data/associations.json")["associations"]


@st.cache_data
def load_nuisibles() -> List[Dict[str, Any]]:
    """Load pests and diseases data."""
    return _load_json("data/nuisibles.json")["nuisibles"]


@st.cache_data
def load_traitements() -> List[Dict[str, str]]:
    """Load natural treatment recipes."""
    return _load_json("data/traitements.json")["traitements_naturels"]


def get_conseil_du_jour() -> str:
    """Get today's gardening tip based on the date."""
    from datetime import date
    conseils = load_conseils()
    today = date.today()
    day_of_year = today.timetuple().tm_yday
    return conseils[day_of_year % len(conseils)]


def get_mois_info(mois: int) -> Dict[str, Any]:
    """Get calendar info for a specific month (1-12)."""
    calendrier = load_calendrier()
    return calendrier[str(mois)]


def search_legumes(keyword: str) -> List[tuple]:
    """Search vegetables by keyword in name, description, or characteristics."""
    legumes = load_legumes()
    results = []
    keyword_lower = keyword.lower()

    for nom, data in legumes.items():
        score = 0
        if keyword_lower in nom.lower():
            score += 10
        if keyword_lower in data["description"].lower():
            score += 5
        if keyword_lower in data["semis"].lower():
            score += 3
        if keyword_lower in data["plantation"].lower():
            score += 3
        if keyword_lower in data["recolte"].lower():
            score += 3
        if keyword_lower in data["maladies"].lower():
            score += 2

        if score > 0:
            results.append((nom, data, score))

    results.sort(key=lambda x: x[2], reverse=True)
    return results


def search_associations(keyword: str) -> List[tuple]:
    """Search companion associations by plant name."""
    associations = load_associations()
    keyword_lower = keyword.lower()
    results = []

    for assoc in associations:
        score = 0
        if keyword_lower in assoc["plante1"].lower():
            score += 5
        if keyword_lower in assoc["plante2"].lower():
            score += 5
        if keyword_lower in assoc["effet"].lower():
            score += 2

        if score > 0:
            results.append((assoc, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in results]


def search_nuisibles(keyword: str) -> List[tuple]:
    """Search pests by name, description, or symptoms."""
    nuisibles = load_nuisibles()
    keyword_lower = keyword.lower()
    results = []

    for nuisible in nuisibles:
        score = 0
        if keyword_lower in nuisible["nom"].lower():
            score += 10
        if keyword_lower in nuisible["description"].lower():
            score += 5
        if keyword_lower in nuisible["degats"].lower():
            score += 3
        for solution in nuisible["solutions"]:
            if keyword_lower in solution.lower():
                score += 1

        if score > 0:
            results.append((nuisible, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in results]


def search_all(keyword: str) -> Dict[str, List[Any]]:
    """Search across all data categories."""
    return {
        "légumes": search_legumes(keyword),
        "associations": search_associations(keyword),
        "nuisibles": search_nuisibles(keyword)
    }
