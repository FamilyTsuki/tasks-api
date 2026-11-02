Q1 une image c'est le modele fige (le code + les dependances), un conteneur c'est une image qui tourne, on peut lancer plusieurs conteneurs depuis la meme image

le .dockerignore sert a pas copier dans l'image les fichiers inutiles (.git, .venv, docs, cache...) pour que l'image soit plus legere, que le build aille plus vite et pour pas mettre de truc sensible dedans

Q2 accelerer la chose et pouvoir avoir la meme a chaque foi

Q3 pour pas construire et publier une image avec du code casse, si les tests ratent ca s'arrete avant le build

latest change a chaque push donc on sait jamais quelle version tourne vraiment en prod et c'est dur de revenir en arriere, avec un tag fixe (0.1.0 ou le sha) on sait exactement ce qui tourne
