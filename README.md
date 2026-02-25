## Descritpion du projet original
### Using fMRI Data to Predict Autism Diagnoses with Machine Learning

Le projet ABIDE, originalement réalisé par Emily Chen, Andréanne Proulx et Mikkel Schöttner, vise à classifier des données d'IRMf au repos de la base de données ABIDE afin de prédire la présence ou non d'un diagnostic de troules du spectre de l'autisme (TSA)

Les données sont transformées en matrices de connectivité fonctionnelle, puis utilisées dans différents modèles de classification avec diverses stratégies de validation croisée. 

### Données 
Dataset: ABIDE (Autism Brain Imaging Data Exchange)
- Données ouvertes
- Plusieurs centaines de participants
- Données multi-sites (plus de 20 sites)
- IRMf au repos prétraitées
- Atlas BASC 64 régions
- Matrices de connectivité fonctionnelle (64 × 64)
- Variable cible : diagnostic ASD vs TD
### Préparation
Le pipeline original comprend :
- Extraction des séries temporelles via l’atlas BASC
- Construction des matrices de corrélation région × région
- Vectorisation des connexions
- Réduction de dimension via PCA (99 % variance conservée)
### Modèles testés 
- LinearSVC (le plus performant)
- K-Nearest Neighbors
- Decision Tree
- Random Forest
Chacun des modèles sont évaluées par différentes méthodes de validation croisée
Les résultats montrent des performances entre 50 à 70 % d'accuracy
<img width="1060" height="608" alt="image" src="https://github.com/user-attachments/assets/c0b5e72a-4fff-4d77-a4a1-65680f7fd0db" />

###### Image tirée du projet d'Emily Chen, Andréanne Proulx et Mikkel Schöttner

#### Piste future logique d'amélioration selon les auteurs : optimisation des paramètres
## Pourquoi ce projet ?
Marie ([@MarieFrancois1](https://github.com/MarieFrancois1)) et moi avons choisi ce projet puisqu’il combine neurosciences cognitives et apprentissage automatique autour d’un enjeu clinique important : le diagnostic du trouble du spectre de l’autisme.

Le dataset ABIDE étant multi-site, il représente un contexte particulièrement intéressant pour explorer :
- la validation croisée en contexte multi-site
- les effets de site
- la réduction de dimension

Bien que le projet soit déjà bien structuré, il laisse place à des améliorations ciblées du pipeline.

## Tâches choisies
### Tâche 1 : Reproductibilité et infrastructure
#### Dans cette tache, je vais: 
- Reproduire l'expérience complète dans un environnement vierge

- Vérifier que toutes les dépendances fonctionnent correctement

- Identifier les problèmes de chemins ou d'installation (s'il y a lieu)

- Documenter les étapes nécessaires si des étapes s'ajoutent dans le README 

Cette étape est cruciale puisque les tâches suivantes impliquent des modifications méthodologiques du pipeline.

### Tâche 2 : Correction du pipeline pour éviter le data leakage
Dans cette tache, le changement apporté concerne la structure du pipeline prepare_data.py
##### Problème identifié :
Dans la version actuelle, la réduction de dimension (PCA) est effectuée dans prepare_data.py avant la validation croisée.

Bien que par la site, les donéées sont séparées en folds avec GroupKFold, la PCA est calculée avant la séparation. 
La transformation PCA tient donc compte de tous les participants, incluant ceux qui devraient etre inconnus lors de la validation et du test 
Bien que cette méthode soit non-supervisé et n'utlise pas les labels, elle peut introduire un biais dans l'estimation des performances à cause du moment ou on l'applique. 

##### Objectif : 
Garantir que toutes les transformations sont apprises uniquement sur les données d’entraînement à chaque fold.
#### Étapes : 
- Retirer le PCA global du script prepare_data.py
- Utiliser l'outil sklearn.pipeline pour créer une pipeline et y intégrer la réduction de dimensions.
- Appliquer cette pipeline à l'intérieur de la validation croisée.
- Recalculer le PCA uniquement sur le training set à chaque fold
- Comparaison des deux méthodes pour voir s'il y a une variation significative

#### Remarque :
L'objectif n'est pas nécessairement d'améliorer l'accuracy mais d'avoir une évaluation méthodologiquement plus robuste. 

### Tâche 3 : Comparaison de stratégies de réduction/sélection de dimensions

#### Situation actuelle :
Le projet original utilise le PCA pour réduire les dimensions. Cette méthode est non supervisée, elle conserve les composantes expliquant le plus de variance globale des données, sans tenir compte du diagnostic.  

#### Objectif: 
Comparer cette approche de sélection de features non supervisée à une approche supervisée en gardant le même classifieur final (LinearSVC) et la même validation croisée.

<img width="340" height="368" alt="image" src="https://github.com/user-attachments/assets/c521a140-7278-4f97-81f7-342dbc46e442" />

###### Image tirée du projet d'Emily Chen, Andréanne Proulx et Mikkel Schöttner
#### Comparaison simplifiée des deux méthodes : 
##### Pipeline 1 (PCA) : 
- Méthode non-supervisée
- Maximise la variance globale
- Transformation des variables en composantes linéaires

##### StandardScaler -> PCA -> LinearSVC

##### Pipeline 2 (sélection supervisée) : 
- Méthode supervisée
- Optimisation de la classification TSA vs controles
- Sélection des connexions les plus pertinentes
- Coefficients des variables non informatives forcées à zéro
- Sélection multivariée

##### StandardScaler -> SelectFromModel(LogisticRegression L1) -> LinearSVC
###### Remarque : la régression logistique L1 est seulement utiliséee pour sélectionner les connexions les plus pertinentes, le classifieur final reste LinearSVC

##### Pourquoi la comparaison est pertinente 
Cette comparaison permettra d’évaluer si une approche supervisée améliore la performance du modèle linéaire, sa stabilité en validation croisée ainsi que l’interprétabilité des connexions.
##### Métriques de comparaison et visualisations
- Accuracy moyenne
- Variabilité entre folds
- Nombre de feautures retenues
##### Tache Bonus...Si le temps le permet...
- Optimisation de paramètres et comparaison de performances optimisées

##### Sources 
###### Documentation et exemples sur les techniques de sélection de dimensions et leur implémentation
https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectFromModel.html
https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
https://scikit-learn.org/stable/modules/feature_selection.html
https://scikit-learn.org/stable/auto_examples/feature_selection/plot_select_from_model_diabetes.html
###### Projet original 
<https://school.brainhackmtl.org/project/abide-fmri/>
<https://github.com/brainhack-school2020/abide-fmri/tree/master>

