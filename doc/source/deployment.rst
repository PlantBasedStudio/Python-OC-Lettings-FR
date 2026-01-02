Guide de Déploiement
====================

Ce guide détaille les procédures de déploiement de l'application OC Lettings.

Prérequis
---------

- Un compte Docker Hub
- Un compte GitHub avec le repository configuré
- Un compte sur une plateforme d'hébergement (Render, Heroku, etc.)
- Un compte Sentry (optionnel mais recommandé)

Pipeline CI/CD
--------------

L'application utilise GitHub Actions pour l'intégration et le déploiement continus.

**Workflow automatique** :

1. À chaque push sur ``master``, le pipeline se déclenche
2. Exécution du linting (flake8)
3. Exécution des tests avec couverture
4. Construction de l'image Docker
5. Push de l'image sur Docker Hub
6. Déploiement sur la plateforme d'hébergement

Configuration des secrets GitHub
--------------------------------

Dans les paramètres de votre repository GitHub, ajoutez les secrets suivants :

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Secret
     - Description
   * - DOCKER_USERNAME
     - Votre nom d'utilisateur Docker Hub
   * - DOCKER_PASSWORD
     - Votre mot de passe ou token Docker Hub
   * - RENDER_DEPLOY_HOOK_URL
     - URL du webhook de déploiement Render
   * - SECRET_KEY
     - Clé secrète Django pour la production
   * - SENTRY_DSN
     - URL DSN de votre projet Sentry

Déploiement sur Render
----------------------

1. **Créer un compte Render** sur https://render.com

2. **Créer un nouveau Web Service**

   - Connectez votre repository GitHub
   - Sélectionnez "Docker" comme environnement
   - Configurez le nom du service

3. **Configurer les variables d'environnement**

   Dans les paramètres du service Render :

   .. code-block:: text

      SECRET_KEY=votre-cle-secrete-generee
      DEBUG=False
      ALLOWED_HOSTS=votre-app.onrender.com
      SENTRY_DSN=https://xxx@sentry.io/xxx
      SENTRY_ENVIRONMENT=production

4. **Récupérer le Deploy Hook**

   - Allez dans Settings > Deploy Hook
   - Copiez l'URL et ajoutez-la comme secret GitHub ``RENDER_DEPLOY_HOOK_URL``

5. **Désactiver le déploiement automatique**

   Important : Désactivez l'auto-deploy dans Render pour que le déploiement
   soit uniquement déclenché par le pipeline CI/CD.

Utilisation de Docker
---------------------

**Récupérer l'image depuis Docker Hub** :

.. code-block:: bash

   docker pull votre-username/oc-lettings-site:latest

**Lancer le conteneur** :

.. code-block:: bash

   docker run -d -p 8000:8000 \
     -e SECRET_KEY="votre-cle-secrete" \
     -e DEBUG=False \
     -e ALLOWED_HOSTS="localhost" \
     -e SENTRY_DSN="https://xxx@sentry.io/xxx" \
     votre-username/oc-lettings-site:latest

Configuration Sentry
--------------------

1. **Créer un projet Sentry**

   - Allez sur https://sentry.io
   - Créez un nouveau projet Django
   - Récupérez le DSN

2. **Configurer le DSN**

   Ajoutez le DSN dans vos variables d'environnement :

   .. code-block:: bash

      SENTRY_DSN=https://xxx@sentry.io/xxx
      SENTRY_ENVIRONMENT=production

3. **Vérifier l'intégration**

   Provoquez une erreur pour vérifier que Sentry la capture correctement.

Checklist de déploiement
------------------------

Avant chaque mise en production :

☐ Les tests passent (couverture > 80%)
☐ Le linting ne retourne aucune erreur
☐ Les variables d'environnement sont configurées
☐ DEBUG est désactivé
☐ ALLOWED_HOSTS est correctement configuré
☐ Les fichiers statiques sont collectés
☐ La connexion Sentry est fonctionnelle
