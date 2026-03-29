"""
Personal garden tracker page module for Jardiner Simplement.
"""

import streamlit as st
from utils.data_loader import load_legumes, get_mois_info
from utils.auth import is_authenticated, get_current_user, update_user_garden
from datetime import date, timedelta


def render_mon_jardin():
    """Render the personal garden tracker page."""
    st.title("🌱 Mon Jardin")
    st.markdown(
        "<p style='text-align:center; color:#a5d6a7;'>"
        "Suivez vos plantations et planifiez vos récoltes."
        "</p>",
        unsafe_allow_html=True
    )

    # Check authentication
    if not is_authenticated():
        st.warning("🔐 Veuillez vous connecter pour gérer votre jardin.")
        if st.button("Se connecter", type="primary"):
            st.session_state.page = "login"
            st.rerun()
        return

    # Initialize garden in session state if not exists
    if "mon_jardin" not in st.session_state:
        st.session_state.mon_jardin = []

    # Add new plant section
    st.markdown("### ➕ Ajouter une plantation")
    
    legumes = load_legumes()
    legume_options = list(legumes.keys())
    
    col1, col2, col3 = st.columns(3)
    with col1:
        legume_nom = st.selectbox(
            "Légume",
            options=legume_options,
            format_func=lambda x: f"{legumes[x]['emoji']} {x}"
        )
    with col2:
        date_plantation = st.date_input(
            "Date de plantation",
            value=date.today(),
            max_value=date.today() + timedelta(days=30)
        )
    with col3:
        quantite = st.number_input(
            "Quantité (nombre de plants)",
            min_value=1,
            max_value=100,
            value=1,
            step=1
        )
    
    # Show info about selected legume
    if legume_nom:
        legume_data = legumes[legume_nom]
        st.markdown(f"**📅 Semis :** {legume_data['semis']}")
        st.markdown(f"**🪴 Plantation :** {legume_data['plantation']}")
        st.markdown(f"**🧺 Récolte :** {legume_data['recolte']}")
        st.markdown(f"**📏 Espacement :** {legume_data['espacement']}")
    
    if st.button("✅ Ajouter au jardin", type="primary"):
        # Check if already exists
        exists = any(
            p["legume"] == legume_nom and p["date_plantation"] == date_plantation
            for p in st.session_state.mon_jardin
        )
        if exists:
            st.warning(f"{legume_nom} est déjà dans votre jardin pour cette date !")
        else:
            st.session_state.mon_jardin.append({
                "legume": legume_nom,
                "date_plantation": date_plantation,
                "quantite": quantite,
                "emoji": legume_data["emoji"]
            })
            # Save to user file
            if is_authenticated():
                update_user_garden(get_current_user(), st.session_state.mon_jardin)
            st.success(f"{legume_data['emoji']} {legume_nom} ajouté à votre jardin !")
            st.rerun()
    
    st.markdown("---")
    
    # Display current garden
    st.markdown("### 📋 Mon Jardin")
    
    if not st.session_state.mon_jardin:
        st.info("Votre jardin est vide. Ajoutez des plantations ci-dessus !")
    else:
        # Group by month for overview
        st.markdown("#### Vue par mois")
        
        # Create a simple timeline
        for plant in sorted(st.session_state.mon_jardin, key=lambda x: x["date_plantation"]):
            legume_nom = plant["legume"]
            legume_data = legumes[legume_nom]
            date_plant = plant["date_plantation"]
            
            # Estimate harvest time (simplified rough estimate)
            mois_plantation = date_plant.month
            if "primeurs" in legume_data["recolte"].lower() or "nouvelles" in legume_data["recolte"].lower():
                mois_recolte = ((mois_plantation - 1 + 2) % 12) + 1
            elif "juillet" in legume_data["recolte"].lower() or "août" in legume_data["recolte"].lower():
                mois_recolte = ((mois_plantation - 1 + 3) % 12) + 1
            else:
                mois_recolte = ((mois_plantation - 1 + 4) % 12) + 1
            
            with st.container():
                col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
                with col1:
                    st.markdown(f'<div style="font-size:2rem; text-align:center;">{plant["emoji"]}</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f"**{legume_nom}**")
                    st.markdown(f"Planté le : {date_plant.strftime('%d/%m/%Y')}")
                    st.markdown(f"Quantité : {plant['quantite']} plant(s)")
                with col3:
                    st.markdown(f"**📋 Infos culture**")
                    st.markdown(f"Semis : {legume_data['semis'][:30]}...")
                    st.markdown(f"Récolte : {legume_data['recolte'][:30]}...")
                with col4:
                    if st.button("🗑️", key=f"delete_{legume_nom}_{date_plant}"):
                        st.session_state.mon_jardin.remove(plant)
                        # Save to user file
                        if is_authenticated():
                            update_user_garden(get_current_user(), st.session_state.mon_jardin)
                        st.rerun()
                st.markdown("---")
        
        # Summary statistics
        st.markdown("### 📊 Statistiques")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_plants = sum(p["quantite"] for p in st.session_state.mon_jardin)
            st.metric("Total de plants", total_plants)
        
        with col2:
            unique_legumes = len(set(p["legume"] for p in st.session_state.mon_jardin))
            st.metric("Types de légumes", unique_legumes)
        
        with col3:
            # Count plants by season
            printemps = sum(1 for p in st.session_state.mon_jardin if p["date_plantation"].month in [3, 4, 5])
            ete = sum(1 for p in st.session_state.mon_jardin if p["date_plantation"].month in [6, 7, 8])
            automne = sum(1 for p in st.session_state.mon_jardin if p["date_plantation"].month in [9, 10, 11])
            hiver = sum(1 for p in st.session_state.mon_jardin if p["date_plantation"].month in [12, 1, 2])
            
            if printemps >= ete and printemps >= automne and printemps >= hiver:
                season = "Printemps"
            elif ete >= printemps and ete >= automne and ete >= hiver:
                season = "Été"
            elif automne >= printemps and automne >= ete and automne >= hiver:
                season = "Automne"
            else:
                season = "Hiver"
            
            st.metric("Saison principale", season)
        
        # Export functionality
        st.markdown("---")
        st.markdown("### 📤 Exporter mon jardin")
        
        if st.button("📄 Générer un plan de jardin (HTML)"):
            generate_garden_plan()
        
        if st.button("📋 Copier la liste"):
            # Create a simple text list
            text_list = "Mon Jardin - Jardiner Simplement\n"
            text_list += f"Généré le : {date.today().strftime('%d/%m/%Y')}\n"
            text_list += "=" * 50 + "\n\n"
            
            for plant in sorted(st.session_state.mon_jardin, key=lambda x: x["date_plantation"]):
                legume_nom = plant["legume"]
                legume_data = legumes[legume_nom]
                text_list += f"{plant['emoji']} {legume_nom}\n"
                text_list += f"  Planté le : {plant['date_plantation'].strftime('%d/%m/%Y')}\n"
                text_list += f"  Quantité : {plant['quantite']} plant(s)\n"
                text_list += f"  Récolte : {legume_data['recolte']}\n"
                text_list += "\n"
            
            st.code(text_list, language="text")
            st.success("Liste générée ! Vous pouvez la copier.")


def generate_garden_plan():
    """Generate a simple HTML garden plan."""
    legumes = load_legumes()
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Mon Jardin - Jardiner Simplement</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            h1 { color: #4caf50; }
            .plant { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px; }
            .emoji { font-size: 2rem; }
            .date { color: #666; font-size: 0.9rem; }
            .info { margin-top: 10px; color: #444; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌱 Mon Plan de Jardin</h1>
            <p>Généré le : """ + date.today().strftime('%d/%m/%Y') + """</p>
            <hr>
    """
    
    for plant in sorted(st.session_state.mon_jardin, key=lambda x: x["date_plantation"]):
        legume_nom = plant["legume"]
        legume_data = legumes[legume_nom]
        
        html += f"""
            <div class="plant">
                <div class="emoji">{plant['emoji']}</div>
                <h3>{legume_nom}</h3>
                <p class="date">Planté le : {plant['date_plantation'].strftime('%d/%m/%Y')} | Quantité : {plant['quantite']} plant(s)</p>
                <div class="info">
                    <strong>Semis :</strong> {legume_data['semis']}<br>
                    <strong>Plantation :</strong> {legume_data['plantation']}<br>
                    <strong>Récolte :</strong> {legume_data['recolte']}<br>
                    <strong>Espacement :</strong> {legume_data['espacement']}<br>
                    <strong>Exposition :</strong> {legume_data['exposition']}<br>
                    <strong>Arrosage :</strong> {legume_data['arrosage']}
                </div>
            </div>
        """
    
    html += """
        </div>
    </body>
    </html>
    """
    
    st.download_button(
        label="⬇️ Télécharger le plan (HTML)",
        data=html,
        file_name=f"mon_jardin_{date.today().strftime('%Y%m%d')}.html",
        mime="text/html"
    )