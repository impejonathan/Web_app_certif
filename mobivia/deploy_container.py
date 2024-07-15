import subprocess
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Informations d'authentification et de configuration
azure_subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
resource_group = os.getenv("AZURE_RESOURCE_GROUP")
container_name = os.getenv("AZURE_CONTAINER_NAME")
docker_image = os.getenv("DOCKER_IMAGE")
docker_username = os.getenv("DOCKER_USERNAME")
docker_password = os.getenv("DOCKER_PASSWORD")

# Chemin vers l'exécutable `az`
az_path = r"C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin\az.cmd"

# Connexion à Azure
def azure_login():
    print("Connexion à Azure...")
    subprocess.run([az_path, "login"], check=True)
    subprocess.run([az_path, "account", "set", "--subscription", azure_subscription_id], check=True)

# Créer le groupe de ressources (si nécessaire)
def create_resource_group():
    print(f"Création du groupe de ressources {resource_group}...")
    subprocess.run([az_path, "group", "create", "--name", resource_group, "--location", "francecentral"], check=True)

# Créer le conteneur dans Azure
def create_container_instance():
    print(f"Création du conteneur {container_name} à partir de l'image {docker_image}...")
    subprocess.run([
        az_path, "container", "create",
        "--resource-group", resource_group,
        "--name", container_name,
        "--image", docker_image,
        "--cpu", "1",
        "--memory", "1.5",
        "--registry-username", docker_username,
        "--registry-password", docker_password,
        "--dns-name-label", container_name,
        "--ports", "80"
    ], check=True)

# Script principal
if __name__ == "__main__":
    azure_login()
    create_resource_group()
    create_container_instance()
    print(f"Le conteneur {container_name} a été créé avec succès.")


# pour le lancer "python deploy_container.py"