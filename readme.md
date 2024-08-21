# Web_app_certif

Ce projet est une application web Django développée dans le cadre de ma certification de développeur IA. Il s'agit d'un site web basé sur les données de pneus récoltées par scraping sur le site Carter Cash. Certaines pages nécessitent une authentification pour y accéder, tandis que d'autres sont accessibles publiquement.

## Contenu

- [Installation](#installation)
- [Configuration](#configuration)
- [Structure du Projet](#structure-du-projet)
- [Base de Données](#base-de-données)
- [Fonctionnalités](#fonctionnalités)
- [Contributeurs](#contributeurs)
- [Licence](#licence)

## Installation

1. **Créez un environnement virtuel**
   ```bash
   python -m venv env
   ```

2. **Activez l'environnement virtuel**
   ```bash
   .\env\Scripts\activate
   ```

3. **Installez les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Créez le projet Django**
   ```bash
   django-admin startproject mobivia
   ```

2. **Créez l'application Django**
   ```bash
   python manage.py startapp Carter_cash
   ```

3. **Configurez les variables d'environnement**
   Créez un fichier `.env` à la racine du projet et ajoutez les variables suivantes :
   ```env
   DB_SERVER=xxxxxxxxxxxxx
   DB_DATABASE=xxxxxxxxxxxxx
   DB_USERNAME=xxxxxxxxxxxxx
   DB_PASSWORD=xxxxxxxxxxxxx

   AZURE_SUBSCRIPTION_ID=xxxxxxxxxxxxx
   AZURE_RESOURCE_GROUP=xxxxxxxxxxxxx
   AZURE_CONTAINER_NAME=xxxxxxxxxxxxx
   DOCKER_IMAGE=xxxxxxxxxxxxx

   DOCKER_LOGIN=xxxxxxxxxxxxx
   DOCKER_PASSWORD=xxxxxxxxxxxxx

   SECRET_KEY=xxxxxxxxxxxxx

   token=xxxxxxxxxxxxx

   SECRET_KEY_DJANGO=xxxxxxxxxxxxx

   API_URL=xxxxxxxxxxxxx
   API_TOKEN=xxxxxxxxxxxxx

   AZURE_OPENAI_ENDPOINT=xxxxxxxxxxxxx
   AZURE_OPENAI_KEY=xxxxxxxxxxxxx
   AZURE_OPENAI_DEPLOYMENT=xxxxxxxxxxxxx

   APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxxxxxxxxxxxx
   ```
3. **Commande pour le lancer Django ou des test ou autres ....**
```
cd .\mobivia\
      <-- pour aller dans  le dossier
python .\manage.py runserver
      <-- pour lancer le django
```

```
python manage.py test
      <-- pour lancer le test
```

```
 python manage.py collectstatic
      <-- pour lancer le fichier static 
         ne pas oublier de faire -- pip install whitenoise -- 
         et mettre   dans "MIDDLEWARE " dans settings  'whitenoise.middleware.WhiteNoiseMiddleware', # Juste ici
```
```
python manage.py createsuperuser
      <-- pour crée  le  Super User Django

```

## Structure du Projet

- **mobivia/** : Dossier principal du projet Django.
- **Carter_cash/** : Application Django pour Carter Cash.
- **env/** : Environnement virtuel.
- **requirements.txt** : Liste des dépendances Python.
- **.env** : Fichier de configuration des variables d'environnement.
- **.gitignore** : Fichier de configuration pour ignorer certains fichiers et dossiers dans le dépôt Git.

## Base de Données

La base de données est structurée en plusieurs tables pour gérer les informations sur les produits, les caractéristiques, les dimensions,  les voitures et les prédictions. Voici les scripts de création des tables :

### Table Produit
```sql
CREATE TABLE Produit (
    ID_Produit INT PRIMARY KEY IDENTITY,
    URL_Produit VARCHAR(200),
    Prix INT,
    Info_generale VARCHAR(200),
    Descriptif VARCHAR(200),
    Note VARCHAR(50),
    Date_scrap DATE,
    Marque VARCHAR(200)
)
```

### Table Caracteristiques
```sql
CREATE TABLE Caracteristiques (
    ID_Caracteristique INT PRIMARY KEY IDENTITY,
    Consommation CHAR(1),
    Indice_Pluie CHAR(1),
    Bruit INT,
    Saisonalite VARCHAR(50),
    Type_Vehicule VARCHAR(50),
    Runflat VARCHAR(50),
    ID_Produit INT FOREIGN KEY REFERENCES Produit(ID_Produit)
)
```

### Table Dimensions
```sql
CREATE TABLE Dimensions (
    ID_Dimension INT PRIMARY KEY IDENTITY,
    Largeur INT,
    Hauteur INT,
    Diametre INT,
    Charge INT,
    Vitesse CHAR(1),
    ID_Produit INT FOREIGN KEY REFERENCES Produit(ID_Produit)
)
```




### Table Voiture
```sql
CREATE TABLE Voiture (
    ID_Voiture INT PRIMARY KEY IDENTITY,
    Marque_Voiture VARCHAR(200),
    Modele VARCHAR(200),
    Largeur INT,
    Hauteur INT,
    Diametre INT
)
```

### Table Prediction
```sql
CREATE TABLE Prediction (
    ID_Produit INT PRIMARY KEY IDENTITY,
    Prix_prediction INT,
    Date_prediction DATE,
    Info_generale VARCHAR(200),
    Descriptif VARCHAR(200),
    Note VARCHAR(50),
    Marque VARCHAR(200),
    Consommation CHAR(1),
    Indice_Pluie CHAR(1),
    Bruit INT,
    Saisonalite VARCHAR(50),
    Type_Vehicule VARCHAR(50),
    Runflat VARCHAR(50),
    Largeur INT,
    Hauteur INT,
    Diametre INT,
    Charge INT,
    Vitesse CHAR(1)
)
```

## Fonctionnalités

### Pages nécessitant une authentification

- **Prédiction** : Fonctionnalité de prédiction basée sur une API externe.
- **Chatbot** : Intégration d'un chatbot basé sur Azure OpenAI.
- **Variation de Prix** : Visualisation de l'évolution des prix des produits au fil du temps.

### Pages accessibles publiquement

- **Authentification** : Gestion des utilisateurs avec des pages de connexion, d'inscription et de déconnexion.
- **Recherche de Pneus** : Recherche de pneus par dimensions et marque.

---


## Pages du Site

### Pages nécessitant une authentification

- **Prédiction** : `/prediction/`
- **Chatbot** : `/gpt/`
- **Variation de Prix** : `/variation/`

### Pages accessibles publiquement

- **Accueil** : `/index`
- **Connexion** : `/` (page d'arrivée)
- **Inscription** : `/signup`
- **Déconnexion** : `/logout/`
- **Voiture** : `/voiture/`
- **Trouver Pneu** : `/trouver_pneu/`
- **Dimension** : `/dimension/`


## Monitoring et Observabilité

Cette application Django intègre un système de monitoring basé sur OpenTelemetry, couplé avec Azure Monitor pour une surveillance et une observabilité avancées.

### Configuration du Monitoring

1. **Installer les dépendances nécessaires**
   Assurez-vous que les bibliothèques requises pour OpenTelemetry et Azure Monitor sont installées :
   ```bash
   pip install opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-django opentelemetry-exporter-azure-monitor
   ```

2. **Configurer OpenTelemetry**
   voire code `opentelemetry_setup.py`

3. **Initialiser le monitoring dans Django**
   Ajoutez l'importation de `opentelemetry_setup.py` dans le fichier `manage.py` ou dans le fichier `wsgi.py`/`asgi.py` pour s'assurer que la configuration est chargée au démarrage de l'application.

### Fonctionnalités

 Monitorées

- **Traces** : Capture des traces pour suivre les requêtes effectuées par l'application.
- **Métriques** : Compteur de prédictions par minute.
- **Logs** : Capture et exportation des logs vers Azure Monitor.



## Tests

L'application Django inclut une suite de tests pour garantir le bon fonctionnement des pages protégées et de l'API de prédiction. Les tests sont définis dans le fichier `tests.py` et utilisent le module de test intégré de Django, `django.test`.

### Explication des Tests

1. **Tests des Pages Protégées** :
    - **Redirection sans authentification** : Ces tests vérifient que lorsqu'un utilisateur non authentifié tente d'accéder à des pages nécessitant une connexion (comme la page de prédiction, la page du chatbot, ou la page de variation de prix), il est redirigé vers la page de connexion.
    - **Accès avec authentification** : Ces tests s'assurent qu'un utilisateur authentifié peut accéder aux pages protégées sans être redirigé.

2. **Tests d'API de Prédiction** :
    - **Mocking des appels externes** : Un test simule un appel API à un service de prédiction en utilisant la méthode `patch` de `unittest.mock` pour remplacer les appels réels par des réponses simulées. Ce test vérifie que l'API répond correctement aux données fournies et que le résultat attendu est affiché.

### Détails des Tests

- **ProtectedPagesTests** : 
  - Ce test couvre la redirection des utilisateurs non authentifiés lorsqu'ils essaient d'accéder à des pages protégées.
  - Il teste également que l'utilisateur authentifié peut accéder aux pages comme prévu après une connexion réussie.

- **PredictionAPITest** :
  - Ce test simule une requête POST à l'API de prédiction après qu'un utilisateur s'est authentifié. 
  - Il utilise `patch` pour éviter les appels réels à des services externes pendant les tests, en simulant une réponse avec des résultats de prédiction.

- **ProtectedPagesRedirectTests** :
  - Ce test s'assure que les utilisateurs non connectés sont redirigés vers la page de connexion lorsqu'ils essaient d'accéder à des pages nécessitant une authentification.
  - Il vérifie également que les utilisateurs connectés peuvent accéder aux pages de prédiction, de chatbot et de variation de prix.

### Exécution des Tests

Pour exécuter les tests, utilisez la commande suivante :

```bash
python manage.py test
```

Les tests sont essentiels pour s'assurer que les fonctionnalités critiques, telles que l'accès aux pages protégées et l'intégration de l'API de prédiction, fonctionnent correctement et que l'application répond comme prévu aux différentes interactions utilisateur.


## Contributeurs

- [impejonathan](https://github.com/impejonathan)

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.