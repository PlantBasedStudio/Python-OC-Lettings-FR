Installation
============

Prérequis
---------

- Python 3.11 ou supérieur
- pip (gestionnaire de paquets Python)
- Git
- Docker (optionnel, pour le déploiement conteneurisé)

Installation locale
-------------------

1. **Cloner le repository**

   .. code-block:: bash

      git clone https://github.com/votre-username/Python-OC-Lettings-FR.git
      cd Python-OC-Lettings-FR

2. **Créer un environnement virtuel**

   .. code-block:: bash

      python -m venv venv

      # Windows
      venv\Scripts\activate

      # Linux/Mac
      source venv/bin/activate

3. **Installer les dépendances**

   .. code-block:: bash

      pip install -r requirements.txt

4. **Configurer les variables d'environnement**

   Copiez le fichier ``.env.example`` en ``.env`` et configurez vos valeurs :

   .. code-block:: bash

      cp .env.example .env

   Variables disponibles :

   - ``SECRET_KEY`` : Clé secrète Django
   - ``DEBUG`` : Mode debug (True/False)
   - ``ALLOWED_HOSTS`` : Hôtes autorisés
   - ``SENTRY_DSN`` : URL Sentry pour le monitoring
   - ``SENTRY_ENVIRONMENT`` : Environnement Sentry

5. **Appliquer les migrations**

   .. code-block:: bash

      python manage.py migrate

6. **Collecter les fichiers statiques**

   .. code-block:: bash

      python manage.py collectstatic

7. **Lancer le serveur de développement**

   .. code-block:: bash

      python manage.py runserver

   L'application est accessible à : http://localhost:8000

Installation avec Docker
------------------------

1. **Construire l'image Docker**

   .. code-block:: bash

      docker build -t oc-lettings-site .

2. **Lancer le conteneur**

   .. code-block:: bash

      docker run -p 8000:8000 \
        -e SECRET_KEY="votre-cle-secrete" \
        -e DEBUG=False \
        -e ALLOWED_HOSTS="localhost,127.0.0.1" \
        oc-lettings-site

   L'application est accessible à : http://localhost:8000
