Q1 flake cherche les erreur alor que black reecrit le code plour luis donner un style uniforme

pour voir simplement a quelle etap est l'ereur et pour pouvoir les fair an meme temp

pour etre sur que le code marche sur toutes les versions que les utilisateurs peuvent avoir et voir direct si une version casse quelque chose

on gagne du temps parce que pip reutilise les paquets deja telecharges au lieu de tout retelecharger a chaque run

un fichier produit par le run (ici coverage.xml) qu'on peut telecharger depuis la page du run apres la fin du job

parce que les deux branches ont modifie la meme ligne du CHANGELOG et git sait pas laquelle garder ou s'il faut garder les deux, c'est a nous de choisir

la CI (le workflow CI) qui s'est relancee sur la PR apres le commit de resolution et a refait passer lint + tests

pour que personne puisse le lire dans les logs, les logs sont visibles par tous ceux qui ont acces au depot (ici il est public) donc le secret serait expose

il est dans l'historique git pour toujours meme si on le supprime apres, tout le monde peut le recuperer donc faut le considerer comme fuite et le changer direct

secret si c'est sensible (token, mot de passe, cle api), variable si c'est pas grave que ce soit visible (nom d'environnement, url, config)

## Explications des 3 pipelines réparés (TP2-10 & TP2-11)

### Pipeline A
- **Quel était le bug :** Erreur d'indentation YAML sur la ligne `- run: pip install -r requirements-dev.txt` (7 espaces au lieu de 6).
- **Comment on l'a trouvé :** GitHub Actions a refusé de lancer le job en indiquant une erreur de syntaxe dans le fichier de workflow (`workflow file issue`).
- **Comment l'éviter :** Utiliser un linter YAML dans l'éditeur (VS Code, etc.) et respecter l'alignement des tirets de liste à 2 espaces.

### Pipeline B
- **Quel était le bug :** Étape de récupération du code manquante (`actions/checkout@v6`).
- **Comment on l'a trouvé :** Dans les logs, l'étape pip install échoue avec `FileNotFoundError: No such file or directory: 'requirements-dev.txt'` car la machine virtuelle démarre vide.
- **Comment l'éviter :** Toujours commencer un job de test ou de build par `actions/checkout`.

### Pipeline C
- **Quel était le bug :** Les numéros de version dans la matrice n'étaient pas entre guillemets (`[3.10, 3.11, 3.12]`). En YAML, `3.10` a été converti en nombre flottant `3.1`.
- **Comment on l'a trouvé :** L'étape `setup-python` a échoué avec l'erreur `Version '3.1' was not found for Ubuntu`.
- **Comment l'éviter :** Toujours entourer de guillemets les versions de logiciels en YAML (`["3.10", "3.11", "3.12"]`).

