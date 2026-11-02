Q1 une image c'est le modele fige (le code + les dependances), un conteneur c'est une image qui tourne, on peut lancer plusieurs conteneurs depuis la meme image

le .dockerignore sert a pas copier dans l'image les fichiers inutiles (.git, .venv, docs, cache...) pour que l'image soit plus legere, que le build aille plus vite et pour pas mettre de truc sensible dedans

Q2 accelerer la chose et pouvoir avoir la meme a chaque foi

## Q3 (Partie 3 : Publier l'image depuis le pipeline)

- **Pourquoi `build` attend-il `test` ?**  
  Pour garantir qu'on ne construit et qu'on ne publie jamais une image Docker avec du code cassé ou non validé. Si les tests échouent, le pipeline s'arrête avant de gaspiller des ressources de build et d'exposer une version défaillante sur le registre.

- **Pourquoi éviter le tag `latest` en production ?**  
  Le tag `latest` est mutable (sa cible change à chaque nouveau push). Cela rend les déploiements non reproductibles : on ne sait pas quelle version exacte tourne en production et il est difficile de faire un rollback en cas de problème. Il faut toujours privilégier des tags immuables et traçables comme le hash de commit (`sha-...`) ou un tag sémantique (`0.1.0`).

