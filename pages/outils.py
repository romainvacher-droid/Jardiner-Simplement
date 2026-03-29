"""
Tools page module for Jardiner Simplement - includes calculators and planners.
"""

import streamlit as st
from utils.data_loader import load_legumes, load_associations


def render_outils():
    """Render the tools page."""
    st.title("🔧 Outils & Calculateurs")
    st.markdown(
        "<p style='text-align:center; color:#a5d6a7;'>"
        "Des outils pratiques pour planifier votre jardin."
        "</p>",
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(["📐 Calculateur de plantation", "🤝 Planificateur d'associations"])

    legumes = load_legumes()
    associations = load_associations()

    with tab1:
        render_planting_calculator(legumes)
    
    with tab2:
        render_companion_planner(legumes, associations)


def render_planting_calculator(legumes):
    """Render the planting calculator."""
    st.markdown("### 📐 Calculateur de Plantation")
    st.markdown("Estimez le nombre de plants nécessaires et l'espacement pour votre potager.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        legume_nom = st.selectbox(
            "Choisissez un légume",
            options=list(legumes.keys()),
            format_func=lambda x: f"{legumes[x]['emoji']} {x}",
            key="calc_legume"
        )
        
        if legume_nom:
            legume_data = legumes[legume_nom]
            st.markdown(f"**Espacement recommandé :** {legume_data['espacement']}")
            
            # Parse spacing to calculate
            spacing_text = legume_data['espacement']
            # Extract numbers for calculation
            import re
            numbers = re.findall(r'(\d+(?:\.\d+)?)', spacing_text)
            if numbers:
                avg_spacing = sum(float(n) for n in numbers) / len(numbers)
                st.markdown(f"**Espacement moyen estimé :** {avg_spacing:.1f} cm")
    
    with col2:
        if legume_nom:
            # Input for bed dimensions
            st.markdown("#### Dimensions de votre planche")
            longueur = st.number_input("Longueur (cm)", min_value=0.0, value=300.0, step=10.0)
            largeur = st.number_input("Largeur (cm)", min_value=0.0, value=120.0, step=10.0)
            
            if longueur > 0 and largeur > 0:
                # Calculate area
                surface = (longueur / 100) * (largeur / 100)  # in m²
                st.markdown(f"**Surface :** {surface:.2f} m²")
                
                # Estimate number of plants
                if avg_spacing > 0:
                    # Simple calculation: area / (spacing²) converted to m²
                    spacing_m = avg_spacing / 100
                    plants_par_m2 = 1 / (spacing_m ** 2)
                    estimated_plants = int(surface * plants_par_m2)
                    
                    st.markdown(f"**Plants estimés par m² :** {plants_par_m2:.1f}")
                    st.markdown(f"### 🌱 Nombre total estimé : **{estimated_plants} plants**")
                    
                    # Show a simple visual
                    st.progress(min(estimated_plants / 50, 1.0), text=f"Capacité: {estimated_plants} plants")
                    
                    # Recommendations
                    st.markdown("#### 💡 Recommandations")
                    st.markdown(f"- Prévoyez **{estimated_plants + int(estimated_plants*0.1)}** plants (avec 10% de marge)")
                    st.markdown(f"- Pour une planche de {longueur}×{largeur} cm")
                    st.markdown(f"- Espacement de {avg_spacing} cm entre les plants")


def render_companion_planner(legumes, associations):
    """Render the companion planting planner."""
    st.markdown("### 🤝 Planificateur d'Associations")
    st.markdown("Sélectionnez vos légumes pour voir quelles associations sont recommandées ou à éviter.")
    
    # Multi-select for vegetables
    selected_legumes = st.multiselect(
        "Choisissez vos légumes",
        options=list(legumes.keys()),
        format_func=lambda x: f"{legumes[x]['emoji']} {x}",
        help="Sélectionnez un ou plusieurs légumes que vous souhaitez planter"
    )
    
    if selected_legumes:
        st.markdown("---")
        st.markdown("### Résultats d'association")
        
        # Find all relevant associations
        positive_matches = []
        negative_matches = []
        
        for assoc in associations:
            p1 = assoc["plante1"]
            p2 = assoc["plante2"]
            
            # Remove emojis for comparison
            p1_clean = p1.split(" ")[-1] if " " in p1 else p1
            p2_clean = p2.split(" ")[-1] if " " in p2 else p2
            
            for selected in selected_legumes:
                if selected in p1 or selected in p1_clean:
                    other = p2_clean
                    if other in legumes and other not in selected_legumes:
                        if "✅" in assoc["effet"]:
                            positive_matches.append((selected, other, assoc["effet"]))
                        else:
                            negative_matches.append((selected, other, assoc["effet"]))
                if selected in p2 or selected in p2_clean:
                    other = p1_clean
                    if other in legumes and other not in selected_legumes:
                        if "✅" in assoc["effet"]:
                            positive_matches.append((selected, other, assoc["effet"]))
                        else:
                            negative_matches.append((selected, other, assoc["effet"]))
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✅ Associations favorables")
            if positive_matches:
                for selected, other, effet in positive_matches:
                    st.markdown(
                        f'<div class="card-item">'
                        f'<strong>{selected}</strong> + <strong>{other}</strong><br>'
                        f'<span style="color:#69f0ae">{effet}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.info("Aucune association favorable trouvée pour votre sélection.")
        
        with col2:
            st.markdown("#### ❌ Associations à éviter")
            if negative_matches:
                for selected, other, effet in negative_matches:
                    st.markdown(
                        f'<div class="card-item" style="border-left-color: #ff5252;">'
                        f'<strong>{selected}</strong> + <strong>{other}</strong><br>'
                        f'<span style="color:#ff5252">{effet}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.success("Aucune association problématique trouvée pour votre sélection !")
        
        # General principles reminder
        st.markdown("---")
        st.markdown("#### 📌 Principes à retenir")
        st.markdown("""
        - 🌿 **Les aromates** (basilic, persil) sont généralement de bons compagnons
        - 🌸 **Les fleurs** (capucines, soucis) protègent les légumes
        - 🚫 **Évitez le fenouil** avec la plupart des légumes
        - 🔄 **Rotations** : ne replantez pas la même famille au même endroit
        """)


def render_bed_layout():
    """Render a simple bed layout visualization (placeholder for future enhancement)."""
    st.markdown("### 🗺️ Plan de plantation (à venir)")
    st.info("Cette fonctionnalité est en développement. Elle permettra de visualiser l'agencement de vos planches de culture.")