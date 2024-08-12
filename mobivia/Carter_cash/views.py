#  views.py
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate , logout
from . import forms
import pyodbc
import os
from dotenv import load_dotenv
import requests
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import PredictionForm

from django.utils.dateparse import parse_date
import plotly.express as px
from openai import AzureOpenAI

import logging
from opentelemetry import trace
from mobivia.opentelemetry_setup import  prediction_counter_per_minute, logger, tracer



# Charger les variables d'environnement
load_dotenv()

API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("API_TOKEN")

# Create your views here.
def get_db_connection():
    """
    FR:
        Établit une connexion à la base de données en utilisant les informations d'identification
        provenant des variables d'environnement.

        Retourne:
            Une connexion pyodbc active à la base de données.

    EN:     
        Establishes a connection to the database using credentials from environment variables.

        Returns:
            An active pyodbc connection to the database.
    """
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_DATABASE')
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')

    driver = '{ODBC Driver 17 for SQL Server}'

    try:
        cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        logger.info("Database connection established")
    except pyodbc.Error as e:
        logger.critical(f"Failed to connect to database: {e}")
        raise e

    return cnxn

def handler404(request, exception):
    """
    FR:
        Gère les erreurs 404 (page non trouvée) en journalisant l'incident
        et en rendant une page personnalisée.

        Args:
            request: L'objet de la requête HTTP.
            exception: L'exception soulevée pour l'erreur 404.

        Retourne:
            Une réponse HTTP avec la page 404 personnalisée.

    EN:     
        Handles 404 errors (page not found) by logging the incident
        and rendering a custom page.

        Args:
            request: The HTTP request object.
            exception: The exception raised for the 404 error.

        Returns:
            An HTTP response with the custom 404 page.
    """
    
    logger.warning("Page not found (404)")
    return render(request, 'Carter_cash/404.html', status=404)

def index(request):
    """
    FR:
        Gère l'accès à la page d'accueil en journalisant l'événement
        et en rendant la page d'accueil.

        Args:
            request: L'objet de la requête HTTP.

        Retourne:
            Une réponse HTTP avec la page d'accueil.

    EN:     
        Handles access to the homepage by logging the event
        and rendering the homepage.

        Args:
            request: The HTTP request object.

        Returns:
            An HTTP response with the homepage.
    """
    logger.info("Index page accessed")
    return render(request, 'Carter_cash/index.html')

def logout_user(request):
    """
    FR:
        Déconnecte l'utilisateur, journalise l'événement, puis redirige
        vers la page de connexion.

        Args:
            request: L'objet de la requête HTTP.

        Retourne:
            Une redirection HTTP vers la page de connexion.

    EN:     
        Logs out the user, logs the event, and then redirects
        to the login page.

        Args:
            request: The HTTP request object.

        Returns:
            An HTTP redirect to the login page.
    """
    logger.info("User logged out")
    logout(request)
    return redirect('login')

def login_page(request):
    """
    FR:
        Gère la logique de connexion des utilisateurs. Si le formulaire
        de connexion est validé, l'utilisateur est authentifié et connecté.

        Args:
            request: L'objet de la requête HTTP.

        Retourne:
            Une réponse HTTP avec la page de connexion et le formulaire.

    EN:     
        Handles user login logic. If the login form is valid,
        the user is authenticated and logged in.

        Args:
            request: The HTTP request object.

        Returns:
            An HTTP response with the login page and form.
    """
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                logger.info(f"User {user.username} logged in")
                return redirect('home')
            else:
                logger.warning("Invalid login attempt")
        message = 'Identifiants invalides.'
    return render(request, 'Carter_cash/login.html', context={'form': form, 'message': message})

def signup_page(request):
    """
    FR:
        Gère l'inscription des utilisateurs. Si le formulaire
        d'inscription est validé, l'utilisateur est créé, connecté
        automatiquement, et redirigé.

        Args:
            request: L'objet de la requête HTTP.

        Retourne:
            Une réponse HTTP avec la page d'inscription et le formulaire.

    EN:     
        Handles user signup. If the signup form is valid,
        the user is created, automatically logged in, and redirected.

        Args:
            request: The HTTP request object.

        Returns:
            An HTTP response with the signup page and form.
    """
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info(f"User {user.username} signed up and logged in")
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'Carter_cash/signup.html', context={'form': form})

