Description du Projet
=====================

Présentation
------------

OC Lettings est une application web développée avec le framework Django permettant
la gestion de locations immobilières (lettings) et de profils utilisateurs.

L'application est structurée en trois applications Django distinctes :

1. **oc_lettings_site** : Application principale contenant la configuration du projet
2. **lettings** : Gestion des biens immobiliers et leurs adresses
3. **profiles** : Gestion des profils utilisateurs

Architecture
------------

L'application suit une architecture modulaire Django classique :

.. code-block:: text

    Python-OC-Lettings-FR/
    ├── oc_lettings_site/     # Configuration principale
    │   ├── settings.py       # Paramètres Django
    │   ├── urls.py           # Routes principales
    │   └── views.py          # Vues (home, 404, 500)
    ├── lettings/             # App de gestion des locations
    │   ├── models.py         # Modèles Address, Letting
    │   ├── views.py          # Vues index, detail
    │   └── tests.py          # Tests unitaires
    ├── profiles/             # App de gestion des profils
    │   ├── models.py         # Modèle Profile
    │   ├── views.py          # Vues index, detail
    │   └── tests.py          # Tests unitaires
    ├── templates/            # Templates HTML
    ├── static/               # Fichiers statiques (CSS, JS)
    └── doc/                  # Documentation Sphinx

Fonctionnalités
---------------

**Gestion des Lettings (Locations)**

- Liste de toutes les locations disponibles
- Détail d'une location avec adresse complète
- Interface d'administration pour CRUD

**Gestion des Profils**

- Liste de tous les profils utilisateurs
- Détail d'un profil avec ville favorite
- Lien avec le système d'authentification Django

**Monitoring**

- Intégration Sentry pour le suivi des erreurs
- Logging configurable par application
- Pages d'erreur personnalisées (404, 500)
