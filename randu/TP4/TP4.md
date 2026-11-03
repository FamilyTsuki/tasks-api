Q1 pod = plus petite unite dans k8s, un ou plusieurs conteneurs qui partagent le reseau et les volumes
deployment = objet qui gere les pods et les replicats, fait les rolling updates et les rollbacks
namespace = isolation logique dans le cluster pour separer les projets et eviter les conflits

Q2 on separe le depot app et config pour eviter que la ci tourne en boucle quand elle modifie les manifests, pour separer les droits des devs et des ops, et pour que chaque depot ait un historique propre

Q3 selfHeal = argo cd compare en permanence le cluster avec git, si quelqu'un modifie un truc a la main (genre kubectl scale a 5) il detecte l'ecart et remet automatiquement ce qui est dans git (3 replicas)

le retour arriere est simple parce que chaque deploiement c'est un commit dans tasks-config, il suffit de faire un git revert et de pousser, argo cd applique l'ancienne config tout seul, pas besoin de toucher au cluster et on garde la trace dans l'historique

Q4 chemin d'un git tag jusqu'au pod :
1. je pousse le tag v0.2.0 sur le depot applicatif, ca declenche la pipeline docker.yml
2. la ci lance les tests, build l'image et la publie sur ghcr.io avec le tag 0.2.0
3. apres le deploiement staging et l'approbation de la prod, le job update-config modifie le deployment.yaml de tasks-config avec set-image-tag.sh et pousse le commit
4. argo cd surveille tasks-config, il voit que le depot a change et que le cluster n'est plus pareil (OutOfSync)
5. argo cd applique le nouveau manifeste, kubernetes cree les nouveaux pods avec l'image 0.2.0 et supprime les anciens (rolling update)

qui pousse et qui tire : la ci pousse (push) l'image sur ghcr et le commit dans tasks-config, mais elle touche jamais au cluster. c'est argo cd, qui tourne dans le cluster, qui tire (pull) la config depuis git, et kubernetes qui tire l'image depuis ghcr

difference avec un deploiement ci/cd classique : en classique c'est la pipeline qui se connecte au cluster et deploie elle meme (kubectl apply, ssh...), donc il faut lui donner les acces au cluster et si quelqu'un modifie a la main personne le voit. en gitops la ci a juste besoin d'un token sur le depot de config, git est la seule source de verite, argo cd corrige les derives tout seul (selfHeal) et on a l'historique de tous les deploiements dans les commits, un revert suffit pour revenir en arriere
