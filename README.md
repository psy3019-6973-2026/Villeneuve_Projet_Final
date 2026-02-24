# Villeneuve_Projet_mi-session
Présentation des taches envisagées sur le projet ABIDE 
# 1) Descritpion du projet original
# 2) Pourquoi ce projet ?
# 3) Taches choisies
## Tache 1 : Reproductibilité et infrastructure
-> Dans cette tache je vais reproduire l'expérience d'un environnement vierge et m'assurer que le tout fonctionne et est reproductible, puis documenter si des changements doivent etre apportés 
## Tache 2 : Modifier un pipeline d’apprentissage automatique 
-> Dans cette tache, le changement apporté concerne la structure du pipeline prepare_data.py
### Actuellement : 
La réduction de features est appliquée sur L'ENSEMBLE des données, puis cette valeur est utilisée dans l'entrainement des différents modèles, cependant, le fait que la mesure PCA soit calculé sur l'ensemble des données donne potentiellement un avantage aux modèles et méthodologiquement expose les données à du data leakage. 
changer ceci permet donc d'avoir une approche méthodologique plus robuste en séparant les données AVANT de réduire les features et puis faire le tout en parallèle. 
Cela ne vise pas nécessairement à améliorer la performance des modèles, cette manoeuvre pourrait meme baisser leur performance, l'objectif est vraiment apporter une moification méthodologique pour respecter les normes. 
### Après modification : 


## Tache 3 : Comparer plusieurs modèles de manière systématique 
Le deuxième objectif est de comparer deux techniques de réduction de features, actuellement, ce qui est utilisé est le PCA, qui est une technique non-supervisée, qui extrait les plus grandes sources de variations et les garde pour les features d'intéret. 
J'aimerais comparer cette technique avec une technique supervisée, soit selectkbest qui choisit non seulement les données les plus variables mais aussi les plus pertinentes comme un diagnostique. Cela est surtout pertinent à cause du contexte de l'étude qui vise à catégoriser les IRMf selon la présence ou non de diagnostique de TSA 
