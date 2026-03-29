#!/usr/bin/env python3
"""
🌱 Jardiner Simplement — Site web de conseils jardinage
Lancez avec : streamlit run app_streamlit.py
"""

import streamlit as st
from datetime import date

# Import components and pages
from components.navigation import render_navigation, render_footer
from pages.accueil import render_accueil
from pages.calendrier import render_calendrier
from pages.legumes import render_legumes
from pages.associations import render_associations
from pages.nuisibles import render_nuisibles
from pages.traitements import render_traitements
from pages.favoris import render_favoris
from pages.mon_jardin import render_mon_jardin
from pages.outils import render_outils
from pages.login import render_login
from utils.auth import (
    is_authenticated,
    get_current_user,
    login_user,
    logout_user,
    update_user_favorites,
    update_user_garden,
    load_user_data
)

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Jardiner Simplement",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS ET STYLE
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* Cacher barre d'outils Streamlit */
    header { display: none !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }

    /* Fond général */
    .stApp { background-color: #0d1f0d; color: #f0f0f0; }

    /* Titres */
    h1 { color: #4caf50 !important; text-align: center; margin-bottom: 0.5rem; }
    h2 { color: #81c784 !important; margin-top: 1rem; margin-bottom: 0.5rem; }
    h3 { color: #a5d6a7 !important; margin-top: 0.8rem; margin-bottom: 0.4rem; }
    h4 { color: #c8e6c9 !important; margin-top: 0.6rem; }

    /* Cartes */
    .card {
        background: #1a3a1a;
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #2e5c2e;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .card-item {
        background: #2e5c2e;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 6px 0;
        border-left: 4px solid #4caf50;
        box-shadow: 0 1px 4px rgba(0,0,0,0.2);
    }
    .conseil-box {
        background: linear-gradient(135deg, #1a3a1a, #2e5c2e);
        border-radius: 12px;
        padding: 18px;
        border-left: 4px solid #8bc34a;
        font-style: italic;
        font-size: 1.05rem;
        margin: 12px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .tag-positif { color: #69f0ae; font-weight: bold; }
    .tag-negatif { color: #ff5252; font-weight: bold; }
    .label { color: #a5d6a7; font-size: 0.9rem; }

    /* Boutons navigation */
    .stButton>button {
        background: linear-gradient(135deg, #2e7d32, #4caf50);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 0.95rem;
        font-weight: bold;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        opacity: 0.85;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .stButton>button:active {
        transform: translateY(0);
    }

    /* Séparateur */
    hr { border-color: #2e5c2e !important; margin: 1.5rem 0; }

    /* Conteneur principal */
    .block-container { padding-top: 1rem !important; }

    /* Amélioration des selects et inputs */
    .stSelectbox, .stTextInput, .stNumberInput, .stDateInput {
        background-color: #1a3a1a;
        border-radius: 8px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #1a3a1a !important;
        border-radius: 10px !important;
        color: #a5d6a7 !important;
    }
    .streamlit-expanderContent {
        background: #0d1f0d !important;
        border-radius: 0 0 10px 10px !important;
    }

    /* Progress bar */
    .stProgress > div > div {
        background-color: #4caf50 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #1a3a1a;
        padding: 8px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #a5d6a7;
        border-radius: 8px;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background: #2e5c2e !important;
        color: #4caf50 !important;
    }

    /* Alertes */
    .stAlert {
        border-radius: 10px !important;
        border: none !important;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: #1a3a1a;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #2e5c2e;
    }
    [data-testid="stMetricLabel"] {
        color: #a5d6a7 !important;
    }
    [data-testid="stMetricValue"] {
        color: #4caf50 !important;
        font-size: 1.8rem !important;
    }

    /* Mobile */
    @media (max-width: 768px) {
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.1rem !important; }
        .card { padding: 14px !important; }
        .stButton>button { font-size: 0.85rem !important; padding: 8px 6px !important; }
        .conseil-box { font-size: 0.95rem !important; padding: 12px !important; }
        
        /* Stack columns on mobile */
        .stColumns {
            flex-direction: column !important;
        }
    }

    /* Animations douces */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .card, .card-item, .conseil-box {
        animation: fadeIn 0.3s ease-out;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #1a3a1a;
    }
    ::-webkit-scrollbar-thumb {
        background: #2e5c2e;
        border-radius: 5px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #3d6b3d;
    }
}
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# INITIALISATION SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────

# Initialize page if not exists
if "page" not in st.session_state:
    st.session_state.page = "accueil"

# Check authentication requirement for protected pages
protected_pages = ["favoris", "mon_jardin"]
if st.session_state.page in protected_pages and not is_authenticated():
    st.session_state.page = "login"
    st.rerun()

# Initialize favorites if not exists (will be overwritten if user logs in)
if "favorites" not in st.session_state:
    st.session_state.favorites = {
        "legumes": [],
        "associations": [],
        "nuisibles": []
    }

# Initialize garden if not exists (will be overwritten if user logs in)
if "mon_jardin" not in st.session_state:
    st.session_state.mon_jardin = []

# If user is authenticated, load their data
if is_authenticated():
    user_data = load_user_data(st.session_state.current_user)
    if user_data:
        st.session_state.favorites = user_data.get("favorites", st.session_state.favorites)
        st.session_state.mon_jardin = user_data.get("mon_jardin", st.session_state.mon_jardin)
    else:
        # File missing or corrupted, log out user
        st.warning("⚠️ Votre fichier de données utilisateur est corrompu ou manquant. Vous avez été déconnecté.")
        logout_user()
        st.session_state.page = "login"
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────

render_navigation()

# ─────────────────────────────────────────────────────────────────────────────
# ROUTAGE DES PAGES
# ─────────────────────────────────────────────────────────────────────────────

page = st.session_state.page

try:
    if page == "accueil":
        render_accueil()
    elif page == "calendrier":
        render_calendrier()
    elif page == "legumes":
        render_legumes()
    elif page == "associations":
        render_associations()
    elif page == "nuisibles":
        render_nuisibles()
    elif page == "traitements":
        render_traitements()
    elif page == "favoris":
        render_favoris()
    elif page == "mon_jardin":
        render_mon_jardin()
    elif page == "outils":
        render_outils()
    elif page == "login":
        render_login()
    else:
        # Default to home page
        render_accueil()
        st.session_state.page = "accueil"
        st.rerun()

except Exception as e:
    st.error(f"Une erreur est survenue : {str(e)}")
    st.exception(e)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────

render_footer()