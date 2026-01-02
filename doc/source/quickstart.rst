Guide de démarrage rapide
=========================

Ce guide vous permet de lancer rapidement l'application en local.

Démarrage en 5 minutes
----------------------

.. code-block:: bash

   # 1. Cloner et se positionner dans le projet
   git clone https://github.com/votre-username/Python-OC-Lettings-FR.git
   cd Python-OC-Lettings-FR

   # 2. Créer et activer l'environnement virtuel
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou venv\Scripts\activate  # Windows

   # 3. Installer les dépendances
   pip install -r requirements.txt

   # 4. Lancer le serveur
   python manage.py runserver

Naviguer dans l'application
---------------------------

Une fois le serveur lancé, vous pouvez accéder aux URLs suivantes :

- **Page d'accueil** : http://localhost:8000/
- **Liste des locations** : http://localhost:8000/lettings/
- **Liste des profils** : http://localhost:8000/profiles/
- **Administration** : http://localhost:8000/admin/

Accès administrateur
--------------------

Pour accéder à l'interface d'administration :

- **URL** : http://localhost:8000/admin/
- **Username** : admin
- **Password** : admin

Lancer les tests
----------------

.. code-block:: bash

   # Lancer tous les tests
   pytest

   # Lancer les tests avec couverture
   pytest --cov=. --cov-report=html

   # Voir le rapport de couverture
   # Ouvrir htmlcov/index.html dans un navigateur

Vérifier le linting
-------------------

.. code-block:: bash

   flake8 --max-line-length=99 --exclude=venv,migrations .
