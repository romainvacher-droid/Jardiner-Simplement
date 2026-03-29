"""
Login and registration page for Jardiner Simplement.
"""

import streamlit as st
from utils.auth import (
    login_user, 
    register_user, 
    logout_user, 
    is_authenticated, 
    get_current_user
)


def render_login():
    """Render the login/registration page."""
    st.title("🔐 Connexion / Inscription")
    st.markdown(
        "<p style='text-align:center; color:#a5d6a7;'>"
        "Connectez-vous ou créez un compte pour sauvegarder vos préférences."
        "</p>",
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # Check if user is already logged in
    if is_authenticated():
        st.success(f"✅ Vous êtes connecté en tant que **{get_current_user()}**")
        st.markdown("Vos données (favoris et jardin) sont sauvegardées automatiquement.")
        
        if st.button("🚪 Déconnexion", type="secondary"):
            logout_user()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📋 Votre profil")
        st.markdown(f"**Nom d'utilisateur :** {get_current_user()}")
        st.markdown("**Préférences sauvegardées :**")
        st.markdown("- ✅ Favoris (légumes, associations, nuisibles)")
        st.markdown("- ✅ Votre jardin (plantations)")
        
        return
    
    # Create two columns for login and register
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔑 Connexion")
        login_username = st.text_input("Nom d'utilisateur", key="login_username")
        login_password = st.text_input("Mot de passe", type="password", key="login_password")
        
        if st.button("Se connecter", key="btn_login", type="primary", use_container_width=True):
            if login_user(login_username, login_password):
                st.success(f"✅ Bienvenue, {login_username} !")
                st.rerun()
            else:
                st.error("❌ Nom d'utilisateur ou mot de passe incorrect.")
    
    with col2:
        st.markdown("### 📝 Inscription")
        reg_username = st.text_input("Nom d'utilisateur", key="reg_username")
        reg_password = st.text_input("Mot de passe", type="password", key="reg_password")
        reg_confirm = st.text_input("Confirmer le mot de passe", type="password", key="reg_confirm")
        
        if st.button("Créer un compte", key="btn_register", type="secondary", use_container_width=True):
            success, message = register_user(reg_username, reg_password, reg_confirm)
            if success:
                st.success(f"✅ {message}")
                # Auto-login after registration
                if login_user(reg_username, reg_password):
                    st.rerun()
            else:
                st.error(f"❌ {message}")
    
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#888; font-size:0.9rem;'>"
        "Vos données sont stockées localement dans le dossier <code>users/</code>."
        "</div>",
        unsafe_allow_html=True
    )