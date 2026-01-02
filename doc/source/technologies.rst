Technologies et Langages
========================

Ce document liste les technologies utilisées dans le projet OC Lettings.

Langages de programmation
-------------------------

**Python 3.11**

Langage principal de l'application backend.

**HTML5 / CSS3 / JavaScript**

Technologies frontend pour les templates et l'interface utilisateur.

Framework Web
-------------

**Django 4.2 LTS**

Framework web Python utilisé pour :

- Routing des URLs
- ORM (Object-Relational Mapping)
- Système de templates
- Administration automatique
- Authentification utilisateur

Base de données
---------------

**SQLite** (Développement)

Base de données légère intégrée, utilisée en développement.

Serveur WSGI
------------

**Gunicorn**

Serveur HTTP Python WSGI pour la production.

Fichiers statiques
------------------

**WhiteNoise**

Middleware pour servir les fichiers statiques en production sans serveur
web externe (Nginx, Apache).

Monitoring
----------

**Sentry**

Plateforme de monitoring d'erreurs et de performance :

- Capture automatique des exceptions
- Alertes en temps réel
- Analyse des performances
- Breadcrumbs pour le débogage

Conteneurisation
----------------

**Docker**

Conteneurisation de l'application pour :

- Environnement reproductible
- Déploiement simplifié
- Isolation des dépendances

CI/CD
-----

**GitHub Actions**

Pipeline d'intégration et déploiement continus :

- Linting automatique
- Tests automatisés
- Build Docker
- Déploiement automatique

Documentation
-------------

**Sphinx**

Générateur de documentation Python :

- Documentation automatique depuis le code
- Format reStructuredText
- Thème Read The Docs

**Read The Docs**

Plateforme d'hébergement de documentation :

- Build automatique
- Versioning
- Hébergement gratuit

Tests
-----

**pytest**

Framework de tests Python :

- Tests unitaires
- Fixtures réutilisables
- Plugins extensibles

**pytest-django**

Plugin pytest pour Django :

- Client de test
- Accès à la base de données de test
- Assertions Django

**pytest-cov / coverage**

Mesure de couverture de code :

- Rapport HTML
- Intégration CI/CD
- Seuil minimum configurable

Qualité de code
---------------

**flake8**

Outil de linting Python :

- Vérification PEP 8
- Détection d'erreurs
- Configuration personnalisable

Dépendances du projet
---------------------

Liste complète des dépendances (requirements.txt) :

.. code-block:: text

   # Framework
   django==4.2.9

   # Linting
   flake8==7.0.0

   # Tests
   pytest==7.4.0
   pytest-django==4.7.0
   pytest-cov==4.1.0
   coverage==7.3.0

   # Monitoring
   sentry-sdk==1.29.0

   # Production
   gunicorn==21.2.0
   whitenoise==6.5.0

   # Configuration
   python-dotenv==1.0.0

   # Documentation
   sphinx==7.2.6
   sphinx-rtd-theme==1.3.0
