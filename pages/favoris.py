"""
Favorites page module for Jardiner Simplement.
"""

import streamlit as st
from utils.data_loader import load_legumes, load_associations, load_nuisibles
from utils.auth import is_authenticated, get_current_user, update_user_favorites


def render_favoris():
    """Render the favorites page."""
    st.title("📖 Mes Favoris")
    st.markdown(
        "<p style='text-align:center; color:#a5d6a7;'>"
        "Vos légumes, associations et solutions préférés en un clic."
        "</p>",
        unsafe_allow_html=True
    )

    # Check authentication
    if not is_authenticated():
        st.warning("🔐 Veuillez vous connecter pour accéder à vos favoris.")
        if st.button("Se connecter", type="primary"):
            st.session_state.page = "login"
            st.rerun()
        return

    # Ensure user data is loaded
    if "favorites" not in st.session_state:
        st.session_state.favorites = {
            "legumes": [],
            "associations": [],
            "nuisibles": []
        }

    # Tabs for different favorite types
    tab1, tab2, tab3 = st.tabs(["🥕 Légumes favoris", "🤝 Associations favorites", "🐛 Nuisibles favoris"])

    legumes = load_legumes()
    associations = load_associations()
    nuisibles = load_nuisibles()

    def save_favorites():
        """Save favorites to user file."""
        if is_authenticated():
            update_user_favorites(get_current_user(), st.session_state.favorites)

    with tab1:
        st.markdown("### Vos légumes préférés")
        if st.session_state.favorites["legumes"]:
            for legume_nom in st.session_state.favorites["legumes"]:
                if legume_nom in legumes:
                    data = legumes[legume_nom]
                    with st.container():
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            st.markdown(f'<div style="font-size:2.5rem; text-align:center;">{data["emoji"]}</div>', unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"#### {legume_nom}")
                            st.markdown(f'<div style="color:#a5d6a7; font-size:0.9rem;">{data["description"][:150]}...</div>', unsafe_allow_html=True)
                            if st.button(f"🗑️ Supprimer", key=f"remove_legume_{legume_nom}"):
                                st.session_state.favorites["legumes"].remove(legume_nom)
                                save_favorites()
                                st.rerun()
                        st.markdown("---")
        else:
            st.info("Aucun légume favori pour le moment. Ajoutez-en depuis la page Légumes !")

    with tab2:
        st.markdown("### Vos associations préférées")
        if st.session_state.favorites["associations"]:
            for assoc in st.session_state.favorites["associations"]:
                # Find the association in the full list
                found = None
                for a in associations:
                    if a["plante1"] == assoc["plante1"] and a["plante2"] == assoc["plante2"]:
                        found = a
                        break
                
                if found:
                    with st.container():
                        effet = found["effet"]
                        icon_color = "#69f0ae" if "✅" in effet else "#ff5252"
                        st.markdown(
                            f'<div class="card" style="border-left: 4px solid {icon_color};">'
                            f'<strong>{found["plante1"]} + {found["plante2"]}</strong><br>'
                            f'<span style="color:{icon_color}">{effet}</span><br>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                        if st.button(f"🗑️ Supprimer", key=f"remove_assoc_{found['plante1']}_{found['plante2']}"):
                            st.session_state.favorites["associations"].remove(found)
                            save_favorites()
                            st.rerun()
                        st.markdown("---")
        else:
            st.info("Aucune association favorite pour le moment.")

    with tab3:
        st.markdown("### Vos nuisibles favoris")
        if st.session_state.favorites["nuisibles"]:
            for nuisible_nom in st.session_state.favorites["nuisibles"]:
                found = None
                for n in nuisibles:
                    if n["nom"] == nuisible_nom:
                        found = n
                        break
                
                if found:
                    with st.container():
                        st.markdown(f"#### {found['emoji']} {found['nom']}")
                        st.markdown(f"**Description :** {found['description'][:150]}...")
                        if st.button(f"🗑️ Supprimer", key=f"remove_nuisible_{nuisible_nom}"):
                            st.session_state.favorites["nuisibles"].remove(nuisible_nom)
                            save_favorites()
                            st.rerun()
                        st.markdown("---")
        else:
            st.info("Aucun nuisible favori pour le moment.")

    # Clear all button
    st.markdown("---")
    if st.button("🗑️ Tout effacer les favoris", type="secondary"):
        if st.session_state.favorites["legumes"] or st.session_state.favorites["associations"] or st.session_state.favorites["nuisibles"]:
            st.session_state.favorites = {"legumes": [], "associations": [], "nuisibles": []}
            save_favorites()
            st.success("Tous les favoris ont été effacés !")
            st.rerun()