def voiture_page(request):
    """
    FR:
        Récupère et affiche les modèles de voitures distincts depuis la base de données.

        Args:
            request: L'objet de la requête HTTP.

        Retourne:
            Une réponse HTTP avec la page des voitures, incluant les marques et modèles.

    EN:     
        Retrieves and displays distinct car models from the database.

        Args:
            request: The HTTP request object.

        Returns:
            An HTTP response with the car page, including makes and models.
    """
    with tracer.start_as_current_span("voiture_page_span"):
        cnxn = get_db_connection()
        cursor = cnxn.cursor()
        cursor.execute("SELECT DISTINCT Marque_Voiture, Modele, Largeur, Hauteur, Diametre FROM Voiture")
        voitures = cursor.fetchall()
        marques_modeles = {}
        for voiture in voitures:
            Marque_Voiture = voiture[0]
            modele = voiture[1]
            if Marque_Voiture not in marques_modeles:
                marques_modeles[Marque_Voiture] = []
            marques_modeles[Marque_Voiture].append({
                'modele': modele,
                'largeur': voiture[2],
                'hauteur': voiture[3],
                'diametre': voiture[4]
            })
        cnxn.close()
        logger.info("Fetched car models from database")
        return render(request, 'Carter_cash/voiture.html', {'marques_modeles': marques_modeles})

def get_marques_by_dimensions(largeur, hauteur, diametre):
    """
    FR:
        Récupère les marques de voiture depuis la base de données
        en fonction des dimensions spécifiées (largeur, hauteur, diamètre).

        Args:
            largeur: La largeur du pneu.
            hauteur: La hauteur du pneu.
            diametre: Le diamètre du pneu.

        Retourne:
            Une liste de marques de voiture correspondant aux dimensions données.

    EN:     
        Retrieves car brands from the database
        based on specified dimensions (width, height, diameter).

        Args:
            largeur: The tire width.
            hauteur: The tire height.
            diametre: The tire diameter.

        Returns:
            A list of car brands matching the given dimensions.
    """
    cnxn = get_db_connection()
    cursor = cnxn.cursor()

    query = """
        SELECT DISTINCT Marque
        FROM Produit
        JOIN Dimensions ON Produit.ID_Produit = Dimensions.ID_Produit
        WHERE Dimensions.Largeur = ? AND Dimensions.Hauteur = ? AND Dimensions.Diametre = ?
    """
    cursor.execute(query, (largeur, hauteur, diametre))
    marques = cursor.fetchall()

    cnxn.close()
    logger.info("Fetched car brands by dimensions from database")

    return [marque[0] for marque in marques]

def dimension_page(request):
    """
    FR:
        Récupère les dimensions distinctes (largeur, hauteur, diamètre) et les marques de voiture
        associées depuis la base de données, et les affiche sur la page.

        Args:
            request: L'objet de la requête HTTP.

        Retourne:
            Une réponse HTTP avec la page des dimensions et les données récupérées.

    EN:     
        Retrieves distinct dimensions (width, height, diameter) and associated car brands
        from the database, and displays them on the page.

        Args:
            request: The HTTP request object.

        Returns:
            An HTTP response with the dimensions page and the retrieved data.
    """
    with tracer.start_as_current_span("dimension_page_span"):
        cnxn = get_db_connection()
        cursor = cnxn.cursor()

        cursor.execute("SELECT DISTINCT Largeur FROM Dimensions ORDER BY Largeur")
        largeurs = cursor.fetchall()

        cursor.execute("SELECT DISTINCT Hauteur FROM Dimensions ORDER BY Hauteur")
        hauteurs = cursor.fetchall()

        cursor.execute("SELECT DISTINCT Diametre FROM Dimensions ORDER BY Diametre")
        diametres = cursor.fetchall()

        selected_largeur = request.GET.get('largeur')
        selected_hauteur = request.GET.get('hauteur')
        selected_diametre = request.GET.get('diametre')

        if selected_largeur and selected_hauteur and selected_diametre:
            marques = get_marques_by_dimensions(selected_largeur, selected_hauteur, selected_diametre)
        else:
            cursor.execute("SELECT DISTINCT Marque FROM Produit ORDER BY Marque")
            marques = cursor.fetchall()
            marques = [marque[0] for marque in marques]

        cnxn.close()
        logger.info("Fetched dimensions and brands for dimension page")

        return render(request, 'Carter_cash/dimension.html', {
            'largeurs': [largeur[0] for largeur in largeurs],
            'hauteurs': [hauteur[0] for hauteur in hauteurs],
            'diametres': [diametre[0] for diametre in diametres],
            'marques': marques,
            'selected_largeur': selected_largeur,
            'selected_hauteur': selected_hauteur,
            'selected_diametre': selected_diametre,
        })

