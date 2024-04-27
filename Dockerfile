# Utiliser une image de base Python officielle.
FROM python:3.10

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . /app

# Installer les dépendances nécessaires
RUN pip install matplotlib

# Commande pour exécuter l'application
CMD ["python", "main.py"]