Q1 une image c'est le modele fige (le code + les dependances), un conteneur c'est une image qui tourne, on peut lancer plusieurs conteneurs depuis la meme image

le .dockerignore sert a pas copier dans l'image les fichiers inutiles (.git, .venv, docs, cache...) pour que l'image soit plus legere, que le build aille plus vite et pour pas mettre de truc sensible dedans

Q2 accelerer la chose et pouvoir avoir la meme a chaque foi

Q3 pour pas construire et publier une image avec du code casse, si les tests ratent ca s'arrete avant le build

latest change a chaque push donc on sait jamais quelle version tourne vraiment en prod et c'est dur de revenir en arriere, avec un tag fixe (0.1.0 ou le sha) on sait exactement ce qui tourne

Q4 l'image c'est toujours la meme partout (ma machine, la ci, la prod) avec les memes dependances, alors que le code de ma machine depend de ce que j'ai installe, avec une version on sait exactement ce qui tourne et on peut revenir a une ancienne facilement

Q5 un test de fumee c'est un test rapide juste apres le deploiement (genre un curl sur /health) pour verifier que l'app demarre et repond, si ca rate on sait direct que le deploiement est casse

pour qu'une personne verifie avant que ca parte en prod, parce que la prod c'est ce que les vrais utilisateurs utilisent donc une erreur coute cher, ca evite de deployer un truc pas voulu juste parce que la pipeline est verte

Q6 ne jamais executer en root parce que si un pirate trouve une faille dans l'application, il est root dans le conteneur et s'il arrive a s'en echapper (container escape), il a les pleins pouvoirs sur la machine hote, alors qu'en utilisateur simple (app) ses droits sont tres limites

bonnes pratiques suite a la compromission de l'action trivy :
- epingler les actions avec leur commit hash (sha) complet au lieu d'un tag comme @v1 qui peut etre modifie par un attaquant
- limiter les permissions du GITHUB_TOKEN au strict minimum par job (ex: contents read)
- ne jamais passer de secrets sensibles aux actions tierces si elles n'en ont pas absolument besoin


Q6 si quelqu'un trouve une faille dans l'app il a tous les droits dans le conteneur et ca peut l'aider a sortir sur la machine hote, avec un utilisateur normal (USER app dans le dockerfile) il peut faire beaucoup moins de degats