def trouver_pneu(request):
    """
    FR:
        Recherche et affiche les pneus en fonction des dimensions et éventuellement de la marque
        spécifiées dans la base de données.

        Args:
            request: L'objet de la requête HTTP.

        Retourne:
            Une réponse HTTP avec la page des pneus et les résultats de la recherche.

    EN:     
        Searches and displays tires based on specified dimensions and optionally the brand
        from the database.

        Args:
            request: The HTTP request object.

        Returns:
            An HTTP response with the tire page and search results.
    """
    with tracer.start_as_current_span("trouver_pneu_span"):
        largeur = request.GET.get('largeur')
        hauteur = request.GET.get('hauteur')
        diametre = request.GET.get('diametre')
        marque = request.GET.get('marque', '')

        cnxn = get_db_connection()
        cursor = cnxn.cursor()
        query_params = (largeur, hauteur, diametre)

        if marque:
            query = """
            SELECT 
                p.URL_Produit, p.Prix, p.Info_generale, p.Descriptif, p.Note, p.Marque,
                c.Consommation, c.Indice_Pluie, c.Bruit, c.Saisonalite, c.Type_Vehicule, c.Runflat,
                d.Charge, d.Vitesse
            FROM 
                Produit p
            JOIN 
                Dimensions d ON p.ID_Produit = d.ID_Produit
            JOIN 
                Caracteristiques c ON p.ID_Produit = c.ID_Produit
            WHERE 
                d.Largeur = ? AND d.Hauteur = ? AND d.Diametre = ? AND p.Marque = ? AND p.Date_scrap = (
                    SELECT MAX(Date_scrap) FROM Produit
                )
            ORDER BY p.Prix
            """
            query_params = (largeur, hauteur, diametre, marque)
        else:
            query = """
            SELECT 
                p.URL_Produit, p.Prix, p.Info_generale, p.Descriptif, p.Note, p.Marque,
                c.Consommation, c.Indice_Pluie, c.Bruit, c.Saisonalite, c.Type_Vehicule, c.Runflat,
                d.Charge, d.Vitesse
            FROM 
                Produit p
            JOIN 
                Dimensions d ON p.ID_Produit = d.ID_Produit
            JOIN 
                Caracteristiques c ON p.ID_Produit = c.ID_Produit
            WHERE 
                d.Largeur = ? AND d.Hauteur = ? AND d.Diametre = ? AND p.Date_scrap = (
                    SELECT MAX(Date_scrap) FROM Produit
                )
            ORDER BY p.Prix
            """

        cursor.execute(query, query_params)
        pneus = cursor.fetchall()
        cnxn.close()
        logger.info("Fetched tires from database")

        return render(request, 'Carter_cash/pneu.html', {'pneus': pneus})
    
    
    
    
