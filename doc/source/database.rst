Structure de la Base de Données
===============================

L'application utilise SQLite en développement. Les modèles sont définis dans les
applications ``lettings`` et ``profiles``.

Modèles de données
------------------

Address (Adresse)
~~~~~~~~~~~~~~~~~

Représente une adresse physique pour les locations.

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Champ
     - Type
     - Description
   * - number
     - PositiveIntegerField
     - Numéro de rue (1-9999)
   * - street
     - CharField(64)
     - Nom de la rue
   * - city
     - CharField(64)
     - Ville
   * - state
     - CharField(2)
     - Code état (ex: CA, NY)
   * - zip_code
     - PositiveIntegerField
     - Code postal (1-99999)
   * - country_iso_code
     - CharField(3)
     - Code pays ISO (ex: USA)

Letting (Location)
~~~~~~~~~~~~~~~~~~

Représente un bien immobilier à louer.

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Champ
     - Type
     - Description
   * - title
     - CharField(256)
     - Titre de la location
   * - address
     - OneToOneField
     - Relation vers Address (cascade delete)

Profile (Profil)
~~~~~~~~~~~~~~~~

Représente un profil utilisateur étendu.

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Champ
     - Type
     - Description
   * - user
     - OneToOneField
     - Relation vers User Django (cascade delete)
   * - favorite_city
     - CharField(64)
     - Ville favorite (optionnel)

Diagramme des relations
-----------------------

.. code-block:: text

    ┌─────────────┐         ┌─────────────┐
    │   Address   │ 1     1 │   Letting   │
    │─────────────│─────────│─────────────│
    │ number      │         │ title       │
    │ street      │         │ address(FK) │
    │ city        │         └─────────────┘
    │ state       │
    │ zip_code    │
    │ country_iso │
    └─────────────┘

    ┌─────────────┐         ┌─────────────┐
    │    User     │ 1     1 │   Profile   │
    │  (Django)   │─────────│─────────────│
    │─────────────│         │ user(FK)    │
    │ username    │         │favorite_city│
    │ email       │         └─────────────┘
    │ password    │
    └─────────────┘

Migrations
----------

Les migrations sont gérées automatiquement par Django.

.. code-block:: bash

   # Créer de nouvelles migrations
   python manage.py makemigrations

   # Appliquer les migrations
   python manage.py migrate

   # Voir l'état des migrations
   python manage.py showmigrations
