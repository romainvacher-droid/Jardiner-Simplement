"""
Pests and diseases page module for Jardiner Simplement.
"""

import streamlit as st
from utils.data_loader import load_nuisibles
from utils.auth import is_authenticated, get_current_user, update_user_favorites


def render_nuisibles():
    """Render the pests page."""
    st.title("🐛 Nuisibles & Maladies")
    st.markdown(
        "<p style='text-align:center; color:#a5d6a7;'>"
        "Identifier les problèmes et y répondre sans chimie."
        "</p>",
        unsafe_allow_html=True
    )

    nuisibles = load_nuisibles()
    
    # Check if a specific pest is selected from search
    selected_nuisible = st.session_state.get("selected_nuisible", None)

    # Ensure favorites structure exists
    if "favorites" not in st.session_state:
        st.session_state.favorites = {"legumes": [], "associations": [], "nuisibles": []}

    for n in nuisibles:
        # Check if this pest is in favorites
        is_favorite = n["nom"] in st.session_state.favorites["nuisibles"]
        
        # If this pest is selected, show detailed view
        if selected_nuisible and selected_nuisible == n["nom"]:
            st.markdown(f"## {n['emoji']} {n['nom']}")
            st.markdown(f"**Description :** {n['description']}")
            st.markdown(f"**Dégâts :** <em>{n['degats']}</em>", unsafe_allow_html=True)
            st.markdown("**Solutions naturelles :**")
            for s in n["solutions"]:
                st.markdown(f'<div class="card-item">✅ {s}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("⬅️ Retour à la liste"):
                    st.session_state.selected_nuisible = None
                    st.rerun()
            with col2:
                # Favorite button in detail view
                if st.button(
                    f"{'⭐ Retirer des favoris' if is_favorite else '☆ Ajouter aux favoris'}",
                    key=f"detail_fav_{n['nom']}"
                ):
                    if is_favorite:
                        st.session_state.favorites["nuisibles"].remove(n["nom"])
                        st.info("Retiré des favoris")
                    else:
                        st.session_state.favorites["nuisibles"].append(n["nom"])
                        st.success("Ajouté aux favoris")
                    if is_authenticated():
                        update_user_favorites(get_current_user(), st.session_state.favorites)
                    st.rerun()
            
            st.markdown("---")
        else:
            # Show compact view with favorite button
            with st.container():
                col1, col2 = st.columns([5, 1])
                with col1:
                    with st.expander(f"{n['emoji']} **{n['nom']}**"):
                        st.markdown(f"**Description :** {n['description']}")
                        st.markdown(f"**Dégâts :** _{n['degats']}_")
                        st.markdown("**Solutions naturelles :**")
                        for s in n["solutions"]:
                            st.markdown(f'<div class="card-item">✅ {s}</div>', unsafe_allow_html=True)
                        if st.button(f"Voir en détail", key=f"view_detail_{n['nom']}"):
                            st.session_state.selected_nuisible = n['nom']
                            st.rerun()
                with col2:
                    # Add to favorites button
                    if st.button(
                        f"{'⭐' if is_favorite else '☆'}",
                        key=f"fav_nuis_{n['nom']}",
                        help="Ajouter/retirer des favoris"
                    ):
                        if is_favorite:
                            st.session_state.favorites["nuisibles"].remove(n["nom"])
                            st.info("Retiré des favoris")
                        else:
                            st.session_state.favorites["nuisibles"].append(n["nom"])
                            st.success("Ajouté aux favoris")
                        if is_authenticated():
                            update_user_favorites(get_current_user(), st.session_state.favorites)
                        st.rerun()