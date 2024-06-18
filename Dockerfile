# Utilisation d'une image plus légère
FROM python:3.9-slim

# Définition du répertoire de travail
WORKDIR /app

# Copie des fichiers nécessaires
COPY requirements.txt gunicorn.conf.py /app/

# Installation des dépendances
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copie du reste de l'application
COPY . /app

# Exposition du port
EXPOSE 8000

# Commande pour lancer l'application
CMD ["gunicorn", "-c", "gunicorn.conf.py", "projet_chef_d_oeuvre.wsgi:application"]

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000" ]


## docker run -p 80:80  -v C:\Users\impej\Documents\BRIEF\projet_chef_d_oeuvre_jonathan\projet_chef_d_oeuvre:/app livre
## docker build -t livre .