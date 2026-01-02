Interfaces de programmation et Points d'accès
=============================================

L'application expose des vues Django rendant des templates HTML.
Voici la liste des URLs disponibles.

Routes principales
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - URL
     - Nom
     - Description
   * - ``/``
     - index
     - Page d'accueil du site
   * - ``/admin/``
     - admin
     - Interface d'administration Django
   * - ``/lettings/``
     - lettings:index
     - Liste de toutes les locations
   * - ``/lettings/<id>/``
     - lettings:letting
     - Détail d'une location
   * - ``/profiles/``
     - profiles:index
     - Liste de tous les profils
   * - ``/profiles/<username>/``
     - profiles:profile
     - Détail d'un profil utilisateur

Vues de l'application oc_lettings_site
--------------------------------------

index
~~~~~

- **URL** : ``/``
- **Méthode** : GET
- **Template** : ``index.html``
- **Description** : Affiche la page d'accueil avec navigation vers lettings et profiles

custom_404_view
~~~~~~~~~~~~~~~

- **URL** : Toute URL non trouvée
- **Template** : ``404.html``
- **Code HTTP** : 404
- **Description** : Page d'erreur personnalisée pour les ressources non trouvées

custom_500_view
~~~~~~~~~~~~~~~

- **URL** : Erreur serveur
- **Template** : ``500.html``
- **Code HTTP** : 500
- **Description** : Page d'erreur personnalisée pour les erreurs internes

Vues de l'application lettings
------------------------------

index
~~~~~

- **URL** : ``/lettings/``
- **Méthode** : GET
- **Template** : ``lettings/index.html``
- **Contexte** : ``lettings_list`` (QuerySet de tous les Letting)

letting
~~~~~~~

- **URL** : ``/lettings/<int:letting_id>/``
- **Méthode** : GET
- **Template** : ``letting.html``
- **Contexte** : ``title``, ``address``
- **Erreur** : 404 si letting_id n'existe pas

Vues de l'application profiles
------------------------------

index
~~~~~

- **URL** : ``/profiles/``
- **Méthode** : GET
- **Template** : ``profiles/index.html``
- **Contexte** : ``profiles_list`` (QuerySet de tous les Profile)

profile
~~~~~~~

- **URL** : ``/profiles/<str:username>/``
- **Méthode** : GET
- **Template** : ``profile.html``
- **Contexte** : ``profile``
- **Erreur** : 404 si username n'existe pas

Utilisation des URLs dans les templates
---------------------------------------

.. code-block:: html

   <!-- Lien vers la page d'accueil -->
   <a href="{% url 'index' %}">Accueil</a>

   <!-- Lien vers la liste des lettings -->
   <a href="{% url 'lettings:index' %}">Locations</a>

   <!-- Lien vers un letting spécifique -->
   <a href="{% url 'lettings:letting' letting_id=1 %}">Location 1</a>

   <!-- Lien vers la liste des profils -->
   <a href="{% url 'profiles:index' %}">Profils</a>

   <!-- Lien vers un profil spécifique -->
   <a href="{% url 'profiles:profile' username='john' %}">Profil de John</a>
