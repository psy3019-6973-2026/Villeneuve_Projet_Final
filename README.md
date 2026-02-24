# Villeneuve_Projet_mi-session
Présentation des taches envisagées sur le projet ABIDE 
## 1) Descritpion du projet original
Le projet ABIDE, originalement fait par xyz vise à classifier des données d'IRMf au repos de la base de données ABIDE afin de prédire la présence ou non d'un diagnostic de troules du spectre de l'autisme (TSA)

Les données sont transformées en matrices de connectivité fonctionnelle, puis utilisées dans différents modèles de classification avec diverses stratégies de validation croisée. 

## 2) Pourquoi ce projet ?
Ce projet a piqué ma curiosité car je m'intéresse aux diagnostics d'autisme et ce projet permet de voir s'il y a des bases en neuroimagerie qui permettraient de discriminer ces diagnostiques. 

## 3) Taches choisies
### Tache 1 : Reproductibilité et infrastructure
#### Dans cette tache je vais: 
-> Reproduire l'expérience complète dans un environnement vierge
-> Vérifier que toutes les dépendances fonctionnent correctement
-> Identifier les problèmes de chemins ou d'installation (s'il y a lieu)
-> Documenter les étapes nécessaires si des étapes s'ajoutent dans le README 
Cette étape est cruciale car le reste des taches nécessitent des manipulations et modification du projet. 
### Tache 2 : Modification du pipeline pour éviter le data leakage
-> Dans cette tache, le changement apporté concerne la structure du pipeline prepare_data.py
#### Actuellement : 
La réduction de dimensions (PCA) est appliquée sur l'ensemble des sujets, y compris ceux qui devraient etre considérés comme inconnus lors de la validation croisée. 
Bien que cette méthode soit non-supervisé et n'utlise pas les labels, elle peut introduire un biais puisqu'elle tient compte de tous les sujets. 

#### Modification : 
-> Utiliser l'outil sklearn.pipeline pour créer une pipeline et y intégrer la réduction de dimensions 
-> Appliquer cette pipeline à la validation croisée 
#### Résultat attendu : 
-> Les transformations sont appliquées uniquement sur le training set et la valeur PCA dans l'entrainement est celle du set d'entrainement et non du set complet. 
-> Comparaison des deux méthodes pour voir s'il y a une variation significative

#### Remarque :
L'objectif n'est pas nécessairement d'améliorer l'accuracy mais d'avoir une évaluation méthodoloiquement valide et robuste et une estimation plus honnete des performances. 


### Tache 3 : Comparer plusieurs modèles de manière systématique 

#### Actuellement :
-> Le projet utilise le PCA pour réduire les dimensions. Cette méthode est non supervisée, elle conserve les composantes expliquant le plus de variance globale. 

#### Proposition: 
-> J'aimerais comparer cette approche non-supervisée à une approche supervisée, le SelectKBest 

#### Différences : 
##### PCA : 
Réduit la dimension selon la variance des données, sans tenir compte du diagnostic 
##### SelectKBest: 
Sélectionne les connexions les plus associées au diagnostic. 

En faisant cette comparaison, il sera possible d'évaluer si une sélection supervisée améliore la performance, la stabilité ou l'interprétabilité des modèles, surtout dans un contexte de diagnostic. 

Des visualisations comparatives (scores, distributions) seront ajoutées à cette analyse. 
