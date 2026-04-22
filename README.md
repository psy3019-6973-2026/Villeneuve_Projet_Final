## Description du projet original
### Titre : Using fMRI Data to Predict Autism Diagnoses with Machine Learning

Originalement réalisé par Emily Chen, Andréanne Proulx et Mikkel Schöttner, ce projet vise à classifier des données d'IRMf au repos de la base de données Autism Brain Imaging Data Exchange (ABIDE) afin de prédire la présence ou non d'un diagnostic de trouble du spectre de l'autisme (TSA).

### Données 
Dataset: ABIDE (Autism Brain Imaging Data Exchange)
- Données ouvertes
- 539 participants avec un diagnostic de TSA
- 573 participants contrôles typiques (TD)
- Données multi-sites (plus de 20 sites)
- IRMf au repos prétraitées
- Atlas BASC 64 régions

### Préparation (prepare_data.py)
Le pipeline original comprend :
- Extraction des séries temporelles via l’atlas BASC
- Construction des matrices de corrélation région × région
- Vectorisation des connexions
- Réduction de dimension via PCA (99 % de la variance conservée)
  
### Modèles testés 
- LinearSVC (le plus performant)
- K-Nearest Neighbors
- Decision Tree
- Random Forest

Chacun des modèles sont évaluées par différentes méthodes de validation croisée, les résultats montrent des performances entre 50 à 70 % d'accuracy.

#### Limite et piste future logique d'amélioration selon les auteurs : 
- Effets potentiels liés aux sites d’acquisition
- Absence d’optimisation paramètres

