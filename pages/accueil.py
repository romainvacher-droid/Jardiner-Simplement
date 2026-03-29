"""
Home page module for Jardiner Simplement.
"""

import streamlit as st
from utils.data_loader import get_conseil_du_jour, load_calendrier, get_mois_info
from datetime import date


def render_accueil():
    """Render the home page."""
    st.title("🌱 Jardiner Simplement")
    st.markdown(
        "<p style='text-align:center; color:#a5d6a7; font-size:1.1rem;'>"
        "Astuces naturelles et conseils pratiques pour un jardin qui vous ressemble."
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Conseil du jour
    today = date.today()
    conseil = get_conseil_du_jour()

    st.markdown("### 💡 Conseil du jour")
    st.markdown(f'<div class="conseil-box">🌿 {conseil}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Saison en cours
    mois = today.month
    info_mois = get_mois_info(mois)

    st.markdown(f"### 🗓️ En ce mois de {info_mois['nom']}")
    st.markdown(f'<div class="card"><em>{info_mois["conseil"]}</em></div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        if info_mois["semis"]:
            st.markdown("**🌱 À semer**")
            for s in info_mois["semis"][:4]:
                st.markdown(f'<div class="card-item">{s}</div>', unsafe_allow_html=True)
        if info_mois["planter"]:
            st.markdown("**🪴 À planter**")
            for p in info_mois["planter"][:3]:
                st.markdown(f'<div class="card-item">{p}</div>', unsafe_allow_html=True)

    with col_b:
        if info_mois["recolter"]:
            st.markdown("**🧺 À récolter**")
            for r in info_mois["recolter"][:4]:
                st.markdown(f'<div class="card-item">{r}</div>', unsafe_allow_html=True)
        if info_mois["travaux"]:
            st.markdown("**🔧 Travaux**")
            for t in info_mois["travaux"][:3]:
                st.markdown(f'<div class="card-item">{t}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Accès rapide
    st.markdown("### 🗺️ Explorer le site")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="card" style="text-align:center"><div style="font-size:2rem">📅</div><strong>Calendrier</strong><br><span class="label">Mois par mois</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card" style="text-align:center"><div style="font-size:2rem">🥕</div><strong>Légumes</strong><br><span class="label">Guide complet</span></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card" style="text-align:center"><div style="font-size:2rem">🤝</div><strong>Associations</strong><br><span class="label">Bons voisins</span></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="card" style="text-align:center"><div style="font-size:2rem">🐛</div><strong>Nuisibles</strong><br><span class="label">Remèdes naturels</span></div>', unsafe_allow_html=True)