@login_required(login_url='login')
def prediction_view(request):
    """
    FR:
        Gère la soumission du formulaire de prédiction, envoie les données à une API externe
        pour obtenir une prédiction, puis affiche le résultat.

        Args:
            request: L'objet de la requête HTTP.

        Retourne:
            Une réponse HTTP avec la page de prédiction et le résultat.

    EN:     
        Handles the prediction form submission, sends the data to an external API
        to get a prediction, and displays the result.

        Args:
            request: The HTTP request object.

        Returns:
            An HTTP response with the prediction page and result.
    """
    with tracer.start_as_current_span("prediction_view_span"):
        form = PredictionForm()
        prediction = None

        if request.method == 'POST':
            form = PredictionForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                headers = {
                    'Authorization': f'Bearer {API_TOKEN}'
                }
                response = requests.post(API_URL, json=data, headers=headers)
                if response.status_code == 200:
                    prediction = response.json().get('prediction')
                    logger.info("Prediction successful")
                    prediction_counter_per_minute.add(1)
                else:
                    form.add_error(None, 'Erreur lors de la prédiction. Veuillez réessayer.')
                    logger.error("Prediction failed with status code: " + str(response.status_code))

        return render(request, 'Carter_cash/prediction.html', {'form': form, 'prediction': prediction})

################################################################################################
#######################              debut   code chatbot                      #################
################################################################################################

# Code pour le chatbot

load_dotenv()

# Récupérer les variables d'environnement
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_key = os.getenv("AZURE_OPENAI_KEY")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Initialiser le client Azure OpenAI
client = AzureOpenAI(
    azure_endpoint=azure_openai_endpoint,
    api_key=azure_openai_key,
    api_version="2024-02-01",
)


@login_required(login_url='login')
def chatbot_view(request):
    """
    FR:
        Gère l'interaction avec l'utilisateur via le chatbot en utilisant Azure OpenAI.
        Retourne la réponse du chatbot basée sur l'entrée de l'utilisateur.

        Args:
            request: L'objet de la requête HTTP.

        Retourne:
            Une réponse HTTP avec la page du chatbot et la réponse générée.

    EN:     
        Handles user interaction via the chatbot using Azure OpenAI.
        Returns the chatbot's response based on user input.

        Args:
            request: The HTTP request object.

        Returns:
            An HTTP response with the chatbot page and the generated response.
    """
    with tracer.start_as_current_span("chatbot_view_span"):
        if request.method == 'POST':
            user_input = request.POST.get('user_input')
            response = client.chat.completions.create(
                model=deployment,
                messages=[
                    {"role": "system", "content": "Vous êtes un assistant utile."},
                    {"role": "user", "content": user_input},
                ],
            ).choices[0].message.content
            logger.info("Chatbot response generated")
            return render(request, 'Carter_cash/gpt.html', {'response': response, 'user_input': user_input})
        return render(request, 'Carter_cash/gpt.html')

################################################################################################
#######################              fin   code chatbot                        #################
################################################################################################


@login_required(login_url='login')
def variation_page(request):
    """
    FR:
        Gère la visualisation de l'évolution des prix d'un produit spécifique au fil du temps,
        en générant un graphique basé sur les données de la base de données.

        Args:
            request: L'objet de la requête HTTP.

        Retourne:
            Une réponse HTTP avec la page de variation des prix et le graphique généré.

    EN:     
        Handles visualization of a specific product's price evolution over time,
        by generating a graph based on database data.

        Args:
            request: The HTTP request object.

        Returns:
            An HTTP response with the price variation page and the generated graph.
    """
    with tracer.start_as_current_span("variation_page_span"):
        if request.method == 'POST':
            url_produit = request.POST.get('url_produit')
            
            cnxn = get_db_connection()
            cursor = cnxn.cursor()
            query = """
            SELECT Prix, Date_scrap
            FROM Produit
            WHERE URL_Produit = ?
            ORDER BY Date_scrap
            """
            cursor.execute(query, url_produit)
            data = cursor.fetchall()
            cnxn.close()

            if not data:
                error_message = "Cette URL n'est pas dans la BDD."
                logger.error("URL not found in the database")
                return render(request, 'Carter_cash/variation.html', {'error_message': error_message, 'url_produit': url_produit})

            dates = [parse_date(str(row[1])) for row in data]
            prices = [row[0] for row in data]

            fig = px.line(x=dates, y=prices, labels={'x': 'Date', 'y': 'Prix'}, title="Évolution du prix dans le temps")
            graph_html = fig.to_html(full_html=False)

            logger.info("Price variation graph generated")
            return render(request, 'Carter_cash/variation.html', {'graph_html': graph_html, 'url_produit': url_produit})
        
        return render(request, 'Carter_cash/variation.html')