## Pourquoi ce projet ?
Marie ([@MarieFrancois1](https://github.com/MarieFrancois1)) et moi avons choisi ce projet puisqu’il combine neurosciences cognitives et apprentissage automatique autour d’un enjeu clinique important : le diagnostic du trouble du spectre de l’autisme. 

De plus, le fait que le projet soit déjà bien structuré offre un cadre solide pour proposer des améliorations ciblées, nous permettant de consolider nos connaissances en apprentissage automatique appliqué aux données cérébrales.

## Présentation des taches 
### Tâche 1 : Reproductibilité du projet du projet original et automatisation avec invoke 
#### Objectif : S'assurer que le code original fonctionne dans un environnement vierge, moderniser et automatiser la reproduction du projet 
Trouvailles : 
- Les dépendences contenues dans requirements.txt et prepare_data.py du projet original était expiré puisque le projet a été fait en 2020.
  - Conséquences:
                  - Il a fallut moderniser les dépendences : requirements-modern.txt
                  - Il a fallut changer le code prepare_data pour changer l'appel de certaines librairies qui avaient changé de nom: prepare_datav2.py
- Tenter la reproduction
  
##### Confirmation : suite à ces corrections Marie a pu reproduire le projet sans problème et entamer elle meme ses taches. 

### Invoke : 
Puisque les changements ont pris moins de temps que prévu j'ai ajouté la fonction invoke sur toutes mes taches pour automatiser et optimiser la reproductibilité de mon travail.
### Prérequis

- Python 3.10+
- Conda **ou** venv
- environment.yml (créé et ajouté au repo) 

### Installation rapide

J'ai créé les deux options pour rendre la reproductivité accessible aux plus d'utilisateurs possibles en incluant l'option conda, venv avec les commandes en Linux, Mac et Windows

```bash
git clone https://github.com/psy3019-6973-2026/Villeneuve_Projet_Final
cd Villeneuve_Projet_Final

# Option 1: Conda
conda env create -f environment.yml
conda activate abide-fmri

# Option 2: venv
python -m venv venv_abide
source venv_abide/bin/activate  # Windows: venv_abide\Scripts\activate
pip install -r requirements-modern.txt
```
## Structure du projet

```
abide-fmri/
├── Taches/
│   ├── prepare_data_v2.py              # Préparation des données (features brutes)
│   ├── tache_2_pca_pipeline_cv.ipynb   # Correction du data leakage (PCA)
│   ├── tache_3_selectkbest_pipeline_cv.ipynb  # Supervisé vs non-supervisé
│   ├── comparaison_4_approches.ipynb   # Synthèse des 4 approches
│   └── output/                         # Résultats & figures
├── data/                               # Dataset ABIDE (téléchargé automatiquement)
├── environment.yml
└── requirements-modern.txt
```
### Exécution

Une fois l'environnement activé (conda ou venv):

```bash
# Enregistrer le kernel Jupyter 
invoke setup

# Télécharger les données et extraire les features (~ 8h la première fois)
invoke fetch

# Lancer toutes les analyses
invoke run
```
### Autres tâches disponibles

| Commande | Description |
|---|---|
| `invoke setup` | Enregistrer le kernel Jupyter |
| `invoke fetch` | Télécharger les données ABIDE et extraire les features |
| `invoke task2` | Exécuter la Tâche 2 (correction PCA) |
| `invoke task3` | Exécuter la Tâche 3 (leakage SelectKBest) |
| `invoke visualisation` |Exécuter la visualisation comparative des méthodes abordées
| `invoke run` | Exécuter toutes les analyses (`fetch` + `task2` + `task3`) |
| `invoke clean` | Supprimer les outputs générés (préserve les features en cache) |

```bash
invoke --list            # afficher toutes les tâches disponibles
invoke --help <tâche>    # afficher l'aide pour une tâche spécifique
```

> L'extraction des features prend environ 8 heures. Elle est automatiquement ignorée si le fichier `output/ABIDE_BASC064_features.npz` existe déjà.

### Tâche 2 : Correction du pipeline pour éviter le data leakage et test d'une CV de type Stratified GroupKFold
Dans cette tache, le changement apporté concerne la structure du notebook prepare_data.py et l'ajout d'un StandardScaler

#### Problème identifié : 
##### Extraction des features -> PCA (sur tous les sujets) -> Validation croisée (GroupKFold) -> LinearSVC

Dans la version actuelle, la réduction de dimension (PCA) est effectuée dans prepare_data.py avant la validation croisée.

Bien que par la suite, les données sont séparées en folds avec GroupKFold, la PCA est calculée avant la séparation. 
La transformation PCA tient donc compte de tous les participants, incluant ceux qui devraient etre inconnus lors de la validation et du test 
Bien que cette méthode soit non-supervisée et n'utlise pas les labels, elle peut introduire un biais dans l'estimation des performances à cause du moment ou on l'applique. 

De plus, lors du cours de selection de modeles avec Pravish nous avons vu que le 'meilleur des deux mondes' dans une CV etait le stratiied groupkfold donc pour bonifier mon travail et voir l'impact dune CV mieux adaptee aux donnees j'ai decide d'ajouter cette methode aussi 

#### Objectif : 
##### Extraction des features -> Validation croisée (GroupKFold ou StratifiedGroupKFold) 
##### Pipeline pour chaque fold : StandardScaler -> PCA -> LinearSVC 
Garantir que toutes les transformations sont apprises uniquement sur les données d’entraînement à chaque fold.
#### Étapes : 
- Retirer le PCA global du script prepare_data.py
- Utiliser l'outil sklearn.pipeline pour créer une pipeline et y intégrer le StandardScaler et la réduction de dimensions.
- Appliquer cette pipeline à l'intérieur des deux validations croisées choisies
- Recalculer le PCA uniquement sur le training set à chaque fold
- Comparaison des 4 situations pour voir s'il y a une variation significative

```python
# Avant (avec leakage)
X_pca = PCA(0.99).fit_transform(X)  # Tous les sujets!
cv_scores = cross_val_score(LinearSVC(), X_pca, y, cv=gkfold)

# Après (sans leakage)
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(0.99)),
    ('classifier', LinearSVC())
])
cv_scores = cross_val_score(pipeline, X, y, cv=gkfold)
```

#### Remarque :
L'objectif n'est pas nécessairement d'améliorer l'accuracy mais d'avoir une évaluation méthodologiquement plus robuste. Dans ce contexte, le PCA est une étape de prétraitement, mais puisqu’il apprend la structure des données, il doit être recalculé à chaque fold pour éviter un biais d’évaluation.

#### Résultat quantitatif : 
- Il y avait un biais introduit par le leakage (~ 1.3%)
- Le stratified groupKFold baisse un peu la performance mais cest une méthode plus rigoureuse dans ce contexte 
- Ce biais est faible et positif (il améliore la performance du Linear SVC!)
- Apprentissage : un data leakage peut améliorer ou empirer une performance dans une stratégie de réduction de dimensions non-supervisée! (j'étais choquée)

### Tâche 3 : 
#### Tache 3a : Comparaison de stratégies de réduction de dimensions 
#### Tache 3b : Illustrer l'impact de l'utilisation de la méthode supervisée sur le data leakage

#### Situation actuelle :
Le projet original utilise le PCA pour réduire les dimensions. Cette méthode est non supervisée, elle conserve les composantes expliquant le plus de variance globale des données, sans tenir compte du diagnostic. L'idée ici est de comparer une méthode supervisée et une méthode non-supervisée, ainsi que justifier que le script original faisait bel et bien illustration de data leakage. Cette comparaison permettra d’évaluer si une approche supervisée améliore la performance du modèle linéaire, sa stabilité en validation croisée ainsi que l’interprétabilité des connexions. Elle permet aussi d'illustrer l'impact du data leakage

#### Tache 3a 
##### Objectif: 
Comparer cette approche de sélection de features non supervisée à une approche supervisée en gardant le même classifieur final (LinearSVC) et la même validation croisée.

#### Comparaison simplifiée des deux méthodes : 
##### Pipeline 1 (PCA) : 
- Méthode non-supervisée
- Maximise la variance globale
- Transformation des variables en composantes linéaires

##### StandardScaler -> PCA -> LinearSVC

##### Pipeline 2 (sélection supervisée) : 
- Méthode supervisée
- Optimisation de la classification TSA vs controles
- Sélection des 100 connexions les plus importantes

##### StandardScaler -> SelectKBest -> LinearSVC
***
### Résultat : 
Suite à la correction, on remarque que la méthode non-supervisée (PCA) performe mieux dans le 10 GroupKFold que la méthode SelectKBest. 
***
#### Tache 3b 
##### Objectif : implémenter SelectKBest dans l'ancien notebook prepare_data.py avec data leakage puis comparer la différence entre les deux approches 

###### Extraction des features -> PCA (sur tous les sujets) -> Validation croisée (GroupKFold) -> LinearSVC
###### Extraction des features -> SelectKBest (sur tous les sujets) -> Validation croisée (GroupKFold) -> LinearSVC
***
#### Résultat : 
On observe effectivement que le data leakage est minime dans la PCA (2.7%) mais l'impact est DOUBLÉ avec la méthode SelectKBest (5.4%).
***
##### Métriques de comparaison et visualisations
- Accuracy moyenne
- Variabilité entre folds
- Nombre de feautures retenues
  
#### Outils utilisés 
Nilearn : téléchargement ABIDE, extraction de connectivité 

Scikit-learn : pipelines, validation croisée, ML 

Numpy & pandas : manipulation de données

Matplotlib & seaborn : visualisations

#### Sources 
###### Documentation et exemples sur les techniques de sélection de dimensions et leur implémentation
https://scikit-learn.org/stable/modules/cross_validation.html
https://scikit-learn.org/stable/modules/compose.html
https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
https://scikit-learn.org/stable/modules/feature_selection.html
https://scikit-learn.org/stable/auto_examples/feature_selection/
###### Projet original 
Chen E., Proulx A., Schöttner M. (2020). *Using fMRI Data to Predict Autism Diagnoses with Various Machine Learning Models and Cross-Validation Methods*. BrainHack School 2020.
<https://github.com/brainhack-school2020/abide-fmri/tree/master>
###### Données 
ABIDE: http://fcon_1000.projects.nitrc.org/indi/abide/
###### Articles scientifiques 
Nielsen, J. A., Zielinski, B. A., Fletcher, P. T., Alexander, A. L., Lange, N., Bigler, E. D., ... & Anderson, J. S. (2013). Multisite functional connectivity MRI classification of autism: ABIDE results. *Frontiers in Human Neuroscience*, 7, 599.

Anderson, J. S., Patel, V. B., Preedy, V. R., & Martin, C. R. (2014). Cortical underconnectivity hypothesis in autism. *Comprehensive Guide to Autism*, 1457–1471.
###### Licence 
MIT (voir [LICENSE](LICENSE))
###### Licence du projet original 
Creative Commons 
