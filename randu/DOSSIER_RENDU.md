# Dossier de rendu : GitOps & CI/CD

**Nom :** ELIE  
**Prénom :** Alban  
**Date :** Novembre 2026  
**Dépôt GitHub applicatif :** [https://github.com/FamilyTsuki/tasks-api](https://github.com/FamilyTsuki/tasks-api)  
**Dépôt GitHub de configuration (GitOps) :** [https://github.com/FamilyTsuki/tasks-config](https://github.com/FamilyTsuki/tasks-config)  

---

# TP1 : Première CI avec GitHub Actions

### Objectif
Le but de ce premier TP était de découvrir GitHub Actions en créant notre premier workflow sur les push. On a automatisé le lancement des tests pytest à chaque commit, appris à lire les logs quand un test échoue et mis en place une pull request avec badge de statut.

### Captures d'écran

* **TP1-1 :** Le premier workflow `Hello` réussi avec la branche et l'auteur dépliés dans les logs.  
  ![TP1-1](TP1/TP1-1.png)

* **TP1-2 :** Le workflow `ci.yml` réussi avec toutes les étapes d'installation et de test visibles.  
  ![TP1-2](TP1/TP1-2.png)

* **TP1-3 :** Le run en échec après avoir cassé volontairement la taille max du titre dans le code.  
  ![TP1-3](TP1/Pp1-3.png)

* **TP1-4 :** Le retour au vert de la CI après correction de la valeur dans `logic.py`.  
  ![TP1-4](TP1/TP1-4.png)

* **TP1-5 :** La pull request ouverte avec les checks de la CI au vert avant de la fusionner.  
  ![TP1-5](TP1/TP1-5.png)

* **TP1-6 :** La pull request fusionnée sur `main` (statut Merged violet).  
  ![TP1-6](TP1/TP1-6.png)

* **TP1-7 :** La page d'accueil du dépôt avec le badge vert de la CI affiché dans le README.  
  ![TP1-7](TP1/TP1-7.png)

### Réponses aux questions

* **Q1 : Combien de temps a duré le run « Hello » ? Où voit-on les logs de chaque étape ?**  
  Durée totale : 39s (dont 36s pour le job). Les logs se voient sur la page du run en cliquant sur le job `test`, puis en dépliant chaque étape dans la console.
* **Q2 : Quel test a échoué dans la partie 3, et à quelle ligne ? Qu'est-ce qui a permis de le trouver rapidement ?**  
  L'étape en échec était `Run pytest` : `test_is_valid_title_accepts_normal_title` à la ligne 13 de `tests/test_logic.py` et `test_add_and_list_tasks` à la ligne 29 de `tests/test_api.py` à cause de `MAX_TITLE_LENGTH = 2`. On l'a trouvé direct grâce au bloc `short test summary info` en bas des logs.
* **Q3 : Pourquoi attend-on que la CI soit verte avant de fusionner une pull request ?**  
  Pour éviter de push des erreurs sur la branche `main` et être sûr que le code qu'on fusionne passe tous les tests.

### Difficultés rencontrées
Au début j'ai push avec les deux variables echo séparées, du coup pour la capture TP1-1 il a fallu regrouper branche et auteur dans la même étape pour que ce soit bien lisible une fois déplié.

---

# TP2 : Une CI solide

### Objectif
Dans ce TP on a rendu la CI plus robuste en séparant le linting du test, en ajoutant un seuil de couverture minimale et une matrice de versions Python avec du cache. On a aussi protégé la branche `main`, géré des conflits Git en équipe, masqué des secrets et réparé trois pipelines buggés.

### Captures d'écran

* **TP2-1 :** Le run réussi montrant les deux jobs séparés `lint` et `test`.  
  ![TP2-1](TP2/TP2-1.png)

* **TP2-2 :** Le job `lint` en rouge avec l'erreur flake8 bien visible dans les logs.  
  ![TP2-2](TP2/TP2-2.png)

* **TP2-3 :** La matrice qui fait tourner les tests en parallèle sur Python 3.11, 3.12 et 3.13.  
  ![TP2-3](TP2/TP2-3.png)

* **TP2-4 :** Le cache pip réutilisé au deuxième run et l'artefact `coverage.xml` téléchargeable.  
  ![TP2-4-1](TP2/TP2-4-1.png)  
  ![TP2-4-2](TP2/TP2-4-2.png)

* **TP2-5 :** La règle de protection de `main` sur GitHub avec `lint` et `test (3.12)` obligatoires.  
  ![TP2-5](TP2/TP2-5.png)

* **TP2-6 :** La pull request bloquée car un test obligatoire a échoué (bouton gris/rouge).  
  ![TP2-6](TP2/TP2-6.png)

* **TP2-7 :** La pull request de B qui affiche le conflit avec la branche `main`.  
  ![TP2-7](TP2/TP2-7.png)

* **TP2-8 :** Le fichier `CHANGELOG.md` sur GitHub contenant bien les deux lignes après fusion.  
  ![TP2-8](TP2/TP2-8.png)

* **TP2-9 :** Les logs de GitHub Actions où la valeur secrète est masquée par `***`.  
  ![TP2-9](TP2/TP2-9.png)

* **TP2-10 :** Les 3 pipelines d'exercice en échec (A : syntaxe yaml, B : checkout manquant, C : python 3.10 lu en 3.1).  
  ![TP2-10A](TP2/TP2-10A.png)  
  ![TP2-10B](TP2/TP2-10B.png)  
  ![TP2-10C](TP2/TP2-10C.png)

* **TP2-11 :** La liste des runs montrant les 3 pipelines corrigés au vert.  
  ![TP2-11](TP2/TP2-11.png)

### Réponses aux questions

* **Q1 : Quelle différence entre un linter (flake8) et un formateur (black) ? Pourquoi séparer `lint` et `test` en deux jobs ?**  
  Flake cherche les erreurs de style et les bugs (variables inutilisées, etc.) alors que Black réécrit le code pour lui donner un style uniforme. On les sépare en deux jobs pour voir simplement à quelle étape est l'erreur et pouvoir les faire tourner en même temps.
* **Q2 : Pourquoi tester sur plusieurs versions de Python ? Que gagne-t-on avec le cache ? Un artefact, c'est quoi ?**  
  Pour être sûr que le code marche sur toutes les versions que les utilisateurs peuvent avoir et voir direct si une version casse quelque chose. Avec le cache on gagne du temps parce que pip réutilise les paquets déjà téléchargés au lieu de tout re-télécharger. Un artefact c'est un fichier produit par le run (ici `coverage.xml`) qu'on peut récupérer après.
* **Q3 : Pourquoi interdire de pousser directement sur `main` ?**  
  Pour interdire de casser la branche principale avec du code pas testé, ça force à passer par une PR et à attendre que la CI soit verte.
* **Q4 : Pourquoi Git ne peut-il pas résoudre ce conflit seul ? Qu'est-ce qui a vérifié le code après la résolution ?**  
  Parce que les deux branches ont modifié la même ligne du CHANGELOG et Git ne sait pas laquelle garder ou s'il faut garder les deux, c'est à nous de choisir. C'est la CI qui s'est relancée sur la PR après le commit de résolution et a refait passer lint + tests.
* **Q5 : Pourquoi masquer la valeur dans les logs ? Qu'est-ce qui se passe si on commite un secret dans Git ? Différence secret vs variable ?**  
  Pour que personne ne puisse le lire dans les logs vu qu'ils sont visibles par tous sur un dépôt public. Si on commite un secret, il reste dans l'historique Git pour toujours même si on le supprime après, donc il faut le considérer comme compromis et le révoquer direct. On utilise un secret pour ce qui est sensible (tokens, mdp) et une variable pour la config non secrète.
* **Q6 : Analyse des 3 pipelines réparés :**  
  - *Pipeline A :* erreur d'indentation yaml à la ligne 12 (`- run` décalé de 7 espaces au lieu de 6). GitHub Actions a refusé de lancer le job. Pour éviter ça : mettre un linter yaml dans son éditeur.  
  - *Pipeline B :* il manquait l'étape `actions/checkout`. Le `pip install` a planté avec `FileNotFoundError` sur `requirements-dev.txt` car le runner démarre vide. Pour éviter ça : toujours mettre checkout au début.  
  - *Pipeline C :* les versions python dans la matrix étaient sans guillemets `[3.10, 3.11, 3.12]`, du coup `3.10` a été lu comme `3.1`. L'étape `setup-python` a cherché Python 3.1 qui n'existe pas. Pour éviter ça : toujours mettre des guillemets autour des versions.

### Difficultés rencontrées
Pour le conflit, il a fallu faire attention à bien retirer les balises `<<<<<<<` et `>>>>>>>` dans le CHANGELOG et garder les deux phrases. Pour le pipeline C le bug était vicieux parce que c'est le parseur YAML qui transforme `3.10` en nombre flottant `3.1`.

---

# TP3 : Docker et livraison continue

### Objectif
L'objectif du TP3 était de conteneuriser notre API avec un Dockerfile léger et sécurisé (utilisateur non-root), d'utiliser Docker Compose en local, puis de créer un workflow qui teste, construit et publie automatiquement les images versionnées sur GitHub Packages (GHCR) avec validation manuelle pour la prod.

### Captures d'écran

* **TP3-1 :** La construction de l'image Docker locale et le `curl /health` qui répond `{"status":"ok"}`.  
  ![TP3-1-1](TP3/TP3-1-1.png)  
  ![TP3-1-2](TP3/TP3-1-2.png)

* **TP3-2 :** Lancement avec `docker compose up` et test du `/version` qui répond `local`.  
  ![TP3-2-1](TP3/TP3-2-1.png)  
  ![TP3-2-2](TP3/TP3-2-2.png)

* **TP3-3 :** Le workflow GitHub Actions montrant le job `test` suivi du job `build` au vert.  
  ![TP3-3](TP3/TP3-3.png)

* **TP3-4 :** La page du package `tasks-api` sur GHCR avec son premier tag `sha-...`.  
  ![TP3-4](TP3/TP3-4.png)

* **TP3-5 :** La liste des tags du package montrant à la fois `0.1.0` et les tags sha.  
  ![TP3-5](TP3/TP3-5.png)

* **TP3-6 :** `docker run` de l'image téléchargée depuis GHCR et réponse `0.1.0` sur `/version`.  
  ![TP3-6](TP3/TP3-6.png)

* **TP3-7 :** Le pipeline en pause en attente d'approbation sur l'environnement production, puis le run terminé.  
  ![TP3-7-1](TP3/TP3-7-1.png)  
  ![TP3-7-2](TP3/TP3-7-2.png)

* **TP3-8 :** Sortie de la commande `id` dans le conteneur confirmant l'utilisateur non-root `uid=1000(app)`.  
  ![TP3-8](TP3/TP3-8.png)

### Réponses aux questions

* **Q1 : C'est quoi une image ? Un conteneur ? À quoi sert le `.dockerignore` ?**  
  Une image c'est le modèle figé (le code + les dépendances), un conteneur c'est une image qui tourne (on peut lancer plusieurs conteneurs depuis la même image). Le `.dockerignore` sert à pas copier les fichiers inutiles (`.git`, `.venv`, cache...) pour que l'image soit plus légère, que le build soit plus rapide et pour pas mettre de trucs sensibles dedans.
* **Q2 : Que gagne-t-on à décrire le lancement dans un `docker-compose.yml` plutôt qu'une longue commande ?**  
  Ça évite de retaper toute la ligne avec les ports et les variables à chaque fois, ça accélère le lancement et on est sûr d'avoir la même configuration à chaque fois.
* **Q3 : Pourquoi `build` attend-il `test` ? Pourquoi éviter le tag `latest` en production ?**  
  Pour pas construire et publier une image avec du code cassé si les tests ratent. `latest` change à chaque push donc on sait jamais quelle version tourne vraiment en prod et c'est dur de revenir en arrière, avec un tag fixe (`0.1.0` ou le sha) on sait exactement ce qui tourne.
* **Q4 : Quel est l'avantage d'une image versionnée par rapport à « le code de ma machine » ?**  
  L'image c'est toujours la même partout (ma machine, la CI, la prod) avec les mêmes dépendances, alors que le code de ma machine dépend de ce qui est installé localement. Avec une version on sait exactement ce qui tourne et on peut revenir à une ancienne version facilement.
* **Q5 : À quoi sert un test de fumée ? Pourquoi demander une approbation humaine avant la prod ?**  
  Un test de fumée c'est un test rapide juste après le déploiement (comme un curl sur `/health`) pour vérifier que l'app démarre et répond bien. On demande une validation humaine pour qu'une vraie personne vérifie avant que ça parte en prod vu que c'est utilisé par de vrais utilisateurs, ça évite de déployer un truc pas voulu juste parce que la pipeline est verte.
* **Q6 : Pourquoi ne pas exécuter une application en root dans un conteneur ? Bonnes pratiques de l'affaire Trivy ?**  
  Ne jamais exécuter en root parce que si quelqu'un trouve une faille dans l'app il a tous les droits dans le conteneur et ça peut l'aider à s'échapper sur la machine hôte. Avec un utilisateur normal (`USER app`) il peut faire beaucoup moins de dégâts.  
  Pour Trivy : épingler les actions avec leur commit hash complet plutôt qu'un tag `@v1` modifiable, limiter les permissions du token au minimum par job, et ne jamais exposer de secrets inutiles aux actions tierces.

### Difficultés rencontrées
Au début mon curl `/version` répondait `local` au lieu de `0.1.0` parce que mon conteneur Docker Compose de la partie précédente tournait encore sur le port 8000. Il a fallu faire un `docker compose down` pour libérer le port avant de lancer l'image de GHCR.

---

# TP4 : GitOps avec Argo CD

### Objectif
Dans ce dernier TP on a mis en place du vrai GitOps avec un cluster Kubernetes local (Kind) et Argo CD. On a séparé le dépôt de configuration du dépôt applicatif, observé la correction automatique des dérives (`selfHeal`), et automatisé toute la chaîne : un tag `v0.2.0` sur le code met à jour le manifeste dans le dépôt de config et déclenche le déploiement sans aucune commande manuelle sur le cluster.

### Captures d'écran

* **TP4-1 :** Le nœud du cluster Kind au statut `Ready` (`kubectl get nodes`).  
  ![TP4-1](TP4/TP4-1.png)

* **TP4-2 :** Tous les pods Argo CD au statut `Running` et la page de connexion web d'Argo CD.  
  ![TP4-2-1](TP4/TP4-2-1.png)  
  ![TP4-2-2](TP4/TP4-2-2.png)  
  ![TP4-2-3](TP4/TP4-2-3.png)

* **TP4-3 :** L'application `tasks-api` dans Argo CD avec le statut `Synced` et `Healthy` et ses 2 pods.  
  ![TP4-3](TP4/TP4-3.png)

* **TP4-4 :** La commande `curl` sur le port 8081 qui répond la version `0.1.0` déployée dans le cluster.  
  ![TP4-4](TP4/TP4-4.png)

* **TP4-5 :** Le commit passant à `replicas: 3` dans `tasks-config` et les 3 pods visibles dans Argo CD.  
  ![TP4-5](TP4/TP4-5.png)

* **TP4-6 :** La commande `kubectl scale` à 5 pods (capture 1) puis la correction automatique d'Argo CD (`selfHeal`) qui supprime direct les pods en trop pour revenir à 3 (capture 2).  
  ![TP4-6-1](TP4/TP4-6-1.png)  
  ![TP4-6-2](TP4/TP4-6-2.png)

* **TP4-7 :** L'historique Git avec le `revert` dans `tasks-config` et le retour automatique à 2 pods.  
  ![TP4-7-1](TP4/TP4-7-1.png)  
  ![TP4-7-2](TP4/TP4-7-2.png)

* **TP4-8 :** Le workflow `docker.yml` terminé avec tous les jobs au vert, y compris `update-config`.  
  ![TP4-8](TP4/TP4-8.png)

* **TP4-9 :** Le commit automatique de `github-actions[bot]` dans `tasks-config` et Argo CD synchronisé sur `0.2.0`.  
  ![TP4-9-1](TP4/TP4-9-1.png)  
  ![TP4-9-2](TP4/TP4-9-2.png)

* **TP4-10 :** La commande `curl` sur l'API qui répond bien la version `0.2.0` mise à jour.  
  ![TP4-10](TP4/TP4-10.png)

### Réponses aux questions

* **Q1 : C'est quoi un pod ? Un deployment ? Pourquoi un namespace ?**  
  - *Pod :* plus petite unité dans Kubernetes, un ou plusieurs conteneurs qui partagent le même réseau et les mêmes volumes.  
  - *Deployment :* objet qui gère les pods et leurs réplicats, gère les rolling updates sans coupure et les retours en arrière.  
  - *Namespace :* isolation logique dans le cluster pour séparer les projets ou environnements et éviter les conflits de nom.
* **Q2 : Pourquoi sépare-t-on le dépôt de l'application et le dépôt de configuration ?**  
  Pour éviter que la CI tourne en boucle quand elle modifie les manifestes, pour bien séparer les droits des devs (code) et des ops (infrastructures), et pour garder un historique propre et traçable sur chaque dépôt.
* **Q3 : Que signifie `selfHeal` ? Pourquoi le retour arrière est-il simple en GitOps ?**  
  `selfHeal` veut dire qu'Argo CD compare en permanence le cluster avec le dépôt Git : si quelqu'un modifie un truc à la main sur le cluster (par exemple un scale à 5), Argo CD détecte la dérive et remet automatiquement ce qui est écrit dans Git (3 réplicas).  
  Le retour arrière est simple parce que chaque déploiement correspond à un commit dans `tasks-config` : il suffit de faire un `git revert` et de pousser, Argo CD applique l'ancienne version tout seul sans qu'on ait besoin de toucher au cluster.
* **Q4 : Résumez en 5 lignes le chemin d'un tag Git jusqu'au pod. Qui pousse et qui tire ? Différence avec un déploiement classique ?**  
  1. Je pousse le tag `v0.2.0` sur le dépôt applicatif, ce qui déclenche la pipeline GitHub Actions.  
  2. La CI teste le code, construit l'image Docker et la publie sur GHCR avec le tag `0.2.0`.  
  3. Après le test staging et la validation de la prod, le job `update-config` met à jour `deployment.yaml` dans `tasks-config` et commite.  
  4. Argo CD surveille `tasks-config`, voit que le dépôt a changé et que le cluster n'est plus synchronisé.  
  5. Argo CD applique le manifeste et Kubernetes remplace les anciens pods par les nouveaux avec l'image `0.2.0`.  
  *Qui pousse / qui tire :* La CI pousse l'image sur GHCR et le commit dans `tasks-config`, mais ne touche jamais au cluster. C'est Argo CD qui tire la config depuis Git, et Kubernetes qui tire l'image depuis GHCR.  
  *Différence avec la CI/CD classique :* En classique, c'est la pipeline qui a les clés du cluster et fait un `kubectl apply` ou un SSH en direct, donc si quelqu'un modifie le cluster à la main personne ne le voit. En GitOps, le cluster n'est pas ouvert à la CI, Git est la seule source de vérité et les dérives sont corrigées automatiquement.

### Difficultés rencontrées
Pour le test du `selfHeal`, Argo CD a corrigé la dérive tellement vite (moins d'une seconde) que la première fois les pods étaient déjà supprimés quand j'ai lancé `kubectl get pods`. Il a fallu lancer la commande avec `-w` dans un premier terminal avant de faire le `kubectl scale` dans un second terminal pour bien capturer l'événement en direct.

Aussi, lors de la création du token pour le workflow GitHub Actions vers `tasks-config`, j'ai cherché les permissions dans les mauvais menus GitHub (recherche vide sur "Read" au mauvais endroit). Il fallait bien activer les permissions en écriture sur le contenu du dépôt (`Contents: Read and write`) pour que le job `update-config` puisse commiter automatiquement.  
![TP4-diff-token](TP4/TP4-diff-token.png)

---

# Bilan personnel

Ce cours m'a permis de comprendre concrètement tout le cycle d'un projet moderne, de l'écriture du code jusqu'au cluster de production. Ce que j'ai surtout retenu, c'est la puissance de GitHub Actions pour automatiser les tests et la sécurité des images, et le principe du GitOps avec Argo CD où Git devient la seule source de vérité pour le déploiement. Ce qui m'a posé le plus de problèmes au début, c'était la gestion fine des permissions (jetons PAT, droits de workflow) et les pièges bêtes comme l'indentation YAML ou les formats de tags. Si c'était à refaire, je ferais plus attention à bien isoler mes branches de test dès le départ et je penserais à lancer mes surveillances terminal (`-w`) avant d'exécuter des modifications sur Kubernetes.

