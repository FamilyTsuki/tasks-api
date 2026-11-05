Q1 flake cherche les erreur alor que black reecrit le code plour luis donner un style uniforme

pour voir simplement a quelle etap est l'ereur et pour pouvoir les fair an meme temp

Q2 pour etre sur que le code marche sur toutes les versions que les utilisateurs peuvent avoir et voir direct si une version casse quelque chose

on gagne du temps parce que pip reutilise les paquets deja telecharges au lieu de tout retelecharger a chaque run

un fichier produit par le run (ici coverage.xml) qu'on peut telecharger depuis la page du run apres la fin du job

Q3 pour interdire de casser la branche principale avec du code pas teste, ca force a passer par une PR et a attendre que la CI soit verte

Q4 parce que les deux branches ont modifie la meme ligne du CHANGELOG et git sait pas laquelle garder ou s'il faut garder les deux, c'est a nous de choisir

la CI (le workflow CI) qui s'est relancee sur la PR apres le commit de resolution et a refait passer lint + tests

Q5 pour que personne puisse le lire dans les logs, les logs sont visibles par tous ceux qui ont acces au depot (ici il est public) donc le secret serait expose

il est dans l'historique git pour toujours meme si on le supprime apres, tout le monde peut le recuperer donc faut le considerer comme fuite et le changer direct

secret si c'est sensible (token, mot de passe, cle api), variable si c'est pas grave que ce soit visible (nom d'environnement, url, config)

Q6 (pipelines a reparer) :
- Pipeline A :
  - bug : erreur d'indentation yaml a la ligne 12 (- run decale avec 7 espaces au lieu de 6)
  - comment trouve : github actions a refuse de lancer le job en disant que le fichier workflow etait invalide
  - comment eviter : utiliser un linter yaml dans l'editeur pour voir direct les soucis d'alignement
- Pipeline B :
  - bug : absence de l'etape actions/checkout au debut
  - comment trouve : dans les logs le pip install disait FileNotFoundError sur requirements-dev.txt parce que le runner demarre vide sans le code
  - comment eviter : toujours commencer un job de test par actions/checkout
- Pipeline C :
  - bug : les versions python etaient sans guillemets [3.10, 3.11, 3.12], en yaml 3.10 est devenu 3.1 (nombre flottant)
  - comment trouve : l'etape setup-python a rate en disant que python 3.1 n'existait pas sur le runner
  - comment eviter : toujours mettre des guillemets autour des versions dans les fichiers yaml
