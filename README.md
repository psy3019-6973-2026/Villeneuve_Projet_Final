# Villeneuve_Projet_mi-session
Présentation des taches envisagées sur le projet ABIDE 
## 1) Descritpion du projet original
Le projet ABIDE, originalement réalisé par Emily Chen, Andréanne Proulx et Mikkel Schöttner, vise à classifier des données d'IRMf au repos de la base de données ABIDE afin de prédire la présence ou non d'un diagnostic de troules du spectre de l'autisme (TSA)

Les données sont transformées en matrices de connectivité fonctionnelle, puis utilisées dans différents modèles de classification avec diverses stratégies de validation croisée. 

## 2) Pourquoi ce projet ?
Le projet ABIDE nous a intéressées parce qu’il pose une question ambitieuse :
peut-on identifier, à partir de données d’IRMf de repos, des patterns de connectivité associés au diagnostic de TSA ?

Bien que le projet soit déjà bien construit, il offre un cadre idéal pour examiner à la fois la performance des modèles et leur rigueur méthodologique. Nous avons donc vu une occasion d’aller au-delà de l’exploration initiale, en structurant davantage l’évaluation et en questionnant certaines étapes du pipeline.

## 3) Taches choisies
### Tache 1 : Reproductibilité et infrastructure
#### Dans cette tache, je vais: 
-> Reproduire l'expérience complète dans un environnement vierge

-> Vérifier que toutes les dépendances fonctionnent correctement

-> Identifier les problèmes de chemins ou d'installation (s'il y a lieu)

-> Documenter les étapes nécessaires si des étapes s'ajoutent dans le README 

Cette étape est cruciale puisque les tâches suivantes impliquent des modifications méthodologiques du pipeline.
### Tache 2 : Modification du pipeline pour éviter le data leakage
Dans cette tache, le changement apporté concerne la structure du pipeline prepare_data.py
#### État actuel : 
La réduction de dimensions (PCA) est appliquée sur l'ensemble des sujets, y compris ceux qui devraient etre considérés comme inconnus lors de la validation croisée. 

Bien que cette méthode soit non-supervisé et n'utlise pas les labels, elle peut introduire un biais dans l'estimation des performances, puisqu'elle tient compte de tous les sujets. 

#### Modification voulue : 
-> Utiliser l'outil sklearn.pipeline pour créer une pipeline et y intégrer la réduction de dimensions, puis, appliquer cette pipeline à la validation croisée. 
-> Recalculer le PCA uniquement sur le training set à chaque fold
#### Résultat attendu : 
-> Les transformations sont appliquées uniquement sur le training set et la valeur PCA dans l'entrainement est celle du set d'entrainement et non du set complet. 
-> Comparaison des deux méthodes pour voir s'il y a une variation significative

#### Remarque :
L'objectif n'est pas nécessairement d'améliorer l'accuracy mais d'avoir une évaluation méthodologiquement plus robuste. 

### Tache 3 : Comparer plusieurs modèles de manière systématique 

#### Situation actuelle :
Le projet utilise le PCA pour réduire les dimensions. Cette méthode est non supervisée, elle conserve les composantes expliquant le plus de variance globale des données, sans tenir compte du diagnostic.  

#### Proposition: 
Nous proposons de comparer cette approche non supervisée à une approche supervisée intégrée : une régression logistique avec régularisation L1

Cette approche sera appliquée au modèle linéaire, puisque les résultats initiaux montrent que LinearSVC est le classifieur le plus performant.

#### Différences entre les deux méthodes : 
##### PCA : 
- Méthode non-supervisée
- Maximise la variance globale
- Transformation des variables en composantes linéaires
##### Classifieur linéaire avec régularisation L1: 
- Méthode supervisée
- Optimisation de la classification TSA vs controles
- Sélection des connexions les plus pertinentes
- Coefficients des variables non informatives forcées à zéro
- Sélection multivariée
##### Objectif de la comparaison
Cette comparaison permettra d’évaluer si une approche supervisée intégrée améliore la performance du modèle linéaire, sa stabilité en validation croisée ainsi que l’interprétabilité des connexions.

L’objectif est de déterminer si une réduction basée sur la variance globale (PCA) est aussi pertinente qu’une sélection parcimonieuse directement alignée avec l’objectif de classification

Des visualisations comparatives (scores, distributions) seront ajoutées à cette analyse. 

###### Sources 
https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression

