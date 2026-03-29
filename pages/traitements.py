"""
Natural treatments page module for Jardiner Simplement.
"""

import streamlit as st
from utils.data_loader import load_traitements


def render_traitements():
    """Render the treatments page."""
    st.title("🌿 Traitements Naturels")
    st.markdown(
        "<p style='text-align:center; color:#a5d6a7;'>"
        "Recettes de soins maison pour un jardin sain."
        "</p>",
        unsafe_allow_html=True
    )

    traitements = load_traitements()

    for t in traitements:
        with st.container():
            st.markdown(
                f'<div class="card">'
                f'<h3>{t["emoji"]} {t["nom"]}</h3>'
                f'<p><span class="label">Usage :</span> {t["usage"]}</p>'
                f'<p><span class="label">Recette :</span> {t["recette"]}</p>'
                f'<p><span class="label">Application :</span> {t["application"]}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
            st.markdown("---")