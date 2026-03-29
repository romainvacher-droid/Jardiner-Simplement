"""
Calendar page module for Jardiner Simplement.
"""

import streamlit as st
from utils.data_loader import load_calendrier
from datetime import date


def render_calendrier():
    """Render the calendar page."""
    st.title("📅 Calendrier du Jardinier")
    st.markdown("<p style='text-align:center; color:#a5d6a7;'>Que faire au jardin chaque mois de l'année ?</p>", unsafe_allow_html=True)

    calendrier = load_calendrier()
    mois_noms = [calendrier[str(m)]["nom"] for m in range(1, 13)]
    
    # Get current month as default
    current_month = date.today().month
    
    mois_selectionne = st.selectbox(
        "Choisissez un mois",
        options=list(range(1, 13)),
        format_func=lambda m: calendrier[str(m)]["nom"],
        index=current_month - 1,
    )

    info = calendrier[str(mois_selectionne)]

    st.markdown(f'<div class="conseil-box">💬 {info["conseil"]}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🌱 Semis")
        if info["semis"]:
            for s in info["semis"]:
                st.markdown(f'<div class="card-item">{s}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card-item" style="color:#888">Pas de semis ce mois-ci.</div>', unsafe_allow_html=True)

        st.markdown("#### 🪴 Plantations")
        if info["planter"]:
            for p in info["planter"]:
                st.markdown(f'<div class="card-item">{p}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card-item" style="color:#888">Pas de plantations ce mois-ci.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🧺 Récoltes")
        if info["recolter"]:
            for r in info["recolter"]:
                st.markdown(f'<div class="card-item">{r}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card-item" style="color:#888">Pas de récoltes ce mois-ci.</div>', unsafe_allow_html=True)

        st.markdown("#### 🔧 Travaux")
        if info["travaux"]:
            for t in info["travaux"]:
                st.markdown(f'<div class="card-item">{t}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Vue annuelle rapide")
    for m in range(1, 13):
        with st.expander(f"**{calendrier[str(m)]['nom']}**"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Semis :** " + ", ".join(calendrier[str(m)]["semis"][:3]) if calendrier[str(m)]["semis"] else "*—*")
                st.markdown("**Plantations :** " + ", ".join(calendrier[str(m)]["planter"][:3]) if calendrier[str(m)]["planter"] else "*—*")
            with c2:
                st.markdown("**Récoltes :** " + ", ".join(calendrier[str(m)]["recolter"][:3]) if calendrier[str(m)]["recolter"] else "*—*")
                st.markdown("**Travaux :** " + ", ".join(calendrier[str(m)]["travaux"][:2]) if calendrier[str(m)]["travaux"] else "*—*")