# Changelog

All notable changes to the "Jardiner Simplement" project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Complete modular architecture with separate data/, components/, utils/, and pages/ directories
- JSON-based data storage for easy maintenance and updates
- Global search functionality across all content (vegetables, calendar, pests, treatments)
- Personal garden tracker ("Mon Jardin") with add/remove plants and export functionality
- Favorites system ("Mes Favoris") with persistent session state
- Smart tools:
  - Planting calculator with bed dimension inputs
  - Companion planting planner with compatibility matrix
- Print/export features:
  - HTML garden plan generation
  - Text list export
- Docker deployment with Dockerfile and docker-compose.yml
- Environment variable management with .env.example
- Enhanced CSS with animations, improved mobile UX, and better component styling
- Comprehensive error handling and user feedback
- Session state management for user data persistence

### Improved
- Performance optimization with @st.cache_data decorators on all data loading functions
- Code organization: separated concerns into modules and components
- Navigation: added search bar and reorganized page links
- UI/UX: smoother transitions, better visual hierarchy, improved accessibility
- Mobile responsiveness with stacked columns on small screens
- Search results with relevance scoring and highlighting

### Changed
- Migrated from monolithic app_streamlit.py to modular architecture
- All hardcoded data moved to JSON files in data/ directory
- Navigation system now uses session state for page routing
- CSS styling enhanced with animations and modern design elements

## [1.0.0] - 2026-03-29

### Added
- Initial release of Jardiner Simplement
- Core pages: Accueil, Calendrier, Légumes, Associations, Nuisibles, Traitements
- 10 vegetables with detailed cultural information
- 12-month gardening calendar with tasks for each month
- Companion planting associations (positive and negative)
- 7 common pests with natural solutions
- 6 natural treatment recipes
- 25 daily gardening tips
- PWA support with manifest.json
- Dark theme with green color palette
- Responsive design for mobile and desktop

[//]: # (Future versions will be added as the project evolves)