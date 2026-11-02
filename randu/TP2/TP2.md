Q1 flake cherche les erreur alor que black reecrit le code plour luis donner un style uniforme

pour voir simplement a quelle etap est l'ereur et pour pouvoir les fair an meme temp

pour etre sur que le code marche sur toutes les versions que les utilisateurs peuvent avoir et voir direct si une version casse quelque chose

on gagne du temps parce que pip reutilise les paquets deja telecharges au lieu de tout retelecharger a chaque run

un fichier produit par le run (ici coverage.xml) qu'on peut telecharger depuis la page du run apres la fin du job

parce que les deux branches ont modifie la meme ligne du CHANGELOG et git sait pas laquelle garder ou s'il faut garder les deux, c'est a nous de choisir

la CI (le workflow CI) qui s'est relancee sur la PR apres le commit de resolution et a refait passer lint + tests
