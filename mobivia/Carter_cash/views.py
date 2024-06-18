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





# Charger les variables d'environnement
load_dotenv()

API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("API_TOKEN")

# Create your views here.
def get_db_connection():
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_DATABASE')
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')

    driver= '{ODBC Driver 17 for SQL Server}'

    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    return cnxn


def handler404(request, exception):
    return render(request, 'Carter_cash/404.html', status=404)


def index(request):
    return render(request, 
                  'Carter_cash/index.html',
                  )
    
def logout_user(request):
    
    logout(request)
    return redirect('login')



def login_page(request):
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
                return redirect('home')
        message = 'Identifiants invalides.'
    return render(request, 'Carter_cash/login.html', context={'form': form, 'message': message})


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'Carter_cash/signup.html', context={'form': form})



def voiture_page(request):
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
    return render(request, 'Carter_cash/voiture.html', {'marques_modeles': marques_modeles})




# Ajouter cette fonction pour récupérer les marques en fonction des dimensions
def get_marques_by_dimensions(largeur, hauteur, diametre):
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

    return [marque[0] for marque in marques]

def dimension_page(request):
    cnxn = get_db_connection()
    cursor = cnxn.cursor()

    cursor.execute("SELECT DISTINCT Largeur FROM Dimensions ORDER BY Largeur")
    largeurs = cursor.fetchall()

    cursor.execute("SELECT DISTINCT Hauteur FROM Dimensions ORDER BY Hauteur")
    hauteurs = cursor.fetchall()

    cursor.execute("SELECT DISTINCT Diametre FROM Dimensions ORDER BY Diametre")
    diametres = cursor.fetchall()

    # Ajouter ces lignes pour initialiser les variables et utiliser la fonction get_marques_by_dimensions
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
    largeur = request.GET.get('largeur')
    hauteur = request.GET.get('hauteur')
    diametre = request.GET.get('diametre')
    marque = request.GET.get('marque', '') # Marque sélectionnée (ou vide si aucune sélection)

    cnxn = get_db_connection()
    cursor = cnxn.cursor()
    query_params = (largeur, hauteur, diametre)

    # Construire la requête en fonction de la sélection de la marque
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
    
    return render(request, 'Carter_cash/pneu.html', {'pneus': pneus})



def prediction_view(request):
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
            else:
                form.add_error(None, 'Erreur lors de la prédiction. Veuillez réessayer.')

    return render(request, 'Carter_cash/prediction.html', {'form': form, 'prediction': prediction})


################################################################################################
#######################              debut   code chatbot                      #################
################################################################################################


# Code pour le chatbot

os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
os.environ["AZURE_OPENAI_KEY"] = os.getenv("AZURE_OPENAI_KEY")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_KEY"],
    api_version="2024-02-01",
)

def chatbot_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ],
        ).choices[0].message.content
        return render(request, 'Carter_cash/gpt.html', {'response': response, 'user_input': user_input})
    return render(request, 'Carter_cash/gpt.html')

################################################################################################
#######################              fin   code chatbot                        #################
################################################################################################




from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.shortcuts import render
import plotly.express as px

def variation_page(request):
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
            return render(request, 'Carter_cash/variation.html', {'error_message': error_message, 'url_produit': url_produit})

        dates = [parse_date(str(row[1])) for row in data]
        prices = [row[0] for row in data]

        fig = px.line(x=dates, y=prices, labels={'x': 'Date', 'y': 'Prix'}, title="Évolution du prix dans le temps")
        graph_html = fig.to_html(full_html=False)

        return render(request, 'Carter_cash/variation.html', {'graph_html': graph_html, 'url_produit': url_produit})
    
    return render(request, 'Carter_cash/variation.html')
