# Utiliser une image de base officielle Python
FROM python:3.10

# Définir le répertoire de travail dans le conteneur
WORKDIR Practical 4/app
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev
# Copier les fichiers de dépendances et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers de l'application dans le conteneur
COPY . .

# Exposer le port sur lequel l'application sera accessible
EXPOSE 8000

# Définir la commande par défaut pour exécuter l'application
CMD ["python", "main.py"]