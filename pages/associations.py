"""
Companion planting associations page module.
"""

import streamlit as st
from utils.data_loader import load_associations
from utils.auth import is_authenticated, get_current_user, update_user_favorites


def render_associations():
    """Render the associations page."""
    st.title("🤝 Associations de Plantes")
    st.markdown(
        "<p style='text-align:center; color:#a5d6a7;'>"
        "Certaines plantes s'entraident, d'autres se nuisent. "
        "Le bon voisinage, c'est la base du jardin en bonne santé."
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    associations = load_associations()

    # Ensure favorites structure exists
    if "favorites" not in st.session_state:
        st.session_state.favorites = {"legumes": [], "associations": [], "nuisibles": []}

    for assoc in associations:
        effet = assoc["effet"]
        if "✅" in effet:
            couleur = "#1b4332"
            icon_color = "#69f0ae"
        else:
            couleur = "#3b1a1a"
            icon_color = "#ff5252"

        # Check if this association is in favorites
        is_favorite = assoc in st.session_state.favorites["associations"]
        
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(
                f'<div class="card" style="border-left: 4px solid {icon_color}; background: {couleur};">'
                f'<strong style="font-size:1.1rem">{assoc["plante1"]} + {assoc["plante2"]}</strong><br>'
                f'<span style="color:{icon_color}">{effet}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
        with col2:
            # Add to favorites button
            if st.button(
                f"{'⭐' if is_favorite else '☆'}",
                key=f"fav_assoc_{assoc['plante1']}_{assoc['plante2']}",
                help="Ajouter/retirer des favoris"
            ):
                if is_favorite:
                    st.session_state.favorites["associations"].remove(assoc)
                    st.info("Retiré des favoris")
                else:
                    st.session_state.favorites["associations"].append(assoc)
                    st.success("Ajouté aux favoris")
                # Save to user file if authenticated
                if is_authenticated():
                    update_user_favorites(get_current_user(), st.session_state.favorites)
                st.rerun()

    st.markdown("---")
    st.markdown("### 📌 Principes généraux")
    principes = [
        "🌿 **Les aromates** (basilic, persil, ciboulette) sont d'excellents compagnons pour la plupart des légumes.",
        "🌸 **Les fleurs** (capucines, soucis, œillets d'Inde) dans le potager attirent les insectes utiles et repoussent les nuisibles.",
        "🚫 **Le fenouil** est l'ennemi commun — plantez-le toujours seul, à l'écart.",
        "🔄 **La rotation** : ne replantez jamais la même famille au même endroit deux années de suite.",
        "🐝 **Les plantes à fleurs** dans et autour du potager attirent les pollinisateurs indispensables.",
        "💪 **Les légumineuses** (haricots, pois, fèves) enrichissent le sol en azote au profit de leurs voisins.",
    ]
    for p in principes:
        st.markdown(f'<div class="card-item">{p}</div>', unsafe_allow_html=True)