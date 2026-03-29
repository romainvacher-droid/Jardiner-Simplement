# 🌱 Jardiner Simplement

Site web de conseils jardinage naturel, développé avec Streamlit. Une application complète pour accompagner les jardiniers amateurs dans leurs cultures potagères.

## ✨ Fonctionnalités

- **📅 Calendrier du jardinier** : Guide mois par mois pour savoir quoi semer, planter, récolter et quels travaux effectuer
- **🥕 Guide des légumes** : Fiches détaillées pour 10+ légumes avec conseils de culture, associations et maladies
- **🤝 Associations de plantes** : Découvrez quelles plantes s'entraident ou se nuisent
- **🐛 Nuisibles & Maladies** : Identification et solutions naturelles pour les problèmes courants
- **🌿 Traitements naturels** : Recettes de purins, décoctions et traitements maison
- **⭐ Mes Favoris** : Sauvegardez vos légumes, associations et solutions préférés
- **🌱 Mon Jardin** : Suivez vos plantations et générez des plans de culture
- **🔧 Outils & Calculateurs** :
  - Calculateur de plantation (estimation du nombre de plants)
  - Planificateur d'associations

## 🚀 Installation & Démarrage

### Option 1 : Exécution directe (recommandé pour le développement)

```bash
# Cloner le dépôt
git clone https://github.com/romainvacher-droid/Jardiner-Simplement.git
cd Jardiner-Simplement

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app_streamlit.py
```

L'application sera accessible à l'adresse : http://localhost:8501

### Option 2 : Avec Docker

```bash
# Construire et lancer avec docker-compose
docker-compose up --build

# Ou avec Docker seul
docker build -t jardiner-simplement .
docker run -p 8501:8501 jardiner-simplement
```

L'application sera accessible à l'adresse : http://localhost:8501

## 📁 Structure du projet

```
Jardiner-Simplement/
├── app_streamlit.py          # Application principale
├── requirements.txt          # Dépendances Python
├── Dockerfile               # Configuration Docker
├── docker-compose.yml       # Orchestration Docker
├── .env.example             # Exemple de variables d'environnement
├── .gitignore               # Fichiers ignorés par Git
├── manifest.json            # PWA manifest
├── Procfile                 # Configuration Heroku
├── data/                    # Données JSON
│   ├── conseils.json
│   ├── calendrier.json
│   ├── legumes.json
│   ├── associations.json
│   ├── nuisibles.json
│   └── traitements.json
├── utils/                   # Utilitaires
│   └── data_loader.py
├── components/              # Composants réutilisables
│   └── navigation.py
└── pages/                   # Pages de l'application
    ├── accueil.py
    ├── calendrier.py
    ├── legumes.py
    ├── associations.py
    ├── nuisibles.py
    ├── traitements.py
    ├── favoris.py
    ├── mon_jardin.py
    └── outils.py
```

## 🎯 Utilisation

### Navigation
- Utilisez la barre de navigation en haut pour accéder aux différentes pages
- La barre de recherche permet de trouver rapidement des légumes, des mois, des nuisibles ou des traitements

### Mes Favoris
- Cliquez sur "⭐ Ajouter aux favoris" sur n'importe quelle fiche de légume
- Retrouvez tous vos favoris sur la page "Mes Favoris"
- Exportez votre liste facilement

### Mon Jardin
- Ajoutez vos plantations avec la date et la quantité
- Visualisez un aperçu de votre jardin
- Exportez un plan de jardin en HTML
- Consultez des statistiques sur vos cultures

### Outils
- **Calculateur de plantation** : Estimez le nombre de plants nécessaires selon vos dimensions de planche
- **Planificateur d'associations** : Vérifiez la compatibilité de vos légumes avant de planter

## 🔧 Configuration

### Variables d'environnement
Copiez `.env.example` vers `.env` et ajustez selon vos besoins :

```bash
cp .env.example .env
```

Options disponibles :
- `STREAMLIT_SERVER_PORT` : Port d'écoute (défaut: 8501)
- `STREAMLIT_SERVER_ADDRESS` : Adresse d'écoute (défaut: 0.0.0.0)
- `APP_ENV` : Environnement (development/production)

## 🚢 Déploiement

### Heroku
L'application est configurée pour Heroku avec le `Procfile` :

```bash
heroku create jardiner-simplement
git push heroku main
heroku open
```

### Railway
```bash
railway init
railway up
```

### VPS / Serveur dédié
```bash
# Avec Docker Compose
docker-compose up -d

# Sans Docker
pip install -r requirements.txt
streamlit run app_streamlit.py --server.port $PORT --server.address 0.0.0.0
```

## 📊 Performance

- **Cache intelligent** : Les données sont chargées une seule fois grâce à `@st.cache_data`
- **Modularité** : Code organisé en composants réutilisables
- **Responsive** : Interface adaptée mobile et desktop
- **PWA-ready** : Peut être installée comme application native

## 🛠️ Développement

### Ajouter un nouveau légume
1. Ouvrez `data/legumes.json`
2. Ajoutez une nouvelle entrée avec les champs requis :
   - `emoji` : Emoji représentant le légume
   - `description` : Description courte
   - `semis`, `plantation`, `recolte` : Calendrier cultural
   - `exposition`, `arrosage`, `espacement` : Conditions de culture
   - `associations_positives`, `associations_negatives` : Compagnons
   - `maladies` : Maladies fréquentes
   - `conseil` : Conseil expert

### Ajouter une nouvelle association
Modifiez `data/associations.json` avec le format :
```json
{
  "plante1": "Tomate 🍅",
  "plante2": "Basilic 🌿",
  "effet": "✅ Le basilic repousse les pucerons..."
}
```

## 📝 Licence

Ce projet est open source et disponible sous licence MIT.

## 🙏 Remerciements

- Développé avec [Streamlit](https://streamlit.io/)
- Design inspiré par la nature et le jardinage biologique
- Données basées sur des pratiques de jardinage traditionnelles et modernes

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.

---

**🌱 Bon jardinage à tous !**