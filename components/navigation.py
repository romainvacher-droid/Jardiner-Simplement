"""
Navigation component for the Jardiner Simplement app.
"""

import streamlit as st
from utils.data_loader import load_conseils, get_conseil_du_jour
from utils.auth import is_authenticated, get_current_user, logout_user
from datetime import date


def render_navigation():
    """Render the top navigation bar with search and page links."""
    
    # Initialize session state for search if not exists
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
    
    # Get today's tip for the search placeholder
    conseil = get_conseil_du_jour()
    
    # Search bar
    col_search, col_clear = st.columns([4, 1])
    with col_search:
        search_query = st.text_input(
            "🔍 Rechercher (légumes, mois, problèmes, solutions...)",
            value=st.session_state.search_query,
            placeholder="Ex: tomate, mildiou, avril...",
            key="search_input",
            help="Recherchez des légumes, des tâches mensuelles, des nuisibles ou des traitements"
        )
        st.session_state.search_query = search_query
    
    with col_clear:
        if st.button("🗑️ Effacer", key="clear_search", use_container_width=True):
            st.session_state.search_query = ""
            st.rerun()
    
    # Navigation buttons
    st.markdown("---")
    
    pages = [
        ("🏠 Accueil", "accueil"),
        ("📅 Calendrier", "calendrier"),
        ("🥕 Légumes", "legumes"),
        ("🤝 Associations", "associations"),
        ("🐛 Nuisibles", "nuisibles"),
        ("🌿 Traitements", "traitements"),
        ("📖 Mes Favoris", "favoris"),
        ("🌱 Mon Jardin", "mon_jardin"),
        ("🔧 Outils", "outils"),
    ]
    
    # Create columns for navigation buttons
    cols = st.columns(len(pages))
    for col, (label, page_key) in zip(cols, pages):
        with col:
            if st.button(label, key=f"nav_{page_key}", use_container_width=True):
                st.session_state.page = page_key
                st.rerun()
    
    # User authentication section
    st.markdown("---")
    col_auth1, col_auth2 = st.columns([3, 2])
    with col_auth1:
        if is_authenticated():
            st.markdown(f"**👤 Connecté :** {get_current_user()}")
        else:
            st.markdown("**🔐 Non connecté**")
    with col_auth2:
        if is_authenticated():
            if st.button("🚪 Déconnexion", key="nav_logout", use_container_width=True):
                logout_user()
                st.rerun()
        else:
            if st.button("🔑 Connexion", key="nav_login", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
    
    st.markdown("---")
    
    # Show search results if there's a query
    if st.session_state.search_query.strip():
        render_search_results(st.session_state.search_query)


def render_search_results(query: str):
    """Display search results with highlighting."""
    from utils.data_loader import search_all
    
    st.markdown(f"### 🔍 Résultats pour : **'{query}'**")
    
    results = search_all(query)
    
    has_results = any([
        results["légumes"],
        results["associations"],
        results["nuisibles"]
    ])
    
    if not has_results:
        st.info(f"Aucun résultat trouvé pour '{query}'. Essayez avec d'autres mots-clés.")
        return
    
    # Display vegetable results
    if results["légumes"]:
        st.markdown(f"#### 🥕 Légumes ({len(results['légumes'])})")
        for nom, data, score in results["légumes"][:5]:
            with st.expander(f"{data['emoji']} **{nom}** (pertinence: {score})"):
                st.markdown(f"**Description :** {data['description'][:200]}...")
                st.markdown(f"**Semis :** {data['semis']}")
                st.markdown(f"**Plantation :** {data['plantation']}")
                if st.button(f"Voir {nom} en détail", key=f"search_legume_{nom}"):
                    st.session_state.selected_legume = nom
                    st.session_state.page = "legumes"
                    st.rerun()
    
    # Display association results
    if results["associations"]:
        st.markdown(f"#### 🤝 Associations ({len(results['associations'])})")
        for assoc in results["associations"][:5]:
            with st.expander(f"{assoc['plante1']} + {assoc['plante2']}"):
                st.markdown(f"**Effet :** {assoc['effet']}")
    
    # Display pest results
    if results["nuisibles"]:
        st.markdown(f"#### 🐛 Nuisibles ({len(results['nuisibles'])})")
        for nuisible in results["nuisibles"][:5]:
            with st.expander(f"{nuisible['emoji']} **{nuisible['nom']}**"):
                st.markdown(f"**Description :** {nuisible['description'][:150]}...")
                if st.button(f"Voir {nuisible['nom']} en détail", key=f"search_nuisible_{nuisible['nom']}"):
                    st.session_state.selected_nuisible = nuisible['nom']
                    st.session_state.page = "nuisibles"
                    st.rerun()
    
    # Show more link if there are more than 5 results in any category
    if (len(results["légumes"]) > 5 or 
        len(results["associations"]) > 5 or 
        len(results["nuisibles"]) > 5):
        st.markdown("---")
        st.info("Les résultats sont limités à 5 par catégorie. Utilisez les pages dédiées pour voir plus de résultats.")


def render_footer():
    """Render the footer with credits."""
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #a5d6a7; font-size: 0.9rem;'>"
        "🌱 <strong>Jardiner Simplement</strong> — "
        "Conseils jardinage naturels — "
        "Développé avec Streamlit"
        "</div>",
        unsafe_allow_html=True
    )