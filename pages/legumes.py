"""
Vegetables guide page module for Jardiner Simplement.
"""

import streamlit as st
from utils.data_loader import load_legumes
from utils.auth import is_authenticated, get_current_user, update_user_favorites


def render_legumes():
    """Render the vegetables guide page."""
    st.title("🥕 Guide des Légumes")
    st.markdown("<p style='text-align:center; color:#a5d6a7;'>Tout savoir pour cultiver vos légumes avec succès.</p>", unsafe_allow_html=True)

    legumes = load_legumes()
    
    # Check if a specific legume is selected from search
    selected_legume = st.session_state.get("selected_legume", None)
    
    if selected_legume and selected_legume in legumes:
        # Show detailed view of selected legume
        l = legumes[selected_legume]
        st.markdown(f"## {l['emoji']} {selected_legume}")
        st.markdown(f'<div class="card">{l["description"]}</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📆 Calendrier cultural")
            st.markdown(f'<div class="card-item">🌱 <strong>Semis :</strong> {l["semis"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-item">🪴 <strong>Plantation :</strong> {l["plantation"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-item">🧺 <strong>Récolte :</strong> {l["recolte"]}</div>', unsafe_allow_html=True)

            st.markdown("#### 🌍 Conditions")
            st.markdown(f'<div class="card-item">☀️ <strong>Exposition :</strong> {l["exposition"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-item">💧 <strong>Arrosage :</strong> {l["arrosage"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-item">📏 <strong>Espacement :</strong> {l["espacement"]}</div>', unsafe_allow_html=True)

        with col2:
            st.markdown("#### 🤝 Associations")
            st.markdown("**Bons voisins :**")
            for a in l["associations_positives"]:
                st.markdown(f'<div class="card-item"><span class="tag-positif">✅</span> {a}</div>', unsafe_allow_html=True)
            st.markdown("**À éviter :**")
            for a in l["associations_negatives"]:
                st.markdown(f'<div class="card-item"><span class="tag-negatif">❌</span> {a}</div>', unsafe_allow_html=True)

            st.markdown("#### ⚠️ Maladies fréquentes")
            st.markdown(f'<div class="card-item">🔴 {l["maladies"]}</div>', unsafe_allow_html=True)

        st.markdown("#### 💡 Conseil expert")
        st.markdown(f'<div class="conseil-box">🌿 {l["conseil"]}</div>', unsafe_allow_html=True)
        
        if st.button("⬅️ Retour à la liste"):
            st.session_state.selected_legume = None
            st.rerun()
    else:
        # Show list of all vegetables
        st.markdown("### Tous les légumes")
        
        # Ensure favorites structure exists
        if "favorites" not in st.session_state:
            st.session_state.favorites = {"legumes": [], "associations": [], "nuisibles": []}
        
        # Create a grid of vegetable cards
        for i, (nom, data) in enumerate(legumes.items()):
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.markdown(f'<div style="font-size:3rem; text-align:center;">{data["emoji"]}</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f"#### {nom}")
                    st.markdown(f'<div style="color:#a5d6a7; font-size:0.9rem;">{data["description"][:100]}...</div>', unsafe_allow_html=True)
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button(f"Voir {nom}", key=f"view_{nom}"):
                            st.session_state.selected_legume = nom
                            st.rerun()
                    with col_btn2:
                        # Add to favorites button
                        is_favorite = nom in st.session_state.favorites["legumes"]
                        if st.button(f"{'⭐' if is_favorite else '☆'} Ajouter aux favoris", key=f"fav_{nom}"):
                            if is_favorite:
                                st.session_state.favorites["legumes"].remove(nom)
                                st.info(f"{nom} retiré des favoris.")
                            else:
                                st.session_state.favorites["legumes"].append(nom)
                                st.success(f"{nom} ajouté aux favoris !")
                            # Save to user file if authenticated
                            if is_authenticated():
                                update_user_favorites(get_current_user(), st.session_state.favorites)
                            st.rerun()
                
                st.markdown("---")