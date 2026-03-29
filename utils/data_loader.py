"""
Data loading utilities with caching for the Jardiner Simplement app.
"""

import json
import streamlit as st
from pathlib import Path
from typing import Dict, Any, List


@st.cache_data
def load_conseils() -> List[str]:
    """Load daily gardening tips."""
    with open("data/conseils.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["conseils_du_jour"]


@st.cache_data
def load_calendrier() -> Dict[str, Any]:
    """Load the 12-month gardening calendar."""
    with open("data/calendrier.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["calendrier"]


@st.cache_data
def load_legumes() -> Dict[str, Any]:
    """Load vegetable guide data."""
    with open("data/legumes.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["legumes"]


@st.cache_data
def load_associations() -> List[Dict[str, str]]:
    """Load companion planting associations."""
    with open("data/associations.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["associations"]


@st.cache_data
def load_nuisibles() -> List[Dict[str, Any]]:
    """Load pests and diseases data."""
    with open("data/nuisibles.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["nuisibles"]


@st.cache_data
def load_traitements() -> List[Dict[str, str]]:
    """Load natural treatment recipes."""
    with open("data/traitements.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["traitements_naturels"]


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
    
    # Sort by relevance score
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