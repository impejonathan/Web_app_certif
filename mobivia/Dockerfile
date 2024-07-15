FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libpq-dev \
        curl \   
        gnupg \ 
        && apt-get -y autoremove \
        && apt-get clean

# Add Microsoft repository for msodbcsql18
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Install msodbcsql18
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 msodbcsql18

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app


# Exposition du port
EXPOSE 80

# Commande pour lancer l'application
# CMD ["gunicorn", "-c", "gunicorn.conf.py", "projet_chef_d_oeuvre.wsgi:application"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:80" ]


# docker build -t impejonathan/carter .
# docker run -p 8000:8000 --env-file .env impejonathan/carter
# docker push impejonathan/carter
