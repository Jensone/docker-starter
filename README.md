# Docker – Guide Complet pour Débutants

## 1. Introduction à Docker

Docker est une plateforme logicielle qui utilise la **conteneurisation** pour exécuter des applications dans des environnements isolés appelés *conteneurs*. Un conteneur embarque une application ainsi que toutes ses dépendances (bibliothèques, configuration, etc.) afin qu’elle puisse tourner de manière uniforme sur tout système supportant Docker ([Docker, c'est quoi ?](https://www.redhat.com/fr/topics/containers/what-is-docker#:~:text=Voici%20les%20diff%C3%A9rentes%20d%C3%A9finitions%C2%A0%3A)). En s’appuyant sur des fonctionnalités du noyau Linux (telles que les *cgroups* et les *namespaces*), Docker parvient à isoler les processus tout en consommant peu de ressources ([Docker, c'est quoi ?](https://www.redhat.com/fr/topics/containers/what-is-docker#:~:text=La%20technologie%20Docker%20utilise%20le,que%20celui%20des%20syst%C3%A8mes%20distincts)). On obtient ainsi un niveau d’isolation suffisant pour exécuter plusieurs applications sur la même machine en toute sécurité, sans conflits de dépendances, et avec une empreinte beaucoup plus légère qu’avec la virtualisation traditionnelle.

**Avantages de Docker :** la conteneurisation avec Docker présente de nombreux atouts : 

- **Portabilité** – Un conteneur Docker peut être exécuté sur n’importe quel système disposant de Docker (Linux, Windows, macOS). Cela garantit que l’application fonctionne de la même manière en développement, en test ou en production.
- **Légèreté et rapidité** – Les conteneurs sont très légers comparés aux machines virtuelles car ils partagent le noyau de l’OS hôte. Ils se lancent en quelques secondes (voire moins) et consomment peu de RAM et de CPU, ce qui permet d’en exécuter un grand nombre sur une machine donnée ([Docker, c'est quoi ?](https://www.redhat.com/fr/topics/containers/what-is-docker#:~:text=)).
- **Isolation** – Chaque conteneur s’exécute de façon isolée, avec son propre système de fichiers, ses variables d’environnement et ses ports. Cela évite les conflits entre applications et améliore la sécurité (un problème dans un conteneur n’affecte pas les autres).
- **Scalabilité** – Grâce à leur démarrage rapide et leur faible overhead, il est facile de créer ou supprimer des conteneurs à la volée pour adapter la charge (montée en charge horizontale). Docker s’intègre bien avec des outils d’orchestration (comme Kubernetes) qui automatisent cette scalabilité.
- **Reproductibilité** – Docker permet de définir l’environnement d’une application dans un fichier de configuration (Dockerfile). Cela assure que chaque développeur ou serveur utilise le même environnement, éliminant le classique « *ça marche sur ma machine* ».

Un conteneur peut être comparé à une machine virtuelle très minimaliste. Pour bien comprendre, examinons les différences entre conteneurs Docker et machines virtuelles (VM) classiques :

| **Caractéristique**         | **Machine Virtuelle (VM)**                                               | **Conteneur Docker**                                           |
|----------------------------|-------------------------------------------------------------------------|---------------------------------------------------------------|
| **Isolation**              | Isolation complète incluant un OS invité séparé. Très sûr, le VM est entièrement sandboxé du système hôte. | Isolation au niveau du système d’exploitation hôte (partage du même noyau). Moins hermétique qu’une VM, mais suffisamment cloisonné pour la plupart des usages ([Docker, c'est quoi ?](https://www.redhat.com/fr/topics/containers/what-is-docker#:~:text=une%20br%C3%A8che%20de%20s%C3%A9curit%C3%A9,mieux%20isol%C3%A9es%20du%20syst%C3%A8me%20h%C3%B4te)). |
| **Système d’exploitation** | Chaque VM embarque son propre OS complet (kernel + userland). Consomme davantage de CPU, RAM, stockage. | Ne contient que l’application et ses dépendances au-dessus du noyau de l’OS hôte. Pas de kernel invité -> empreinte réduite. |
| **Démarrage**              | Lancement en minutes : il faut booter un OS entier.                      | Lancement en quelques secondes : le processus de l’application démarre directement, le kernel étant déjà là. |
| **Portabilité**            | Images lourdes (plusieurs Go) spécifiques à un hyperviseur, moins faciles à déplacer. | Images légères (quelques dizaines ou centaines de Mo) partageables via des registres (Docker Hub, etc.), faciles à transférer. |
| **Compatibilité OS**       | Peut exécuter un OS invité différent de l’hôte (ex: une VM Windows sur un Linux). | Doit utiliser le même type de noyau que l’hôte (ex: conteneurs Linux sur un hôte Linux). Pas de noyau Windows sur un Docker Linux (sauf via VM). |
| **Performances**           | Overhead important dû à la virtualisation du matériel complet.           | Overhead minime : performances proches de l’exécution native, grâce à l’utilisation directe du kernel de l’hôte. |

En résumé, Docker ne *virtualise* pas du matériel comme le fait une VM ; il *isole* des processus au-dessus du système hôte. Cela explique qu’un conteneur soit beaucoup plus léger en ressources qu’une VM tout en restant suffisamment isolé pour la plupart des applications. Grâce à Docker, on obtient « des machines virtuelles très légères et modulaires » faciles à créer, déployer, copier et déplacer d’un environnement à un autre ([Docker, c'est quoi ?](https://www.redhat.com/fr/topics/containers/what-is-docker#:~:text=Gr%C3%A2ce%20%C3%A0%20Docker%2C%20les%20conteneurs,ainsi%20optimis%C3%A9es%20pour%20le%20cloud)).

Docker a révolutionné les workflows de développement et de déploiement. Il s’est imposé comme un outil incontournable du mouvement DevOps, permettant aux développeurs et aux administrateurs système de collaborer plus efficacement. En développant votre application dans un conteneur, vous pouvez garantir qu’elle fonctionnera de façon identique chez tous les membres de l’équipe et en production. Dans les chapitres suivants, nous allons découvrir comment installer Docker, l’utiliser pas à pas, construire nos propres images, et enfin orchestrer des conteneurs en production.

## 2. Installation de Docker

Docker peut s’installer sur la plupart des environnements : distributions Linux, Windows 10/11 et macOS. Les étapes d’installation varient selon le système d’exploitation. Nous détaillons ci-dessous la procédure pour Linux, Windows et macOS.

### 2.1 Sur Linux (Ubuntu/Debian)

Nous prenons ici l’exemple d’Ubuntu (les étapes sont similaires pour Debian). L’installation se fait via la ligne de commande :

1. **Désinstaller d’anciennes versions (le cas échéant)** – Si Docker était déjà installé via les dépôts officiels d’Ubuntu sous le nom `docker.io` ou une ancienne version *Docker*/*Docker Engine*, il est recommandé de la supprimer pour éviter les conflits :  
   ```bash
   sudo apt remove docker docker-engine docker.io containerd runc
   ```
   (Cette commande ignore les packages non installés.)

2. **Installer les prérequis** – Mettez à jour l’index APT et installez les paquets permettant d’utiliser un repository via HTTPS :  
   ```bash
   sudo apt update
   sudo apt install -y ca-certificates curl gnupg lsb-release
   ```
   Ces paquets servent à ajouter la clé GPG de Docker et le dépôt officiel.

3. **Ajouter le dépôt officiel Docker** – Ajoutez la clé GPG officielle de Docker, puis le dépôt stable à vos sources APT :  
   ```bash
   sudo mkdir -p /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
       | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
     https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
     | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```  
   Cette commande configure le dépôt Docker pour votre distribution (la variable `$(lsb_release -cs)` insère le nom de code d’Ubuntu, par ex. *focal*, *jammy*...).

4. **Installer Docker Engine** – Mettez à jour l’index des paquets puis installez Docker et Containerd (son runtime conteneur) :  
   ```bash
   sudo apt update
   sudo apt install -y docker-ce docker-ce-cli containerd.io
   ```  
   Après l’installation, le service Docker (daemon) démarre automatiquement. Vous pouvez vérifier son statut par `sudo systemctl status docker`.

5. **Post-installation (optionnel)** – Par défaut, la commande `docker` doit être exécutée avec les droits *root* (ou via `sudo`). Pour permettre à votre utilisateur de lancer Docker sans `sudo`, ajoutez-le au groupe `docker` :  
   ```bash
   sudo usermod -aG docker $USER
   ```  
   **Note:** Il faudra vous déconnecter/reconnecter (ou lancer un nouveau shell) pour que ce changement prenne effet. Ensuite, la commande `docker info` devrait fonctionner sans `sudo`.

6. **Tester l’installation** – Lancez le conteneur de test officiel :  
   ```bash
   docker run hello-world
   ```  
   Ce conteneur d’exemple affiche un message de bienvenue, confirmant que Docker fonctionne correctement. S’il s’exécute sans erreur, Docker est bien installé sur votre système.

### 2.2 Sur Windows 10/11

Sous Windows, Docker s’exécute via **Docker Desktop**, une application fournissant le moteur Docker dans une machine virtuelle légère (basée sur Hyper-V ou WSL2). Voici comment l’installer :

1. **Vérifier les prérequis** – Docker Desktop requiert Windows 10/11 64-bit. Sur Windows 10 Home/Pro, assurez-vous d’avoir la fonctionnalité Windows Subsystem for Linux 2 (**WSL2**) activée (Docker l’utilise pour faire tourner Docker Engine). Activez également la **virtualisation** dans le BIOS de votre PC si ce n’est pas déjà le cas.
2. **Télécharger Docker Desktop** – Rendez-vous sur le site officiel de Docker et téléchargez l’installeur Docker Desktop pour Windows (un fichier `.exe`).
3. **Installer Docker Desktop** – Exécutez l’installeur. Cochez l’option d’utilisation de WSL2 si proposée. L’installation va configurer Docker et WSL2 automatiquement. Un redémarrage peut être demandé.
4. **Lancer Docker** – Après installation, lancez **Docker Desktop** depuis le menu Démarrer. Attendez que Docker démarre (l’icône Docker dans la zone de notification deviendra stable ou affichera « Docker is running »).
5. **Tester avec un conteneur** – Ouvrez un terminal PowerShell ou l’invite de commandes (CMD) et exécutez :  
   ```powershell
   docker run hello-world
   ```  
   Vous devriez voir le message de bienvenue de Docker, comme sous Linux. Docker est opérationnel sur votre machine Windows. (En arrière-plan, Docker utilise une VM Linux via WSL2 pour exécuter ce conteneur Linux.)

*Remarques Windows :* Docker Desktop intègre une interface utilisateur pour configurer des paramètres (par ex. la quantité de mémoire/CPU allouée à Docker, le choix entre backend WSL2 ou Hyper-V, etc.). Docker Desktop permet également d’exécuter des conteneurs Windows natifs si nécessaire, mais par défaut, c’est le mode conteneurs Linux qui est utilisé, car c’est le plus courant.

### 2.3 Sur macOS

Sous macOS, Docker s’installe également via Docker Desktop :

1. **Télécharger Docker Desktop** – Depuis le site officiel Docker, téléchargez l’image disque **Docker Desktop for Mac** (`.dmg`) compatible avec votre version de macOS (Intel ou Apple Silicon).
2. **Installer l’application** – Ouvrez le fichier `.dmg` puis faites glisser l’icône Docker dans le dossier Applications.
3. **Lancer Docker** – Ouvrez Docker Desktop (via Spotlight ou Applications). Au premier lancement, macOS vous demandera d’autoriser Docker à avoir les privilèges administrateur pour installer ses composants (Docker utilise en interne l’hyperviseur macOS pour créer une VM Linux). Acceptez et entrez votre mot de passe si requis.
4. **Vérifier le démarrage** – Patientez quelques instants le temps que Docker démarre en arrière-plan. Vous devriez voir l’indicateur « Docker is running » dans la barre de menus (une icône de baleine).
5. **Tester un conteneur** – Ouvrez l’application Terminal et lancez :  
   ```bash
   docker run hello-world
   ```  
   Si le message de bienvenue s’affiche, l’installation est un succès.

*Remarques macOS :* Comme sur Windows, Docker Desktop sur Mac gère une VM Linux légère en coulisses (via *hyperkit* ou le framework de virtualisation Apple) pour exécuter Docker Engine. Vous pouvez ajuster dans les préférences la RAM/CPU alloués à Docker. L’utilisation de Docker sur Mac ou Windows est quasiment identique à Linux du point de vue des commandes (une fois Docker Desktop en fonctionnement). 

## 3. Premiers pas avec Docker

Maintenant que Docker est installé, explorons les bases de son utilisation. Nous allons apprendre à exécuter notre premier conteneur, à gérer les **images Docker** locales, et à utiliser les commandes courantes de Docker.

### 3.1 Exécuter un premier conteneur

La commande de base pour lancer un conteneur est `docker run`. Par exemple, exécutons un conteneur simple qui affiche un message puis s’arrête :

```bash
docker run hello-world
```

Docker va rechercher l’image nommée **hello-world** en local. Si elle n’est pas trouvée, il la téléchargera automatiquement depuis Docker Hub (le registre public par défaut). Une fois l’image récupérée, Docker crée un conteneur et exécute le programme à l’intérieur. Dans ce cas, le conteneur affiche un message de bienvenue puis se termine. Vous verrez dans la console le texte "Hello from Docker!" confirmant le bon fonctionnement de Docker.

Maintenant, lançons un conteneur plus utile, par exemple un serveur web Nginx. Nous utiliserons l’option `-d` (détaché) pour lancer le conteneur en arrière-plan, et `-p 8080:80` pour publier le port 80 du conteneur sur le port 8080 de notre machine :

```bash
docker run -d -p 8080:80 --name monserveur nginx:latest
```

Cette commande télécharge l’image **nginx:latest** (si pas déjà présente), puis démarre un conteneur nommé *monserveur* exécutant Nginx en arrière-plan. Le serveur web à l’intérieur écoute sur le port 80 du conteneur, que nous avons mappé sur le port 8080 de l’hôte. Cela signifie qu’on peut ouvrir un navigateur et accéder à `http://localhost:8080` pour voir la page par défaut d’Nginx. 

On peut vérifier que le conteneur tourne bien via la commande `docker ps` (nous verrons cette commande en détail dans la section suivante). Si besoin, on peut consulter les logs du conteneur Nginx avec `docker logs monserveur`. Pour arrêter le conteneur, utilisez `docker stop monserveur` (ce qui envoie un signal d’arrêt au processus Nginx). Vous pouvez ensuite le redémarrer avec `docker start monserveur` si nécessaire.

> 🔹 **Astuce :** La première fois que vous lancez une image Docker, le téléchargement peut prendre du temps (dépendant de la taille de l’image et de votre connexion). Les exécutions suivantes seront instantanées si l’image est déjà présente localement.

### 3.2 Gestion des images Docker

Une **image Docker** est un gabarit (template) à partir duquel les conteneurs sont lancés. On peut voir une image comme une « classe », et un conteneur comme une « instance » de cette classe. Docker fournit des centaines d’images officielles sur Docker Hub (par exemple nginx, mysql, ubuntu, node, etc.), et vous pouvez aussi construire vos propres images (voir chapitre 4).

Quelques commandes utiles pour gérer les images en local :

- `docker images` : liste les images présentes sur votre machine (nom, tag, identifiant, taille, etc.).
- `docker pull <image>` : télécharge une image depuis Docker Hub sans la lancer. Par exemple, `docker pull ubuntu:20.04` récupère l’image Ubuntu 20.04.
- `docker rmi <image>` : supprime une image locale (si plus aucun conteneur ne l’utilise). Utile pour faire du ménage et économiser de l’espace disque.
- `docker search <mot-clé>` : permet de rechercher des images sur Docker Hub en fonction d’un mot-clé (ex: `docker search redis`).

Lorsque nous avons lancé `docker run hello-world`, Docker a fait implicitement un `pull` de l’image *hello-world*. De même, `docker run nginx` va automatiquement télécharger l’image *nginx:latest* si vous ne l’avez pas déjà. Vous pouvez bien sûr spécifier une version particulière d’une image en ajoutant un **tag** après le nom (format `nom:tag`). Par défaut, si aucun tag n’est précisé, Docker utilise le tag `latest` (souvent le dernier build stable). Par exemple, `docker run alpine:3.16` lancera Alpine Linux v3.16, tandis que `docker run alpine` équivaut à `alpine:latest` (la version alpine la plus récente).

Pour voir un aperçu des images sur votre système, exécutez `docker images`. Essayez par exemple après avoir lancé quelques conteneurs de test :

```bash
$ docker images
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
nginx        latest    <image-id>     2 weeks ago   142MB
ubuntu       20.04     <image-id>     3 weeks ago   72.8MB
hello-world  latest    <image-id>     5 months ago  13kB
```

On voit le nom du dépôt (repository), le tag, l’ID unique de l’image, la date de création et la taille. Ici nous avons trois images : nginx, ubuntu:20.04, et hello-world.

### 3.3 Commandes Docker de base

Docker propose de nombreuses commandes pour examiner et manipuler les conteneurs et images. Voici un tableau récapitulatif des commandes de base que tout débutant doit connaître :

| **Commande**                    | **Description**                                                |
|---------------------------------|----------------------------------------------------------------|
| `docker run <image>`            | Télécharge (si besoin) l’image spécifiée et crée un nouveau conteneur à partir de celle-ci, puis l’exécute. Des options peuvent être ajoutées (voir exemples précédents). |
| `docker ps`                     | Liste les conteneurs *en cours d’exécution*. Ajoutez `-a` (`docker ps -a`) pour lister *tous* les conteneurs, y compris arrêtés. |
| `docker stop <nom ou id>`          | Arrête un conteneur (en envoyant un signal SIGTERM puis SIGKILL si nécessaire après délai). |
| `docker start <nom ou id>`         | Démarre un conteneur qui était arrêté (ne fonctionne pas sur un conteneur déjà supprimé). |
| `docker restart <nom ou id>`       | Redémarre un conteneur (équivalent à un stop suivi d’un start). |
| `docker rm <nom ou id>`            | Supprime un conteneur arrêté (supprime ses ressources). Ajoutez `-f` pour forcer la suppression d’un conteneur même s’il est en cours d’exécution (Docker effectuera alors un stop forcé). |
| `docker logs <nom ou id>`          | Affiche les logs (stdout/stderr) d’un conteneur. Utile pour vérifier le output d’une application tournant en arrière-plan. Ajoutez `-f` pour *follower* les logs en continu. |
| `docker exec -it <cont> <cmd>`  | Exécute une commande à l’intérieur d’un conteneur en cours d’exécution. Par exemple `docker exec -it monserveur /bin/bash` ouvre un shell Bash interactif dans le conteneur *monserveur*. Très pratique pour du débogage. |
| `docker inspect <nom ou id>`       | Fournit en sortie JSON tous les détails sur un conteneur ou une image (configuration, réseaux, volumes, variables d’env, etc.). |

Avec ces commandes de base, vous pouvez déjà piloter l’essentiel de Docker : lancer et arrêter des applications conteneurisées, surveiller leurs logs, et gérer les images. Au fil des chapitres, nous introduirons d’autres commandes plus spécifiques (par exemple pour les volumes, les réseaux, etc.). N’hésitez pas à utiliser `docker --help` ou la documentation en ligne pour approfondir chaque commande.

## 4. Dockerfile et construction d’images

Jusqu’à présent, nous avons utilisé des images existantes (issues de Docker Hub). L’un des grands pouvoirs de Docker est de permettre de **construire vos propres images** pour y empaqueter *votre* application. Pour cela, on écrit un fichier texte appelé **Dockerfile** qui contient les instructions de construction de l’image. Dans cette section, nous allons découvrir la syntaxe d’un Dockerfile, construire une image personnalisée, et aborder les bonnes pratiques de création d’images.

### 4.1 Syntaxe et instructions d’un Dockerfile

Un **Dockerfile** est un simple fichier texte (généralement nommé "Dockerfile" sans extension) qui définit pas à pas comment construire une image. Chaque ligne du Dockerfile est une **instruction** qui correspond à une action (par exemple installer un package, copier des fichiers, définir une variable d’environnement, etc.). Docker va lire ces instructions et les exécuter successivement pour produire l’image finale.

Voici les instructions les plus courantes dans un Dockerfile et leur rôle :

| **Instruction**  | **Description**                                                    | **Exemple**                        |
|------------------|--------------------------------------------------------------------|------------------------------------|
| `FROM`           | Spécifie l’image de base à partir de laquelle on construit. C’est la première ligne obligatoire de tout Dockerfile. | `FROM python:3.11-slim` (base Debian avec Python 3.11) |
| `RUN`            | Exécute une commande durant la construction de l’image. Chaque `RUN` crée une nouvelle couche dans l’image. Utilisé typiquement pour installer des paquets ou configurer le système. | `RUN apt-get update && apt-get install -y curl` |
| `COPY`           | Copie des fichiers ou dossiers du *contexte de construction* (votre machine hôte) vers le système de fichiers de l’image. | `COPY src/ /app/src/` (copie le dossier src local vers /app/src dans l’image) |
| `ADD`            | Similaire à COPY (copie fichiers locaux ou URL). Moins utilisé, sauf si besoin d’extraire une archive (ADD sait dézipper les *.tar*). | `ADD app.tar.gz /app/` |
| `WORKDIR`        | Définit le répertoire de travail courant pour les instructions suivantes et pour le conteneur final. (Equivalent à un `cd` persistent). | `WORKDIR /app` |
| `ENV`            | Définit une variable d’environnement dans l’image. Utile pour configurer l’application ou indiquer des chemins. | `ENV NODE_ENV=production` |
| `EXPOSE`         | Documente le port sur lequel l’application écoute. **Note :** C’est indicatif, cela **n’ouvre pas** le port sur l’hôte. (Pour rendre le service accessible, on utilise `-p` à l’exécution du conteneur). | `EXPOSE 8080` |
| `CMD`            | Spécifie la commande par défaut à exécuter lorsque le conteneur est lancé. C’est le *point d’entrée* de votre application. Si on passe des arguments à `docker run`, ils viendront surcharger le CMD. | `CMD ["python", "app.py"]` |
| `ENTRYPOINT`     | Définis le processus principal du conteneur, de manière impérative. Combiné avec CMD (qui peut fournir des arguments par défaut). En général on utilise soit ENTRYPOINT soit CMD pour lancer l’appli. | `ENTRYPOINT ["npm", "start"]` |

En plus de ces instructions, il en existe d’autres (comme `LABEL` pour ajouter des métadonnées, `ARG` pour les variables de build, `USER` pour changer l’utilisateur d’exécution, etc.), mais les listées ci-dessus sont suffisantes pour débuter.

Lorsqu’on exécute `docker build` pour construire l’image, Docker lit le Dockerfile et traite chaque instruction dans l’ordre. Chaque instruction (FROM, RUN, COPY, etc.) crée une **couche** de l’image. Docker va mettre en cache ces couches pour accélérer les reconstructions futures : si le Dockerfile n’a pas changé à un certain stade, Docker peut réutiliser la couche existante au lieu de la reconstruire. **Important :** l’ordre des instructions impacte le cache. Il est courant d’ordonner le Dockerfile du général au particulier afin de maximiser la réutilisation du cache (voir bonnes pratiques plus bas).

Pour illustrer, écrivons un Dockerfile simple pour une application Python :

```dockerfile
# Utiliser l'image de base Python officielle (version 3.11 slim)
FROM python:3.11-slim

# Définir le dossier de travail à /app
WORKDIR /app

# Copier le fichier de dépendances et installer les dépendances
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier le reste du code de l'application
COPY . .

# Exposer le port de l'application (exemple: une app web sur le port 5000)
EXPOSE 5000

# Lancer l'application
CMD ["python", "app.py"]
```

Analysons ce Dockerfile :
- On part d’une image de base légère (`python:3.11-slim`) contenant Python 3.11 sur un OS minimal.
- On se place dans le répertoire `/app` dans l’image.
- On copie le fichier `requirements.txt` (qui liste les paquets Python nécessaires) puis on exécute `pip install` pour installer ces dépendances. En séparant COPY et RUN de cette manière, on optimise le cache : si seul le code de l’appli change mais pas les dépendances, Docker pourra re-utiliser la couche d’installation des requirements.
- On copie ensuite tout le reste du projet dans l’image (`COPY . .`).
- On documente que l’application écoute sur le port 5000.
- Enfin, on définit la commande de lancement : ici, exécuter `python app.py`. Ainsi, quand on fera `docker run` sur l’image résultante, le conteneur démarrera notre application Python automatiquement.

### 4.2 Construction de l’image Docker

Avec notre Dockerfile en place, construisons l’image. Assurez-vous d’être dans le répertoire où se trouve le Dockerfile (et les fichiers de l’application). Puis lancez la commande de build :

```bash
docker build -t monapp:1.0 .
```

Ici, `-t monapp:1.0` assigne un *tag* à l’image (nom de l’image = "monapp", tag = "1.0"). Le `.` final indique que le *contexte de build* est le répertoire courant (Docker va envoyer ce dossier au démon Docker pour qu’il accède aux fichiers à copier). Docker va alors exécuter chaque instruction :
- Télécharger l’image de base python:3.11-slim (si pas déjà en cache local).
- Exécuter les commandes RUN (mise à jour pip, installation des dépendances).
- etc.

Vous verrez dans la console la progression, étape par étape. Si tout se passe bien, Docker conclura par un message du type *Successfully built <image-id>* et *Successfully tagged monapp:1.0*.

Notre image `monapp:1.0` est maintenant construite. On peut la lister avec `docker images` (elle apparaîtra avec le nom et tag spécifiés). Testons-la en lançant un conteneur :

```bash
docker run -d -p 5000:5000 monapp:1.0
```

Cette commande exécute notre application Python en détaché. Supposons que c’est une petite API web Flask écoutant sur le port 5000 ; grâce au mapping `-p 5000:5000`, elle est accessible via `http://localhost:5000`. Si besoin, on consulte les logs (`docker logs <container_id>`) pour vérifier que tout se passe bien. Notre image personnalisée fonctionne !

**Gestion des images** : Vous pouvez retagger ou pousser cette image vers un registre. Par exemple, pour envoyer `monapp:1.0` sur Docker Hub, il faudrait la taguer en `docker tag monapp:1.0 monDockerHubUtilisateur/monapp:1.0` puis exécuter `docker push monDockerHubUtilisateur/monapp:1.0` (après s’être authentifié via `docker login`). Nous reviendrons sur l’automatisation de ces étapes dans la section CI/CD.

Un aspect fondamental à comprendre est la notion de *couches*. Chaque commande du Dockerfile a créé une couche dans l’image. Docker réutilise ces couches lors de constructions ultérieures pour éviter de tout refaire à zér ([Docker, c'est quoi ?](https://www.redhat.com/fr/topics/containers/what-is-docker#:~:text=,version%20des%20images))】. Par exemple, si vous modifiez juste le code applicatif mais pas le fichier requirements.txt, Docker reprendra le cache jusqu’à l’étape d’installation des dépendances, puis ne reconstruira que la copie du code et la couche finale. Cela accélère énormément les itérations.

### 4.3 Bonnes pratiques pour les Dockerfile

Lors de la création d’images Docker, quelques bonnes pratiques permettent d’obtenir des images plus petites, plus efficaces et plus sûres :

- **Minimiser la taille des images** : Utilisez des images de base légères (*slim*, *alpine* etc. lorsqu’elles existent). Évitez d’installer des packages inutiles. Nettoyez le cache des gestionnaires de paquets (par ex. ajouter `rm -rf /var/lib/apt/lists/*` après un `apt-get install` dans le même `RUN`) pour réduire la taille des couches. Des images plus petites se déploient plus vite et ont une surface d’attaque réduite.
- **Tirer parti du cache** : Organisez les instructions du Dockerfile de façon logique pour maximiser la réutilisation du cache. Par exemple, placez les instructions qui changent le moins (installation de dépendances système, etc.) au début, et les parties qui changent fréquemment (copie du code source de l’application) vers la fin. Ainsi, vous ne refaites pas les étapes lourdes à chaque modification mineure du code.
- **Utiliser un fichier .dockerignore** : Créez un fichier `.dockerignore` pour exclure du contexte de build les fichiers qui ne sont pas nécessaires à l’image (ex: fichiers temporaires, `.git`, documentation, etc.). Cela accélère la construction et évite d’embarquer des fichiers inutiles dans l’image.
- **Un seul processus par conteneur** : Par convention, chaque conteneur Docker ne doit exécuter qu’un seul processus principal. Par exemple, ne lancez pas à la fois une base de données et un serveur web dans le même conteneur – préférez deux conteneurs séparés. Docker n’est pas une machine virtuelle générale, mais une sandbox pour une application unique (on peut tout de même avoir des processus auxiliaires si besoin, mais l’idée est de découper en micro-services).
- **Éviter d’exécuter en root** : Par défaut, un conteneur tourne en tant qu’utilisateur root (superutilisateur) à l’intérieur. Cela peut poser des problèmes de sécurité si quelqu’un parvient à s’échapper du conteneur. Quand c’est possible, créez un utilisateur dédié dans l’image (`RUN adduser ...` puis `USER <nom>` dans le Dockerfile) pour exécuter l’application avec moins de privilèges. De nombreuses images officielles (ex: Node, Nginx) proposent déjà un utilisateur non-root par défaut pour l’exécution.
- **Tenir compte du réseau et du stockage** : Documentez avec `EXPOSE` les ports utilisés par votre application dans le Dockerfile (cela aide les autres à comprendre comment l’utiliser, même si ce n’est pas obligatoire). Idem, si votre application doit stocker des données persistantes, envisagez d’utiliser l’instruction `VOLUME` pour indiquer quel chemin devra être monté en volume lors de l’exécution du conteneur. (Nous verrons les volumes au chapitre suivant.)

En suivant ces conseils, vos images seront plus faciles à maintenir et à déployer. Vous trouverez sur le web (docs Docker, blogs) des *Dockerfile best practices* plus détaillées, mais ces bases vous permettront d’éviter les écueils classiques (images trop lourdes, builds lents, failles de sécurité basiques).

## 5. Gestion des volumes et des réseaux

Lorsque vous lancez des conteneurs, deux aspects importants entrent en jeu : la **persistance des données** (les volumes) et la **communication réseau** entre conteneurs ou avec l’extérieur. Par défaut, un conteneur Docker est éphémère et relativement isolé sur le plan réseau. Voyons comment conserver des données au-delà du cycle de vie d’un conteneur grâce aux volumes, puis comment fonctionnent les réseaux Docker.

### 5.1 Les volumes : persistance des données

Par design, les données écrites à l’intérieur d’un conteneur (dans son système de fichiers isolé) disparaissent lorsque le conteneur est supprimé. Docker propose les **volumes** pour sauvegarder des données de manière persistante, indépendamment du cycle de vie des conteneurs. Un volume est une zone de stockage gérée par Docker, généralement stockée sur l’hôte, que l’on peut monter dans un ou plusieurs conteneurs.

**Pourquoi des volumes ?** Prenons l’exemple d’une base de données dans un conteneur : sans volume, toutes les données seraient perdues à l’arrêt/suppression du conteneur (ou lors d’une mise à jour de l’image). En utilisant un volume, on attache un dossier persistant à l’emplacement où la base stocke ses fichiers, ce qui permet de conserver les données même si le conteneur est recréé ou mis à jour.

Il existe principalement deux types de volumes/montages avec Docker :
- **Volumes nommés (managed volumes)** – Stockage géré par Docker, dans un emplacement interne (par défaut sous `/var/lib/docker/volumes/`). On les crée via Docker (`docker volume create`) ou automatiquement au `docker run`. Ils sont identifiés par un nom attribué. Exemple : `docker run -d -v monvolume:/var/lib/mysql mysql:8` va créer (si inexistant) un volume nommé *monvolume* et le monter dans le conteneur à l’emplacement `/var/lib/mysql`. Si vous supprimez le conteneur, le volume *monvolume* existe toujours et pourra être remonté sur un autre conteneur pour récupérer les données.
- **Bind mounts (montages de répertoire)** – Montage direct d’un répertoire du système hôte dans le conteneur. On fournit un chemin absolu de l’hôte. Exemple : `docker run -d -v /home/user/backup:/backup alpine tar czf /backup/etc.tar.gz /etc`. Ici, on monte le dossier `/home/user/backup` du host dans le conteneur comme `/backup`. Le conteneur (une Alpine Linux) crée une archive de /etc et la place dans /backup, qui en réalité est stocké sur l’hôte. Les bind mounts permettent donc un contrôle exact de l’emplacement des données sur l’hôte. Ils sont souvent utilisés en développement pour monter le code source local dans le conteneur (ainsi l’application voit les modifications de code en temps réel), ou pour accéder à des fichiers spécifiques du host.

En résumé, utilisez de préférence des **volumes nommés** pour la persistance applicative (base de données, fichiers import/uploads, etc.), car Docker les gère pour vous (pas besoin de connaître le chemin exact sur l’hôte, ce qui améliore la portabilité). Les **bind mounts** sont utiles pour des cas où vous avez besoin de contrôler précisément le chemin hôte ou de partager des fichiers spécifiques entre host et conteneur.

Voyons quelques commandes liées aux volumes :
- `docker volume create <nom>` crée un volume persistant vide.
- `docker volume ls` liste les volumes Docker existants.
- `docker volume inspect <nom>` donne des infos (notamment le chemin sur l’hôte où sont stockées les données du volume).
- `docker volume rm <nom>` supprime un volume (attention, cela efface les données – Docker n’autorise pas la suppression d’un volume s’il est utilisé par un conteneur actif).

**Exemple d’utilisation de volume :** Supposons que nous déployons MySQL via Docker. Pour que la base sauvegarde ses données hors du conteneur, on peut lancer:
```bash
docker volume create db_data        # créer un volume pour la base
docker run -d -v db_data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=secret mysql:8
``` 
Ici on a spécifiquement monté le volume `db_data` sur `/var/lib/mysql` (dossier où MySQL stocke ses bases). On a également passé une variable d’env pour le mot de passe root (juste pour que MySQL se lance). Ainsi, même si ce conteneur MySQL s’arrête ou est supprimé, les données resteront dans `db_data`. On pourrait lancer une nouvelle version de MySQL et remonter `db_data` pour récupérer immédiatement l’état précédent de la base.

**Partage de volumes entre conteneurs :** Plusieurs conteneurs peuvent accéder au même volume (typique par ex. si vous avez un conteneur d’application et un conteneur de backup qui doit lire les mêmes fichiers). Il faut toutefois faire attention aux accès concurrents. Docker ne verrouille pas les volumes – c’est à vous de s’assurer que c’est safe (par ex. un conteneur en lecture seule).

**Écriture sur volume vs couche conteneur :** Notez que si un fichier est modifié à l’intérieur d’un conteneur :
- S’il fait partie d’un volume monté, la modification impacte directement le volume (persistant).
- S’il fait partie de l’image (pas dans un volume), la modification est faite dans la couche *conteneur* (copy-on-write). Ces changements-là sont perdus quand le conteneur est supprimé. On évite généralement de s’appuyer là-dessus pour du stockage applicatif.

### 5.2 Les réseaux Docker

Par défaut, Docker isole aussi le réseau des conteneurs : chaque conteneur a sa propre pile réseau et ne voit pas directement les autres. Comprendre le fonctionnement réseau de Docker est crucial pour faire communiquer des conteneurs entre eux ou exposer des services à l’extérieur.

**Réseau *bridge* par défaut :** Lorsque vous installez Docker, un réseau *bridge* nommé `bridge` est créé automatiquement. Si vous lancez un conteneur sans préciser de réseau, il est attaché à ce réseau par défaut. Le réseau bridge agit comme un sous-réseau virtuel interne à la machine Docker :
- Les conteneurs sur ce réseau peuvent communiquer entre eux **par IP** (Docker leur attribue une IP locale, ex: 172.17.0.X). Cependant, ils ne connaissent pas automatiquement les noms des autres conteneurs. Sur le réseau par défaut, il n’y a pas de DNS conteneur -> conteneur.
- Les conteneurs peuvent accéder à Internet (par NAT) via le réseau du host. En revanche, de l’extérieur on ne peut pas atteindre un port d’un conteneur sans un *port mapping* explicite (`-p host_port:container_port` lors du run).
- Le host (votre machine) peut contacter un conteneur sur le bridge via son IP docker interne, mais c’est peu pratique (on privilégie le port mapping ou l’utilisation de `docker exec` pour communiquer).

**Réseaux *bridge* personnalisés :** Docker permet de créer vos propres réseaux virtuels isolés. Par exemple, si vous faites :
```bash
docker network create monreseau
```
vous obtenez un nouveau réseau de type bridge nommé *monreseau*. Les conteneurs que vous lancerez avec `--network monreseau` seront connectés ensemble sur ce réseau. L’avantage principal d’un réseau personnalisé est que Docker configure un **serveur DNS interne** pour ce réseau : ainsi, les conteneurs peuvent se résoudre par nom d’hôte. Concrètement, si vous lancez deux conteneurs sur *monreseau*, l’un nommé `web` et l’autre `db`, alors dans le conteneur `web`, le nom d’hôte `db` résoudra automatiquement vers l’IP du conteneur `db`. Pas besoin de connaître les adresses IP. Ceci simplifie grandement la communication dans des architectures multi-conteneurs (et c’est ce que fait Docker Compose automatiquement, nous y viendrons).

Pour attacher un conteneur à un réseau existant, utilisez `--network` à la création. Exemple :
```bash
docker run -d --name web --network monreseau nginx
docker run -d --name db --network monreseau mysql:8
```
Ici, `web` et `db` sont sur le même réseau isolé *monreseau*. Le conteneur `web` peut contacter `db` en utilisant l’adresse `db:3306` (3306 étant le port MySQL standard). Ce genre de réseau est isolé du réseau par défaut et des autres réseaux Docker, ce qui offre une bonne étanchéité entre différentes applications sur une même machine.

**Autres types de réseau :** Docker propose deux autres drivers de réseau principaux :
- **host** – En mode host, un conteneur partage directement la pile réseau de l’hôte, il n’y a pas d’isolation réseau. Le conteneur n’a pas sa propre IP : il utilise celle du host. Par exemple, si on lance `docker run --network host -p 8080:80 nginx`, le `-p` n’a plus lieu d’être car le conteneur *est* déjà sur le host : Nginx écoutera directement sur le port 80 du host. Le mode host peut améliorer la performance réseau (pas de NAT) et est utile pour des conteneurs qui doivent accéder à des services sur localhost (host) ou diffuser en réseau local. Par contre, c’est moins isolé (ports conteneur = ports host, donc risques de conflits).
- **none** – C’est l’inverse : pas de réseau du tout. Le conteneur n’a aucune interface réseau (à part *lo* interne). Il ne peut pas communiquer, ni être contacté. Ce mode ultra-isolé sert pour des cas très spécifiques (par exemple des tests de sécurité, ou forcer qu’une appli ne fasse aucune communication).

**Résumé des modes réseau :**

- **Bridge par défaut** : isolation modérée, communication conteneur->conteneur par IP, nécessite des mapping de ports pour l’accès externe. Convenable pour débuter ou conteneurs isolés.
- **Bridge personnalisé** : isolation entre applications, mais conteneurs sur un même réseau peuvent se joindre par nom. Recommandé pour les applications multi-conteneurs (et c’est ce qu’utilise Compose).
- **Host** : conteneur fusionné avec le réseau de l’hôte. Utile pour besoins particuliers (performance, accès local), à utiliser prudemment.
- **None** : pas de réseau, cas extrêmes.

**Exposer un port :** Comme vu précédemment, pour rendre un service conteneur accessible depuis l’hôte (ou l’extérieur), il faut publier son port via `-p`. Par exemple, `-p 8080:80` expose sur le port 8080 de toutes les interfaces de l’hôte. Vous pouvez restreindre à une IP spécifique de l’hôte en préfixant (ex: `-p 127.0.0.1:8080:80` écoutera uniquement en localhost). Sans mapping, un conteneur web dans Docker ne sera pas visible depuis l’extérieur.

**Connexion de conteneurs entre plusieurs hôtes :** Le Docker de base ne connecte pas des conteneurs sur des machines différentes. Pour cela, Docker propose un driver de réseau *overlay* utilisable avec Docker Swarm (le mode cluster natif de Docker) – cela dépasse notre scope ici. En général, pour un réseau multi-hôtes, on utilise une surcouche d’orchestration comme Kubernetes ou Docker Swarm qui se charge de créer un réseau distribué.

En pratique, si vous utilisez **Docker Compose** (chapitre suivant), celui-ci crée automatiquement un réseau dédié pour vos conteneurs du compose, ce qui leur permet de se découvrir par nom de service. Cela facilite la vie : plus besoin de créer manuellement le réseau ou de l’indiquer dans chaque commande `docker run`. Nous allons voir cela immédiatement avec Compose.

## 6. Docker Compose

Gérer manuellement plusieurs conteneurs avec les commandes Docker de base peut devenir fastidieux, surtout lorsqu’il faut se souvenir de lancer X conteneurs avec les bons paramètres dans le bon ordre. **Docker Compose** est un outil qui simplifie le déploiement de multi-conteneurs définis déclarativement dans un fichier YAML. Il permet, avec une seule commande, de lancer (ou arrêter) tout un ensemble de conteneurs qui forment une application.

### 6.1 Présentation de Docker Compose

Docker Compose utilise un fichier typiquement nommé `docker-compose.yml` où vous décrivez les services (conteneurs) composant votre application, ainsi que leurs configurations :
images à utiliser (ou Dockerfile à construire), ports exposés, volumes montés, variables d’environnement, dépendances entre services, réseaux, etc. Ensuite, la commande `docker-compose up` (ou la nouvelle syntaxe `docker compose up`) va automatiquement créer tous les conteneurs définis et les configurer selon le YAML.

Compose est très pratique en développement et test, car il permet de reproduire une architecture (ex: une app web + une base de données + un cache) sur une seule machine de façon cohérente. En production, on utilisera plutôt Kubernetes ou Swarm, mais Compose reste utile pour orchestrer des conteneurs sur un seul hôte ou pour les pipelines CI.

Quelques bénéfices de Compose :
- **Lancement unifié** : un simple `docker-compose up -d` peut lancer une base de données, un backend API et un frontend, reliés et configurés.
- **Réseau automatique** : comme mentionné, Compose crée un réseau bridge spécifique sur lequel il connecte tous les services, avec résolution DNS par nom de service.
- **Variables d’environnement** : on peut utiliser un fichier `.env` ou passer des env au conteneur facilement via le YAML.
- **Orchestration simple** : Compose assure de lancer d’abord les conteneurs dont d’autres dépendent (grâce à l’instruction `depends_on`). Il permet aussi de reconstruire des images (`docker-compose build`) et de les lancer, de surveiller les logs de l’ensemble (`docker-compose logs`), etc.

### 6.2 Syntaxe de docker-compose.yml

Le format du fichier Compose est en YAML. Voici les éléments principaux :
- `version` : la version du format Compose (par ex. "3.8"). Les versions 3.x sont les plus courantes avec Docker >= 20.
- `services` : la liste des services (chaque service correspondra à un conteneur, ou à un ensemble de conteneurs identiques si on scale).
- Pour chaque service :
  - soit un champ `image: nom_image:tag` pour indiquer quelle image utiliser,
  - soit un bloc `build:` si on veut construire l’image à partir d’un Dockerfile (on peut mettre `build: .` pour construire depuis le Dockerfile du dossier courant).
  - des `ports:` à publier (format `"hôte:conteneur"` comme en ligne de commande),
  - des `environment:` pour les variables d’env (liste ou dict YAML),
  - des `volumes:` pour monter des volumes ou bind mounts,
  - un `depends_on:` listant les autres services du compose qui doivent démarrer avant celui-ci.
  - éventuellement `networks:` si on a plusieurs réseaux personnalisés, ou `restart:` pour définir une politique de redémarrage automatique (ex: always).

- On peut également définir des `volumes:` (nommés) au niveau top-level du fichier, que les services utiliseront, ainsi que des `networks:` si besoin de réseaux spécifiques. Par défaut, si on ne définit rien, Compose crée un réseau implicite du nom du projet, et les volumes nommés déclarés dans services seront aussi créés automatiquement.

Pour illustrer, écrivons un exemple concret de `docker-compose.yml`. Imaginons que l’on souhaite déployer une application WordPress avec une base de données MySQL. Nous aurons deux services : *wordpress* (le serveur web+php) et *db* (MySQL). Nous voulons persister les données de la base dans un volume. Voici à quoi pourrait ressembler le fichier Compose :

```yaml
services:
  db:
    image: mysql:5.7
    restart: always
    environment:
      - MYSQL_ROOT_PASSWORD=exemple
      - MYSQL_DATABASE=wordpress
    volumes:
      - db_data:/var/lib/mysql

  wordpress:
    image: wordpress:latest
    restart: always
    ports:
      - "8080:80"
    environment:
      - WORDPRESS_DB_HOST=db:3306
      - WORDPRESS_DB_PASSWORD=exemple
      - WORDPRESS_DB_NAME=wordpress
    depends_on:
      - db

volumes:
  db_data:
```

Analysons les points clés de ce fichier :

- Nous utilisons deux images officielles : **mysql:5.7** pour la base, **wordpress:latest** pour l’application PHP.
- Chaque service a une politique `restart: always` : cela indique à Docker de toujours redémarrer le conteneur en cas d’arrêt (ou au démarrage du Docker daemon). C’est une bonne pratique en production pour les conteneurs critiques.
- Le service **db** reçoit des variables d’environnement :
  - `MYSQL_ROOT_PASSWORD` pour définir le mot de passe root de MySQL,
  - `MYSQL_DATABASE` pour créer une base nommée *wordpress* d’entrée de jeu.
- On monte un volume nommé `db_data` sur `/var/lib/mysql` afin de conserver les données de la base MySQL.
- Le service **wordpress** publie le port 80 du conteneur sur le port 8080 de l’hôte (on pourra accéder au site sur http://localhost:8080).
- WordPress a besoin de se connecter à la base de données. On lui fournit:
  - `WORDPRESS_DB_HOST=db:3306` : l’adresse du serveur MySQL. Ici on utilise le nom de service `db` qui sera résolu automatiquement grâce au réseau Compose, et le port standard 3306.
  - `WORDPRESS_DB_PASSWORD=exemple` et `WORDPRESS_DB_NAME=wordpress` pour qu’il puisse se connecter avec l’utilisateur root et la base configurée.
- `depends_on: db` indique que le conteneur *wordpress* ne sera démarré qu’après le lancement du conteneur *db*. (Ça ne signifie pas que MySQL sera prêt instantanément, mais au moins l’ordre est respecté.)
- En bas, on déclare le volume `db_data` afin que Compose le crée (s’il n’existe pas déjà). Ainsi, la première exécution va créer un volume persistant, et les suivantes réutiliseront le même.

**Démarrer l’application avec Compose :** placez ce YAML dans un fichier `docker-compose.yml`. Dans le même dossier, exécutez la commande :
```bash
docker-compose up -d
``` 
*(Ou `docker compose up -d` selon votre version, les deux syntaxes fonctionnent.)* 

Compose va alors :
- Créer le réseau `monDossier_default` (si non existant) et le volume `db_data`.
- Lancer le conteneur **db** (MySQL), puis le conteneur **wordpress**.
- Les deux conteneurs seront connectés au réseau commun, et pourront communiquer (WordPress -> MySQL).
- Vous pouvez surveiller le démarrage avec `docker-compose logs -f` pour voir, par exemple, MySQL initialiser sa base puis WordPress se connecter.

Après quelques secondes, en visitant `http://localhost:8080`, vous devriez voir l’écran d’installation de WordPress 🎉. Tout cela a été réalisé avec un unique fichier de configuration et une commande – plutôt que de lancer manuellement 2 conteneurs avec une panoplie de paramètres.

**Utilisation au quotidien :** 
- `docker-compose ps` liste les conteneurs gérés par le compose en cours (dans le dossier courant).
- `docker-compose down` arrête et supprime les conteneurs (ainsi que les réseaux associés). Les volumes persistants, eux, ne sont pas supprimés par défaut (ce qui est bien pour ne pas perdre les données).
- Si vous modifiez le fichier compose (par ex, changer une variable d’env ou la version d’une image), il suffit de re-exécuter `docker-compose up -d` pour appliquer les changements (Compose fera les mises à jour nécessaires, recréera les conteneurs concernés).
- `docker-compose build` permet de construire les images si vous avez des services avec un contexte de build (Dockerfile). Sinon, Compose va toujours chercher les images sur Docker Hub automatiquement.

Docker Compose est un outil précieux pour tester des configurations complexes sur votre machine ou pour déployer des stacks simples sur un serveur unique. Il est également très utilisé dans les scénarios de développement, pour lancer rapidement l’environnement complet (ex: lancer à la fois votre API, la base de données et Redis en une commande). Nous verrons dans l’étude de cas finale comment l’utiliser dans un workflow de projet.

## 7. Déploiement en production sur un VPS Linux

Lorsque vous passez en **production** (par exemple déployer vos conteneurs sur un serveur cloud ou un VPS), de nouvelles considérations entrent en jeu : il faut sécuriser les déploiements, assurer la haute disponibilité, gérer les mises à jour sans coupure, collecter les logs et monitorer les conteneurs en service. Dans cette section, nous allons présenter des bonnes pratiques pour déployer Docker en production sur un serveur Linux, en couvrant la sécurisation, l’opérationnel et la supervision.

### 7.1 Sécurisation des conteneurs

Bien que Docker offre une isolation, en production il est crucial de renforcer la sécurité :

- **Utiliser des images fiables et mises à jour** : Ne téléchargez des images qu’à partir de sources de confiance (Docker Official Images, éditeurs reconnus, ou vos propres images construites). Mettez à jour régulièrement vos images pour intégrer les derniers patchs de sécurité. Par exemple, si une faille est découverte dans PHP, assurez-vous de récupérer une image mise à jour dès que possible.
- **Principe de moindre privilège** : Faites tourner vos conteneurs avec le moins de privilèges possible. Comme mentionné, évitez de lancer vos processus applicatifs en root à l’intérieur du conteneur. De plus, Docker permet d’ajouter des options de sécurité lors du `docker run` – par ex : `--read-only` (monter le système de fichiers conteneur en lecture seule), `--cap-drop` (retirer des *capabilities* Linux du conteneur pour limiter ce qu’il peut faire), `--security-opt no-new-privileges` (empêcher l’escalade de privilèges). Ces options renforcent l’isolation.
- **Limiter l’exposition réseau** : N’exposez que les ports nécessaires. Si un conteneur n’a pas vocation à être accessible directement depuis Internet, ne faites pas de `-p` vers l’hôte. Laissez-le dans le réseau interne Docker, et faites passer les communications via un proxy ou un service dédié. Par exemple, en production on utilise souvent un **reverse proxy** (Nginx, Traefik) unique exposé sur le port 80/443, qui redirige les requêtes vers les conteneurs webs en interne – cela évite d’exposer chaque conteneur web individuellement.
- **Pare-feu au niveau de l’hôte** : Configurez un firewall (iptables, UFW, etc.) sur votre serveur Docker pour filtrer les ports. Par défaut Docker ouvre les ports mappés sur toutes les interfaces. Avec un pare-feu, vous pouvez restreindre l’accès à certains services à une IP de confiance ou à un réseau interne.
- **Docker daemon** : Protégez l’accès au socket Docker (`/var/run/docker.sock`). Ce socket donne un contrôle total sur Docker (et donc sur la machine). Par défaut, seul root (ou le groupe docker) y a accès – ne mettez que des utilisateurs de confiance dans le groupe docker. N’exposez surtout pas l’API Docker en TCP sans des mesures de sécurités robustes (certificats TLS client/serveur) – sinon un attaquant pourrait prendre le contrôle de votre hôte via Docker.
- **Scanning de vulnérabilités** : Envisagez d’utiliser des outils d’analyse d’images (Docker fournit `docker scan`, basé sur Snyk, pour détecter les vulnérabilités connues dans les images). Cela vous aide à identifier des dépendances ou packages à risque dans vos images, afin de les mettre à jour.
- **Secrets** : Ne stockez pas de secrets (mots de passe, clés privées) en clair dans vos images ou variables d’environnement. Préférez les injecter au runtime via des fichiers montés (volumes) ou utilisez des solutions de gestion de secrets intégrées (Docker Swarm et Kubernetes ont des objets *secrets* spécialisés pour cela). Au minimum, si vous devez passer un secret en variable, utilisez par exemple un fichier `.env` non versionné lu par Compose, plutôt que de le commit dans un repo.

En suivant ces précautions, vous réduisez considérablement la surface d’attaque de vos conteneurs. Docker, bien configuré, peut offrir une isolation proche de celle de VMs traditionnell ([Docker, c'est quoi ?](https://www.redhat.com/fr/topics/containers/what-is-docker#:~:text=une%20br%C3%A8che%20de%20s%C3%A9curit%C3%A9,mieux%20isol%C3%A9es%20du%20syst%C3%A8me%20h%C3%B4te))4】, mais cela requiert de respecter ces bonnes pratiques de durcissement.

### 7.2 Bonnes pratiques de déploiement

Au-delà de la sécurité, voici d’autres conseils pour opérer vos conteneurs en production de manière fiable :

- **Utiliser des orchestrateurs ou outils de gestion** : Sur un simple VPS, Docker Compose peut très bien gérer le démarrage de vos conteneurs. Mais pour plusieurs serveurs ou des besoins de scaling auto, envisagez un orchestrateur comme Kubernetes (voir chapitre 9) ou Docker Swarm. Ils apportent des fonctionnalités de tolérance aux pannes et de déploiements progressifs. Même sur un seul nœud, des outils comme **Portainer** (interface web de gestion Docker) peuvent vous aider à visualiser et administrer vos conteneurs.
- **Politique de redémarrage** : Mettez `--restart=always` (ou dans Compose, `restart: always`) pour les conteneurs critiques afin qu’ils redémarrent automatiquement en cas de crash ou au reboot du serveur Docker. Ainsi, si votre VPS redémarre, vos services Docker se relanceront d’eux-mêmes.
- **Limitation des ressources** : En production, évitez qu’un conteneur monopolise toute la machine. Utilisez les options `--memory`, `--cpus` pour limiter la RAM et CPU utilisables par conteneur. Par exemple `--memory=512m` pour contraindre à 512 Mo. Ceci évitera qu’un bug ou une charge soudaine saturent l’hôte et impactent les autres services.
- **Surveillance de la santé (healthchecks)** : Vous pouvez définir des commandes de **healthcheck** dans le Dockerfile (instruction HEALTHCHECK) pour que Docker surveille l’application à l’intérieur du conteneur (par ex. ping d’une URL de santé). Compose/Kubernetes peuvent utiliser ces healthchecks pour redémarrer un conteneur qui ne répond plus correctement. C’est utile pour détecter automatiquement un service bloqué.
- **Gestion des configs** : Pour vos applications, utilisez des variables d’environnement ou des fichiers de configuration externes (montés en volume) pour adapter l’application à l’environnement (dev, prod). Ainsi, vous n’avez pas besoin de reconstruire une image pour changer une URL de base de données ou un niveau de log – il suffit de changer la variable au déploiement.
- **Mises à jour sans coupure** : Étudiez des stratégies de déploiement *rolling*. Par exemple, sur Kubernetes, un Deployment permet de faire un *rolling update* (on lance la nouvelle version et on arrête progressivement l’ancienne). Sur un single VPS sans orchestrateur, vous pourriez utiliser Compose en combinant des techniques comme déployer une nouvelle instance et basculer un proxy. L’idée est d’éviter l’indisponibilité : ne pas stopper tous les conteneurs avant d’avoir les nouveaux prêts. Cela peut nécessiter une infrastructure un peu plus complexe (load balancer, etc.), mais c’est un objectif à viser pour des services en production critiques.
- **Sauvegardes** : N’oubliez pas que si vous stockez des données dans des volumes Docker (ex: base de données), il faut les sauvegarder régulièrement. Docker ne s’en occupe pas. Vous pouvez soit faire des backups depuis l’application (ex: dump SQL régulier), soit monter vos volumes de données sur l’hôte et inclure ces dossiers dans vos procédures de sauvegarde du serveur.
- **Isolation par projet** : Si plusieurs applications tournent sur le même serveur Docker, isolez-les dans des networks distincts et utilisez des préfixes/nommage clairs pour les conteneurs, images et volumes (Compose le fait par projet). Évitez que deux projets utilisent un même nom de conteneur ou volume par inadvertance.

En appliquant ces bonnes pratiques, vous rendez votre déploiement Docker plus robuste et plus facile à maintenir sur le long terme.

### 7.3 Logs et monitoring des conteneurs

En production, pouvoir consulter les **logs** de vos applications et surveiller leur **métriques** (CPU, RAM, etc.) est indispensable pour détecter les anomalies et diagnostiquer les problèmes.

**Gestion des logs :** Par défaut, Docker stocke les sorties standard (stdout/stderr) de chaque conteneur dans un fichier JSON (par conteneur) sous `/var/lib/docker/containers/<id>/<id>-json.log`. C’est ce que `docker logs` affiche. Sur un serveur, ces fichiers peuvent grossir indéfiniment si l’application est verbeuse. Pensez à configurer une **rotation des logs**. Docker permet via son démon d’utiliser des drivers de logs (ex: `json-file` avec options de rotation, ou `syslog`, `journald`, etc.). Vous pouvez, dans `/etc/docker/daemon.json`, définir par exemple :
```json
{"log-driver": "json-file", "log-opts": {"max-size": "10m", "max-file": "3"}}
``` 
pour limiter chaque log de conteneur à 10 Mo et garder 3 fichiers (rotation). Ainsi, pas de disque saturé.

Pour une approche plus centralisée : envisagez d’utiliser un système de collecte de logs :
- *Solution ELK (Elasticsearch + Logstash + Kibana)* ou sa variante légère EFK (Elasticsearch/Fluentd/Kibana) : vous pouvez déployer un agent (Logstash/Fluentd) sur l’hôte Docker qui capte les logs des conteneurs (via le socket ou en lisant les fichiers) et les envoie vers une base centralisée (Elasticsearch) où vous pouvez les analyser avec Kibana.
- Des services cloud existent également (Datadog, Splunk, etc.) ou des solutions comme Grafana Loki.

L’important est de ne pas perdre les logs et de pouvoir y accéder même si un conteneur est mort ou a été recréé. Au minimum, assurez-vous de sauvegarder les logs applicatifs critiques en dehors du conteneur (par ex, montés sur un volume host, ou redirigés vers syslog host).

**Monitoring des conteneurs :** Docker fournit la commande `docker stats` pour voir en temps réel la consommation CPU, mémoire, E/S de vos conteneurs. En production automatisée, vous voudrez une solution plus robuste :
- **cAdvisor** (Container Advisor) : un outil open-source créé par Google qui tourne en conteneur et collecte les métriques de tous les conteneurs Docker d’un hôte (CPU, mémoire, network, filesystem...). Il expose ces métriques, que l’on peut récolter via **Prometheus** (solution de monitoring open-source très utilisée pour containers et Kubernetes). Avec cAdvisor + Prometheus + Grafana, on peut avoir des tableaux de bord détaillés sur la santé de chaque conteneur.
- **Docker Dashboard** : Docker Desktop propose un petit dashboard de ressources mais sur un serveur Linux sans interface, ce n’est pas disponible.
- **Outils Cloud/APM** : Des solutions comme Datadog, NewRelic, etc., offrent des agents Docker pour remonter les métriques et parfois tracer les requêtes à travers les conteneurs.

**Alerting** : Pensez à mettre en place des alertes sur les métriques importantes : par exemple, si un conteneur consomme plus de 90% CPU sur 5 minutes, ou si la mémoire libre de l’hôte passe sous un seuil, etc. Ceci vous permettra d’intervenir avant une panne. Prometheus/Grafana ou des services SaaS peuvent envoyer des alertes email/Slack.

En complément, surveillez l’état de Docker lui-même. Assurez-vous que le daemon Docker tourne (par défaut en service systemd, il redémarre tout seul en cas de crash). Surveillez l’espace disque de `/var/lib/docker` (images et volumes peuvent remplir le disque – faites du nettoyage d’images obsolètes avec `docker system prune` de temps en temps, ou expansion de stockage si nécessaire).

Pour finir, loggez aussi l’activité Docker en elle-même : les actions de déploiement, etc., afin d’auditer qui a lancé quoi (sur un serveur multi-admin). Docker conserve un log (souvent via journald ou /var/log/docker.log suivant config) que vous pouvez consulter.

En résumé, une stack de production typique pourrait inclure :
- Un **système de logs centralisés** (par exemple Filebeat/Logstash + Elasticsearch + Kibana) pour agréger les logs de tous les conteneurs.
- Un **système de monitoring** (Prometheus + Grafana) scrutant les métriques d’infrastructure (Docker, OS) et éventuellement instrumentant les applications (via exporters ou APM).
- Des **alertes** pour réagir en cas d’incident (conteneur down, utilisation anormale, etc.).

Avec Docker, beaucoup de choses sont éphémères, il faut donc être particulièrement attentif à ne pas perdre l’information en route. Un conteneur qui crash et disparaît doit laisser derrière lui au moins un log d’erreur dans votre système centralisé, sans quoi le diagnostic sera compliqué.

## 8. CI/CD avec Docker

La conteneurisation s’intègre parfaitement aux chaînes d’intégration continue et de déploiement continu (**CI/CD**). Docker permet de construire une image de votre application à chaque changement de code et de la déployer de manière consistante sur vos différents environnements. Dans cette section, nous verrons comment Docker s’intègre avec des pipelines CI/CD tels que **GitHub Actions** ou **GitLab CI**, et comment automatiser la construction et le déploiement de vos conteneurs.

### 8.1 Intégration de Docker dans la CI

Sans Docker, une pipeline CI classique doit installer toutes les dépendances de l’application sur l’agent CI avant de lancer les tests ou le déploiement, ce qui peut être lent et sujet à des problèmes (versions d’outils différentes, etc.). Avec Docker, on peut au contraire :
- Soit utiliser **Docker pour exécuter les étapes CI** : par exemple, exécuter les tests de l’application à l’intérieur d’un conteneur configuré identiquement à l’environnement de prod. GitHub Actions et GitLab CI permettent de lancer des conteneurs Docker dans les jobs, garantissant que « ça marche pareil que sur ma machine ».
- Soit (et surtout) **construire l’image Docker** de l’application dans le pipeline CI, et éventuellement la pousser dans un registre. Cela permet de versionner chaque build (ex: taggé avec le commit ou un numéro de version), et de déployer exactement cette image en production.

L’idée typique : à chaque push sur la branche main (ou création d’une release), la CI va :
1. Builder l’image Docker de l’application (`docker build`).
2. L’exécuter et lancer les tests unitaires à l’intérieur (ou utiliser un conteneur séparé pour les tests, dépendant de la stratégie).
3. Si tests ok, pousser l’image vers un registre (Docker Hub, GitLab Registry, ECR AWS, etc.).
4. Déclencher le déploiement : par exemple, informer un serveur de récupérer la nouvelle image et de relancer un conteneur, ou créer une release sur Kubernetes.

Les systèmes CI/CD modernes (GitHub Actions, GitLab CI, Jenkins, etc.) ont de très bons supports de Docker.

### 8.2 Exemple avec GitHub Actions

GitHub Actions permet de définir des workflows d’intégration et déploiement via un fichier YAML (dans `.github/workflows/`). Voici un exemple simple de pipeline CI/CD qui build et push une image Docker :

```yaml
name: CI Build and Push
on:
  push:
    branches: [ main ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3  # Récupérer le code du dépôt
      - name: Build Docker image
        run: docker build -t monutilisateur/monapp:${{ github.sha }} .
      - name: Login to Docker Hub
        env:
          DOCKER_USER: ${{ secrets.DOCKER_USER }}
          DOCKER_PASS: ${{ secrets.DOCKER_PASS }}
        run: echo "$DOCKER_PASS" \| docker login -u "$DOCKER_USER" --password-stdin
      - name: Push image to registry
        run: docker push monutilisateur/monapp:${{ github.sha }}
```

Explication :
- Ce workflow se déclenche à chaque push sur la branche main.
- L’environnement d’exécution est une VM Ubuntu équipée de Docker.
- On checkoute le code, puis on exécute `docker build` pour construire l’image, en la taguant avec l’identifiant du commit (`github.sha` fournit le SHA du commit). On pourrait tagguer `latest` ou une version, mais utiliser le SHA garantit l’unicité.
- Ensuite, on se logge à Docker Hub (`docker login`) en utilisant des secrets stockés dans GitHub (il faut définir DOCKER_USER/PASS dans la configuration du repo GitHub).
- Enfin, on pousse l’image. Ainsi, à chaque modification, on aura sur Docker Hub une image à jour (taggée par son SHA ou on pourrait aussi tagger `latest` en plus pour la dernière version).

On pourrait enrichir ce workflow en ajoutant un job de tests (par exemple, *builder* l’image, puis *run* un conteneur de test ou utiliser `docker run` pour exécuter une suite de tests à l’intérieur, ou utiliser un service DB à côté pendant les tests). GitHub Actions permet d’utiliser des *services* (un peu comme Compose) ou de lancer plusieurs conteneurs.

### 8.3 Exemple avec GitLab CI/CD

Avec **GitLab CI**, l’idée est similaire. GitLab fournit un registre d’images intégré (Container Registry) par projet. Un runner GitLab peut utiliser Docker d’une façon particulière : souvent via **Docker-in-Docker (DinD)**. On active un service Docker dans le job pour pouvoir lancer des commandes Docker.

Un `.gitlab-ci.yml` simple pourrait être :
```yaml
image: docker:20.10  # image Docker CLI
services:
  - docker:dind     # service Docker Daemon

build:
  stage: build
  script:
    - docker build -t registry.gitlab.com/monprojet/monapp:$CI_COMMIT_SHA .
    - echo "$CI_REGISTRY_PASSWORD" \| docker login -u "$CI_REGISTRY_USER" $CI_REGISTRY --password-stdin
    - docker push registry.gitlab.com/monprojet/monapp:$CI_COMMIT_SHA
```

Ici on utilise l’image Docker officielle pour avoir la CLI, et on utilise le service `docker:dind` (un conteneur Docker Engine dans lequel la CLI va se connecter). On build puis on push sur le registry du projet (les variables CI_REGISTRY_USER/PASSWORD sont fournies automatiquement pour le registre GitLab). Le principe reste le même : produire l’image et la stocker.

**Déploiement continu :** Une fois l’image poussée, la phase CD (déploiement) peut prendre le relais. Selon votre infrastructure, cela peut être :
- Sur un serveur Docker classique : utiliser **SSH** pour se connecter au serveur et exécuter `docker pull` puis `docker-compose up -d` avec la nouvelle image, par exemple. GitHub Actions/GitLab CI peuvent faire du SSH sur un hôte pour déployer.
- Sur Kubernetes : on peut utiliser kubectl dans le pipeline (par ex. un job qui applique un manifeste Kubernetes mis à jour avec le nouveau tag d’image, ou qui utilise un déploiement auto-trigger).
- Via des outils spécialisés : par ex, utiliser Argo CD (GitOps) ou Helm charts déployés via pipeline. Ou les GitLab *Environments* et *Deploy Boards* si on utilise Kubernetes.

L’important est que, grâce à Docker, votre artefact de déploiement est l’image elle-même. Une fois qu’elle est testée et poussée, la même image est déployée en prod, évitant tout écart entre environnements. Vous pouvez tagger l’image avec le numéro de version ou le tag Git (ex: `1.2.3` ou `release-2023-03`) pour vous y retrouver.

**Intégration de tests dans des conteneurs :** Un autre usage de Docker en CI est de lancer les tests dans un environnement éphémère reproductible. Par exemple, on peut avoir un job qui fait `docker-compose -f docker-compose.test.yml up --abort-on-container-exit` pour exécuter une suite de tests intégration (en montant du code ou en construisant une image test dédiée) – à la fin, Compose arrête tout. Cela permet de tester votre application conteneurisée comme elle le serait en vrai.

En somme, Docker et la CI/CD vont de pair. En automatisant la construction d’images et leur déploiement, on obtient un flux de déploiement très rapide : un développeur pousse du code -> quelques minutes plus tard, une nouvelle image est construite et déployée sur un environnement (staging ou production) de manière consistante. Cette approche élimine beaucoup de problèmes de « configuration drift » et de « works on my machine », car tout est contenu dans l’image Docker créée par la CI.

## 9. Introduction à Kubernetes

Lorsque vos déploiements d’applications conteneurisées deviennent plus complexes (beaucoup de conteneurs, besoin de haute disponibilité, multi-nœuds…), il est temps de passer à l’**orchestration de conteneurs**. **Kubernetes** (souvent noté *K8s*) est la plateforme open-source la plus répandue pour automatiser le déploiement, la montée en charge et la gestion de conteneurs sur un cluster de machin ([Kubernetes — Wikipédia](https://fr.wikipedia.org/wiki/Kubernetes#:~:text=Kubernetes%20%28commun%C3%A9ment%20appel%C3%A9%20%C2%AB%C2%A0K8s,la%20Cloud%20Native%20Computing%20Foundation))9】. Dans ce chapitre, nous allons introduire les concepts clés de Kubernetes – en particulier les objets **Pods**, **Deployments** et **Services** – et voir comment installer un cluster de test, ainsi que les bases de la gestion de charges de travail conteneurisées avec K8s.

### 9.1 Concepts clés de Kubernetes

**Cluster Kubernetes :** Kubernetes fonctionne sur un ensemble de machines (physiques ou virtuelles) formant un cluster. Un cluster K8s se compose généralement de *nœuds de calcul* (workers) qui exécutent les conteneurs, et de composants de *plan de contrôle* (control plane) qui gèrent l’orchestration (API server, scheduler, contrôleurs, etc.). Kubernetes abstrait ces machines pour que vous déployiez vos applications sans vous soucier du détail de quel nœud individuel les exécute.

Les objets fondamentaux de Kubernetes pour décrire et gérer une application conteneurisée sont :

- **Pod** : l’unité de base de Kubernetes. Un Pod est le plus petit objet déployable dans Kubernet ([Pods | Kubernetes](https://kubernetes.io/fr/docs/concepts/workloads/pods/pod/#:~:text=Les%20Pods%20sont%20les%20plus,cr%C3%A9%C3%A9es%20et%20g%C3%A9r%C3%A9es%20dans%20Kubernetes))4】. Il encapsule un ou plusieurs conteneurs qui partagent un même espace réseau et de stockage. Dans la majorité des cas, un Pod contient un seul conteneur applicatif principal (éventuellement accompagné de conteneurs auxiliaires appelés *sidecars*). Si vous déployez un microservice, il sera généralement packagé dans un Pod = 1 conteneur. Kubernetes crée, supervise et termine des Pods, pas directement des conteneurs individuels.
- **Deployment (Déploiement)** : un contrôleur d’abstraction qui gère un ensemble de pods identiques (réplicas) et permet des mises à jour déclarativ ([Déploiements | Kubernetes](https://kubernetes.io/fr/docs/concepts/workloads/controllers/deployment/#:~:text=Un%20Deployment%20,d%C3%A9claratives%20pour%20Pods%20et%20ReplicaSets))4】. Avec un Deployment, vous déclarez dans un manifeste YAML l’*état désiré* de votre application (par exemple : « je veux 3 instances du pod *webapp*, tournant avec l’image *myapp:v1* »). Kubernetes se charge de créer ces pods (en arrière-plan, un Deployment gère un ReplicaSet qui lui-même gère les pods). Si un pod meurt, le Deployment en recrée un pour maintenir le nombre souhaité. Si vous voulez déployer une nouvelle version, vous modifiez le Deployment (par ex. nouvelle image *v2*), Kubernetes va orchestrer le remplacement graduel des pods (c’est le rolling update).
- **Service** : une abstraction réseau pour exposer vos po ([Service | Kubernetes](https://kubernetes.io/fr/docs/concepts/services-networking/service/#:~:text=Service))6】. Un Service définit un ensemble logique de pods (par un *selector* sur des labels) et fournit une adresse stable pour y accéder. Les pods peuvent changer (par ex, tués et recréés, donc avec nouvelles IPs), mais le Service reste en place pour les clients. Il existe plusieurs types de Services : 
  - *ClusterIP* (par défaut) : expose les pods à une IP interne du cluster (accessible seulement depuis le cluster, par d’autres pods).
  - *NodePort* : expose le service sur un port fixé de chaque nœud du cluster, ce qui permet d’y accéder de l’extérieur en visant n’importe quel nœud à ce port.
  - *LoadBalancer* : réservé généralement aux clusters dans le cloud, ce type demande à l’infrastructure cloud de provisionner un load balancer externe (par ex. un ELB sur AWS) pointant vers les pods. 
  - (Et d’autres comme ExternalName, etc.) 
  Un Service agit un peu comme un DNS + load balancer interne : il attribue un nom DNS stable et distribue le trafic vers les pods en backend.

Pour identifier les pods, Kubernetes utilise des **labels** (étiquettes clé=valeur) que vous pouvez attacher aux objets et sur lesquels les Service ou Deployments s’appuient (ex: Deployment va donner un label `app: webapp` à ses pods, et le Service va cibler `app: webapp` pour faire le lien).

Par exemple, on pourrait avoir : un Deployment nommé *webapp-deployment* qui gère des pods labelisés `app=webapp`. Un Service *webapp-service* selectionne `app=webapp` et écoute sur le port 80, répartissant les requêtes aux pods. Si on scale le Deployment à 5 pods, le Service enverra le trafic aux 5.

En plus de ces objets, Kubernetes en comporte beaucoup d’autres (ConfigMap pour les configs, Secret pour les secrets, Ingress pour la gestion fine du trafic HTTP, StatefulSet pour les applications à état comme bases de données, DaemonSet, Job/CronJob, etc.). Mais Pod, Deployment et Service sont vraiment le trio de base pour n’importe quelle application sans état (stateless app).

### 9.2 Installation d’un cluster Kubernetes (pour tests)

Mettre en place Kubernetes peut être complexe (surtout sur plusieurs nœuds), mais il existe des solutions simples pour tester en local :
- **Minikube** : un outil qui installe un cluster Kubernetes monoposte dans une VM sur votre machine. En une commande `minikube start`, vous avez un petit cluster fonctionnel (un seul nœud faisant office de control plane et worker).
- **Docker Desktop** : intègre une option "Enable Kubernetes". En l’activant, Docker Desktop démarre un Kubernetes mono-noeud dans votre environnement Docker. Pratique pour les tests rapides (pas besoin d’installer autre chose).
- **Kind** (Kubernetes-in-Docker) : lance un cluster Kubernetes en exécutant les nœuds control plane et worker eux-mêmes comme conteneurs Docker. C’est léger et scriptable.
- **MicroK8s** : distribution Kubernetes allégée proposée par Canonical (Ubuntu) pour un usage local ou edge, s’installe via snap sur Linux.

Pour un usage sérieux en production, on utilise souvent des **services managés** (GKE sur Google Cloud, EKS sur AWS, AKS sur Azure, etc.) ou des distributions comme kubeadm, Rancher, K3s, etc. Sur un VPS, vous pourriez installer Kubernetes via **kubeadm** : c’est l’outil officiel pour déployer un cluster : on promeut un serveur en master, puis on join d’autres serveurs comme workers. Cependant, c’est assez impliqué (certificats, réseaux à configurer, etc.). Si vous voulez expérimenter sur 2-3 VMs, kubeadm est un bon apprentissage, mais pour un débutant, minikube est plus simple.

**Installer Minikube (bref aperçu) :**
- Avoir Docker ou une solution de VM (VirtualBox par ex) sur votre machine.
- Télécharger l’exécutable minikube.
- Faire `minikube start` – ça va créer une VM Linux et y déployer Kubernetes.
- minikube configure automatiquement `kubectl` (le client en ligne de commande de Kubernetes) pour pointer vers ce cluster.

Une fois minikube démarré, vous pouvez utiliser `kubectl get nodes` pour voir le nœud, etc. Le kubectl est l’outil principal pour interagir avec Kubernetes.

### 9.3 Gestion des workloads sur Kubernetes

Déployer une application sur Kubernetes consiste généralement à **écrire des fichiers YAML** décrivant les objets (Deployment, Service, etc.), puis à les appliquer au cluster via `kubectl apply -f mondeploiement.yaml`.

Par exemple, un manifeste YAML de Deployment minimal pour notre application web pourrait être :
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp
  template:   # spécification des pods
    metadata:
      labels:
        app: webapp
    spec:
      containers:
      - name: webapp-container
        image: monutilisateur/monapp:1.0
        ports:
        - containerPort: 3000
```
Ici on demande 3 replicas de `monutilisateur/monapp:1.0`. Kubernetes va donc démarrer 3 pods contenant chacun ce conteneur. Si on fait `kubectl get pods`, on verra 3 pods (nommés automatiquement *webapp-deployment-xxxxx*). 

On exposerait cela avec un Service, par exemple :
```yaml
apiVersion: v1
kind: Service
metadata:
  name: webapp-service
spec:
  type: NodePort
  selector:
    app: webapp
  ports:
    - port: 3000       # port interne du service (cible des pods)
      targetPort: 3000 # port exposé par les pods
      nodePort: 30000  # port sur les nodes
```
Ce Service prendra tous les pods avec `app=webapp` (donc nos 3 pods) et les rendra accessibles sur chaque machine du cluster via le port 30000. Sur minikube (un seul node), on pourrait ainsi accéder à `http://<IP_minikube>:30000` pour joindre l’application.

**Commande kubectl de base :** 
- `kubectl get pods,deploy,svc` pour lister les ressources.
- `kubectl describe pod <name>` pour obtenir les détails et événements d’un pod (précieux en cas d’erreur de démarrage).
- `kubectl logs <pod>` pour voir les logs (on peut ajouter `-f` ou `-c nom_du_containeur` si plusieurs conteneurs dans un pod).
- `kubectl exec -it <pod> -- bash` pour entrer dans un conteneur du pod (similaire à `docker exec`).
- `kubectl scale deployment/webapp-deployment --replicas=5` pour changer le nombre de replicas.
- `kubectl rollout status deployment/webapp-deployment` pour voir la progression d’un déploiement (par ex, lors d’une mise à jour).
- `kubectl apply -f fichier.yaml` pour créer ou mettre à jour des objets via un fichier.
- `kubectl delete -f fichier.yaml` pour supprimer ce qui est décrit dans le fichier, ou `kubectl delete pod/nom` etc. pour un objet spécifique.

**Auto-réparation et scaling :** Kubernetes va surveiller les pods : si un nœud tombe en panne, les pods qui y tournaient sont reprogrammés ailleurs (si d’autres nœuds dispos). Le Deployment s’assure toujours d’avoir le bon nombre de pods vivants. On peut configurer des **probes de santé** (livenessProbe, readinessProbe) dans la spec du conteneur pour que Kubernetes sache détecter un conteneur planté (liveness) ou pas encore prêt à recevoir du trafic (readiness). En fonction, Kubernetes peut redémarrer le conteneur ou l’isoler du Service temporairement.

K8s offre aussi le **Horizontal Pod Autoscaler (HPA)**, qui peut augmenter/diminuer le nombre de pods en fonction de la charge (par ex., si CPU > 80% sur 5 min, ajouter des pods). Pour cela, il faut avoir des métriques (via Metrics Server). C’est un sujet un peu avancé, mais sachez que la scalabilité horizontale peut être automatique.

**Mises à jour** : Avec un Deployment, un changement d’image ou de configuration déclenche un *rolling update* par défaut : K8s va créer un nouveau pod (avec la nouvelle version) avant de supprimer un ancien, et ainsi de suite, assurant qu’à tout moment il reste des pods pour servir. Vous pouvez ajuster la stratégie (max pods en plus/en moins, etc.). En cas de problème, vous pouvez faire un *rollback* du déploiement à la version précédente très facilement (`kubectl rollout undo deployment/webapp-deployment`).

**Organisation** : En pratique, on regroupe plusieurs objets dans des fichiers ou charts (Helm). Par exemple, un déploiement complet d’appli comprend souvent : Deployment, Service, Ingress (pour routage http), ConfigMap/Secret (pour la config), PersistentVolumeClaim (pour réserver du stockage si base de données, dans le cas d’un StatefulSet). Kubernetes a une courbe d’apprentissage, mais une fois les concepts assimilés, il offre un contrôle très fin et une grande fiabilité pour exécuter des conteneurs en prod.

Enfin, Kubernetes a son propre écosystème d’outils (kubectl étant de base). Des tableaux de bord web existent (Lens, le dashboard officiel K8s, etc.) pour visualiser les ressources. Et des opérateurs/contrôleurs additionnels peuvent être installés pour ajouter des fonctionnalités (autoscaler de pods, gestion de certificats auto, etc.).

Pour un débutant, le plus gros défi est de se familiariser avec la terminologie et la logique déclarative de Kubernetes. Commencez par déployer une application simple sur minikube en suivant la documentation – par exemple *Hello World* ou une app web comme la nôtre – et expérimentez les commandes kubectl.

*Kubernetes* est un vaste sujet, mais maîtriser Docker vous donne déjà une base solide, car beaucoup de concepts (images, conteneurs, ports, volumes) restent valables. Kubernetes se charge juste de lancer les conteneurs sur un cluster de machines de façon intelligente. En résumé, comme le dit souvent la communauté : Docker vous permet d’exécuter un conteneur sur *votre* machine, Kubernetes vous permet d’exécuter des conteneurs sur *des centaines* de machines de manière automatisée.

## 10. Étude de cas et projets pratiques

Pour terminer ce guide, illustrons de manière concrète tout le parcours de déploiement d’une application web conteneurisée, depuis le développement jusqu’à la production orchestrée. Nous allons prendre l’exemple d’une application web simple composée de deux éléments : un frontend (notre application web) et une base de données MySQL. L’objectif est de montrer comment :

1. **Containeriser l’application** avec Docker (écrire un Dockerfile et construire l’image).
2. **Configurer l’environnement de développement** avec Docker Compose (pour lancer l’appli et la DB ensemble facilement en local).
3. **Déployer en production** en utilisant Kubernetes sur un cluster.

Imaginons que notre application soit un petit serveur web développé en Node.js qui stocke des données dans une base MySQL. Appelons-la *MyApp*. Voici les grandes étapes :

### 10.1 Conteneurisation de l'application web (Dockerfile)

Supposons que le code de *MyApp* est dans un répertoire `myapp/` avec un fichier `package.json` (pour les dépendances Node) et un fichier d’entrée `index.js`. La première étape est d’écrire un **Dockerfile** pour emballer cette application Node.js dans une image.

Dockerfile (`myapp/Dockerfile`) :
```dockerfile
# Étape 1 : image de base Node.js
FROM node:18-alpine

# Étape 2 : définir le répertoire de l'application
WORKDIR /app

# Étape 3 : copier les fichiers de dépendances et installer
COPY package*.json ./
RUN npm install --production

# Étape 4 : copier le code de l'application
COPY . .

# Étape 5 : exposer le port d'écoute de l'application (par ex 3000)
EXPOSE 3000

# Étape 6 : commande de démarrage
CMD ["node", "index.js"]
```

Explication rapide :
- On part de l'image Node.js officielle en version 18 (variante alpine pour la légèreté).
- On définit le dossier de travail et on copie le fichier `package.json` et `package-lock.json` (le wildcard package*.json les couvre). Puis on lance `npm install` pour installer les dépendances nécessaires.
- On copie ensuite le reste du code.
- On expose le port 3000 (admettons que notre app écoute sur 3000).
- On définit la commande `node index.js` pour démarrer le serveur web.

Avec ce Dockerfile, on peut construire l’image de notre application. Supposons que l’on veuille la tagger `myapp:dev` pour indiquer que c’est l’image de développement (on utilisera un autre tag pour la production plus tard) :

```bash
# depuis le répertoire myapp/
docker build -t myapp:dev .
```

Docker va produire l’image locale `myapp:dev`. Testons-la rapidement (en la reliant à une DB MySQL existante par exemple, si on en a une). Mais pour l’instant, concentrons-nous sur l'intégration avec MySQL via Compose.

### 10.2 Environnement de développement avec Docker Compose

Pour développer et tester *MyApp*, nous allons utiliser **Docker Compose** afin de lancer à la fois l’application Node (conteneur basé sur l’image qu’on vient de construire) et un conteneur MySQL pour la base de données. L’utilisation de Compose va nous simplifier la vie : un seul fichier pour configurer les deux, et une commande pour tout lancer.

Créons un fichier `docker-compose.yml` à la racine du projet :

```yaml
services:
  app:
    build: ./myapp   # construit l'image à partir du Dockerfile dans myapp/
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=db
      - DB_NAME=myappdb
      - DB_USER=root
      - DB_PASSWORD=example
    depends_on:
      - db

  db:
    image: mysql:8
    environment:
      - MYSQL_DATABASE=myappdb
      - MYSQL_ROOT_PASSWORD=example
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
```

Dans ce fichier Compose :
- Le service **app** va construire l’image à partir du Dockerfile (option `build: ./myapp` pointant vers le dossier). On expose le port 3000 pour accéder à l'appli web depuis l’hôte. On définit quelques variables d’environnement que l’application Node utilisera pour se connecter à la DB (nom d’hôte du serveur DB, nom de la base, user, mot de passe). Ici, par simplicité on utilise l’utilisateur root de MySQL avec un mot de passe (pas idéal en prod, mais en dev ça va). `depends_on: db` assure que le conteneur db soit démarré avant app.
- Le service **db** utilise l’image MySQL 8. On passe `MYSQL_DATABASE` pour qu’une base `myappdb` soit créée d’office, et `MYSQL_ROOT_PASSWORD` pour le mot de passe root (ici "example"). On monte un volume nommé `db_data` pour persister les données MySQL (ainsi arrêter/relever Compose ne perd pas les données insérées).
- On a déclaré le volume `db_data` à la fin.

Pour lancer le tout, on exécute simplement :
```bash
docker-compose up -d
```
Compose va:
  - Construire l’image *app* (équivalent à notre `docker build` plus tôt).
  - Créer le réseau `mon_projet_default` et le volume `db_data`.
  - Démarrer le conteneur **db** (MySQL) puis **app** (MyApp). Le conteneur app verra la variable `DB_HOST=db`, et grâce au réseau commun, le nom d’hôte `db` résoudra l’adresse IP du conteneur MySQL.

Après quelques secondes, MySQL devrait être opérationnel et *MyApp* peut sans doute se connecter (il faudra dans le code Node.js récupérer ces variables d’env et se connecter, par ex. en utilisant `process.env.DB_HOST`, etc.). Vous pouvez vérifier les logs :
```bash
docker-compose logs -f app
```
pour voir si l’app Node a réussi sa connexion. Vous pouvez aussi vous connecter à MySQL pour vérifier que la base `myappdb` existe, par exemple en exécutant :
```bash
docker-compose exec db mysql -uroot -pexample -e "SHOW DATABASES;"
``` 
(qui utilisera le client mysql à l’intérieur du conteneur).

Si tout est bon, en ouvrant un navigateur sur http://localhost:3000, vous devriez accéder à l'application *MyApp*. Dans le cas d’une API REST, on pourrait faire des requêtes avec curl. L’essentiel est qu’en quelques minutes, on a mis en place un environnement de dev isolé, sans installer MySQL ou Node localement : tout tourne dans Docker. Chaque membre de l’équipe pourrait lancer le même `docker-compose up` et obtenir un environnement identique.

Pendant la phase de développement, on peut reconstruire l’image app à chaque modification du code, ou monter le code en volume pour recharger à chaud (on aurait pu faire `volumes: - "./myapp:/app"` pour que les modifications locales soient vues dans le conteneur, couplé avec un outil genre nodemon pour restart auto – ceci est une amélioration possible du workflow de dev).

### 10.3 Déploiement de l'application sur Kubernetes (production)

Une fois l’application testée et prête, comment la déployer en production sur un serveur ou cluster Kubernetes ?

**Préparation de l’image de production :** 
D’abord, on peut reconstruire l’image Node sans le tag *dev*. Éventuellement, on optimise le Dockerfile pour la prod (par ex, utiliser `NODE_ENV=production`, retirer d’éventuelles dépendances de dev, etc.). Disons que l’on construit et tague l’image comme `monutilisateur/monapp:1.0` et qu’on la pousse sur Docker Hub (ou un registre privé). Cette étape peut être faite via CI/CD comme décrit précédemment.

**Base de données en production :** 
Plusieurs approches :
- Utiliser également un conteneur MySQL sur le cluster K8s. Kubernetes sait gérer du stockage persistant via des PersistentVolumeClaim. On pourrait déployer MySQL dans un *StatefulSet* avec un volume persistant (ce qui assure que les données survivent aux recréations de pod). C’est faisable, bien que pour des bases critiques en production, on utilise parfois un service géré (RDS, Cloud SQL...) ou on la garde hors cluster.
- Pour notre cas, on va continuer avec MySQL conteneurisé, pour garder l’étude homogène.

**Déploiement Kubernetes :** 
Nous allons créer un Deployment pour *MyApp* et un Deployment (ou StatefulSet) pour MySQL, plus les Services nécessaires.

Commençons par le **Deployment de MyApp** (fichier `k8s-myapp-deployment.yaml`) :
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: monutilisateur/monapp:1.0
        env:
        - name: DB_HOST
          value: "mysql"               # on supposera un Service "mysql" pour la DB
        - name: DB_NAME
          value: "myappdb"
        - name: DB_USER
          value: "root"
        - name: DB_PASSWORD
          value: "example"
        ports:
        - containerPort: 3000
```

Ici, on déploie 2 replicas de l’app (on peut en mettre plus pour répartir la charge). On passe les mêmes variables d’env qu’avant, en particulier `DB_HOST=mysql` – cela signifie qu’on s’attend à avoir un Service DNS nommé "mysql" dans le namespace. On expose le port 3000 du conteneur (note: cela aide Kubernetes à savoir quel port est *targetPort* par défaut pour un Service le sélectionnant).

Ensuite, le **Deployment (ou StatefulSet) pour MySQL** (`k8s-mysql-deployment.yaml`). Pour simplifier, utilisons un Deployment aussi (idéalement un StatefulSet serait plus approprié pour une base, car il gère mieux le stockage et le naming, mais ça complexifie peu inutilement l’exemple) :
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:8
        env:
        - name: MYSQL_DATABASE
          value: "myappdb"
        - name: MYSQL_ROOT_PASSWORD
          value: "example"
        ports:
        - containerPort: 3306
        volumeMounts:
        - name: mysql-data
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-data
        emptyDir: {}
```

Ici on déploie MySQL (1 replica). On utilise un volume `emptyDir` pour le stockage de /var/lib/mysql – **attention** : emptyDir est éphémère (lié à la vie du Pod). En production réelle, il faudrait un PersistentVolumeClaim pour que les données survivent à un redéploiement du pod sur un autre nœud. Disons que pour un test, emptyDir suffit (mais retenez que ce n’est pas persistant à long terme : si le Pod bouge de nœud, les données sont perdues). On fournit les mêmes env de création de base et mdp root qu’avant.

Enfin, créons les **Services** pour exposer ces deux Deployments (`k8s-services.yaml` par exemple) :
```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql
spec:
  selector:
    app: mysql
  clusterIP: None
  ports:
    - port: 3306
      targetPort: 3306

---
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: NodePort
  selector:
    app: myapp
  ports:
    - port: 3000
      targetPort: 3000
      nodePort: 30000
```

Explications :
- Le Service **mysql** a un `clusterIP: None`. Ceci en fait un *Headless Service*, qui n’attribue pas d’IP stable mais permet la découverte DNS *sans load balancing* (chaque pod a son DNS). Dans notre cas, comme il n’y a qu’un pod MySQL, on aurait pu mettre un ClusterIP normal. L’important est que le nom "mysql" existe – nos pods MyApp vont résoudre "mysql" et obtenir l’IP du pod MySQL. On expose le port 3306. (ClusterIP None n’est pas forcément nécessaire, c’est une variante pour DB stateful).
- Le Service **myapp-service** est de type NodePort, ce qui permet un accès externe. Il prend tous les pods avec label `app=myapp` (nos 2 pods Node.js) et écoute sur port 3000, mappé sur le port 3000 des pods. Le champ `nodePort: 30000` indique que sur chaque node du cluster, le port 30000 sera ouvert pour ce service. Ainsi, depuis l’extérieur (supposant qu’on a l’IP du node), on peut accéder à `<nodeIP>:30000` et ça distribuera aux pods. Sur minikube, on ferait `minikube service myapp-service --url` pour obtenir l’URL par exemple.

On peut appliquer ces manifests sur le cluster (minikube ou un vrai cluster) via :
```bash
kubectl apply -f k8s-mysql-deployment.yaml
kubectl apply -f k8s-myapp-deployment.yaml
kubectl apply -f k8s-services.yaml
```

Kubernetes va créer le tout. On peut surveiller avec `kubectl get pods -w` pour voir les pods se télécharger (il téléchargera l’image `monutilisateur/monapp:1.0` depuis le registre) et démarrer. Une fois en statut *Running*, on teste l’accès :
- Depuis l’intérieur du cluster : on pourrait exec dans le pod myapp et faire un curl sur localhost:3000 ou utiliser `kubectl port-forward service/myapp-service 3000:3000` pour accéder en local.
- Depuis l’extérieur (si cluster sur un VPS par ex) : taper `http://<IP-du-noeud>:30000`. Sur minikube, `minikube service myapp-service` ouvre directement le navigateur sur l’URL correcte.

Notre application devrait répondre, reliée à son MySQL. On a donc réussi le déploiement sur Kubernetes ! 🎉

**Améliorations et bonnes pratiques de ce déploiement :**
- Comme dit, on utiliserait un *PersistentVolume* pour MySQL en prod afin de ne pas perdre les données si le pod bouge.
- On ajouterait probablement un Ingress Controller pour éviter d'utiliser un NodePort (Ingress permet d’exposer via une entrée HTTP/HTTPS plus élégamment, souvent combiné avec un LoadBalancer sur le cloud).
- On sécuriserait l’accès DB (utiliser un user applicatif au lieu de root, mettre le mot de passe dans un Secret Kubernetes plutôt qu’en clair dans le déploiement).
- On configurerait des *Liveness/Readiness Probes* sur le conteneur myapp (par ex, un endpoint `/health`) pour que Kubernetes sache quand le pod est prêt ou doit être redémarré.
- On pourrait ajuster le nombre de replicas myapp selon la charge, voire mettre un HPA.

Malgré ces simplifications, ce scénario montre le chemin parcouru :
- On a développé et testé localement avec Compose, très proche de la config prod.
- On a construit une image Docker unique de l'app, qu’on a pu déployer inchangée sur le cluster.
- En prod, Kubernetes gère le redémarrage automatique des conteneurs, l’éventuelle mise à l’échelle (si on modifie `replicas`), et la robustesse (si un node tombe, on pourrait en avoir un autre).
- Si on veut déployer une version 2.0 de l’app, on construirait l’image `monutilisateur/monapp:2.0`, on mettrait à jour le Deployment (via `kubectl set image deployment/myapp-deployment myapp=monutilisateur/monapp:2.0` par exemple), et Kubernetes ferait le rolling update sans downtime.

Cette étude de cas, du code source jusqu’au déploiement orchestré, illustre la puissance de Docker et Kubernetes pour un workflow moderne :
développeurs et ops peuvent collaborer autour de fichiers de config (Dockerfile, docker-compose.yml, manifests Kubernetes) au lieu de manipulations manuelles. L’environnement est isolé et reproductible, que ce soit sur la machine de dev, le serveur de staging ou le cluster de production.

**Projets pratiques pour aller plus loin :** 
- Tentez de conteneuriser une application existante (une appli Python Flask + Redis par ex.), déployez-la avec Compose, puis sur Kubernetes (peut-être en utilisant un Chart Helm pour apprendre un autre outil).
- Explorez des architectures multi-conteneurs plus complexes : par exemple, déployer un stack MEAN (MongoDB, Express, Angular, Node) ou une appli 3 tiers (frontend, API, DB) en utilisant Docker Compose pour le dev et Kubernetes pour la prod.
- Mettez en place une pipeline CI/CD réelle : code sur GitHub, Actions qui build/push l’image, et peut-être un déploiement auto sur un cluster Kubernetes de test (il existe des actions GitHub pour kubectl ou Helm).
- Testez la résilience : faites tomber un conteneur exprès (`docker kill`) et voyez Docker le redémarrer (si restart: always) ou Kubernetes recréer un pod, etc.
