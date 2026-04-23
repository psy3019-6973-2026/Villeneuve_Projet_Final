# Projet ABIDE : Prédiction du TSA à partir de l'IRMf au repos

**Cours :** PSY3019

**Nom :** Eva Villeneuve

**Projet original :** [Chen, Proulx & Schöttner — BrainHack School 2020](https://github.com/brainhack-school2020/abide-fmri) 

**Base de données :** [ABIDE (Autism Brain Imaging Data Exchange)](http://fcon_1000.projects.nitrc.org/indi/abide/)
 
---

## Présentation du projet
 
Ce projet reproduit et améliore le pipeline de classification du [Brainhack School 2020](https://github.com/brainhack-school2020/abide-fmri), dont l'objectif est de prédire un diagnostic de trouble du spectre de l'autisme (TSA) à partir de données d'IRM fonctionnelle de repos (IRMf). 
### Pourquoi ce projet ?
[Marie](https://github.com/MarieFrancois1) et moi avons choisi ce projet puisqu’il combine neurosciences cognitives et apprentissage automatique autour d’un enjeu clinique important : le diagnostic du trouble du spectre de l’autisme. 

De plus, le fait que le projet soit déjà bien structuré offre un cadre solide pour proposer des améliorations ciblées, nous permettant de consolider nos connaissances en apprentissage automatique appliqué aux données cérébrales.
### Données 
Le dataset ABIDE regroupe des données de 871 participants provenant de 20 sites d'acquisition différents (403 contrôles, 468 ASD). Les données sont prétraitées et téléchargées automatiquement via `nilearn`.

### Pipeline de base
Les features sont extraites à partir des séries temporelles de 64 régions cérébrales définies par l'atlas BASC, à l'aide d'un `NiftiLabelsMasker`. Une matrice de connectivité fonctionnelle vectorisée est calculée par sujet, produisant une matrice de features de dimension **(871, 2016)**.

La classification est réalisée par un **LinearSVC** (`max_iter=10000`), évalué en **GroupKFold** à 10 splits groupés par site d'acquisition, afin de simuler la généralisation à de nouveaux sites.

### Structure du projet
 
```
Villeneuve_Projet_Final/
├── Taches/
│   ├── Tache2_PCA/
│   │   └── Tache_2_pca_pipeline_cv.ipynb        # Correction du data leakage — PCA dans CV
│   └── Tache3_SelectKBest/
│       ├── Tache_3a_selectkbest_cv.ipynb        # SelectKBest corrigé (dans CV)
│       └── Tache_3b_comparaison.ipynb           # Démonstration du leakage + comparaison
├── prepare_data_v2.py                           # Extraction des features (brutes, sans PCA)
├── tasks.py                                     # Tâches invoke
├── invoke.yaml                                  # Configuration invoke (chemins des répertoires)
├── environment.yml                              # Environnement conda
├── requirements-modern.txt                      # Dépendances pour venv
└── LICENSE
```
 
---

## Tâche 1 : Reproductibilité et automatisation avec `invoke`
 
### Problème identifié
 
Le projet original reposait sur un environnement `venv` avec un `requirements.txt` figé datant de 2020. Plusieurs dépendances étaient expirées et certains appels à `nilearn` utilisaient des chemins anciens, rendant le code non fonctionnel dans un environnement moderne. L'exécution nécessitait également plusieurs étapes manuelles.
  
### Changements apportés
 
| | Original | Actuel |
|---|---|---|
| Environnement | `venv` + `requirements.txt` | `conda` + `environment.yml` **ou** `venv` + `requirements-modern.txt` |
| Exécution des tâches | Étapes manuelles | `invoke` + `tasks.py` |
| Exécution des notebooks | JupyterLab (interactif) | `nbconvert` (automatique via `invoke run`) |
| Import nilearn | `nilearn.input_data` | `nilearn.maskers` |
| API atlas | `fetch_atlas_basc_multiscale_2015()` | `fetch_atlas_basc_multiscale_2015(version="sym", resolution=64)` |
 
Les scripts ont été mis à jour dans `prepare_data_v2.py` pour être compatibles avec les deux options d'environnement. Suite à ces corrections, [Marie](https://github.com/MarieFrancois1) a pu reproduire le projet sans problème.

### Fichiers ajoutés

| Fichier | Rôle |
|---|---|
| `environment.yml` | Définition de l'environnement conda (toutes les dépendances) |
| `requirements-modern.txt` | Dépendances mises à jour pour un environnement venv |
| `invoke.yaml` | Configuration du projet (chemins des répertoires) — template [airoh](https://github.com/airoh-pipeline/airoh-template/tree/main) |
| `tasks.py` | Définition des tâches `invoke` |
 
> Ces fichiers sont placés à la racine du dépôt pour faciliter l'installation, mais ont été créés dans le cadre de cette tâche.

### Installation et reproduction
 
Cloner d'abord le dépôt :
 
```bash
git clone -b main https://github.com/psy3019-6973-2026/Villeneuve_Projet_Final
cd Villeneuve_Projet_Final
```
**Ici la commande git clone -b main est utilisee pour seulement cloner la main branche**

Deux options sont ensuite disponibles pour configurer l'environnement :
 
---
 
#### Option A : conda
 
**Prérequis :** [Miniconda](https://docs.conda.io/en/latest/miniconda.html) ou [Anaconda](https://www.anaconda.com/)
 
```bash
conda env create -f environment.yml
conda activate abide-fmri
```
 
#### Option B : venv (sans conda)
 
```bash
# Linux / macOS
python -m venv venv_abide
source venv_abide/bin/activate
pip install -r requirements-modern.txt
 
# Windows
python -m venv venv_abide
venv_abide\Scripts\activate
pip install -r requirements-modern.txt
```
 
---
 
Une fois l'environnement activé :
 
```bash
# Enregistrer le kernel et télécharger les données ABIDE (~8h la première fois)
invoke tache1
 
# Lancer toutes les analyses
invoke run
```
 
> L'extraction des features prend environ 8 heures. Elle est automatiquement ignorée si le fichier `Taches/output/ABIDE_BASC064_features.npz` existe déjà.
 
### Commandes disponibles
 
| Commande | Description |
|---|---|
| `invoke tache1` | Enregistrer le kernel Jupyter et télécharger les données ABIDE |
| `invoke tache2` | Exécuter la Tâche 2 (correction PCA) |
| `invoke tache3` | Exécuter la Tâche 3 (leakage SelectKBest) |
| `invoke visualisation` | Exécuter la comparaison des approches (Tâche 3b) |
| `invoke run` | Exécuter le pipeline complet (`tache1` + `tache2` + `tache3` + `visualisation`) |
| `invoke clean` | Supprimer les outputs générés (préserve les features en cache) |
 
```bash
invoke --list             # afficher toutes les tâches disponibles
invoke --help <tâche>     # afficher l'aide pour une tâche spécifique
```
 
---
## Tâche 2 : Correction méthodologique PCA et StratifiedGroupKFold
 
### Problème identifié
 
Dans le pipeline original, la réduction de dimensionnalité par **PCA** était appliquée globalement sur l'ensemble des sujets *avant* la validation croisée.
 
```
Tous les sujets → PCA → CV split → LinearSVC
```
 
Cela constitue une forme de **data leakage** : les axes de projection PCA sont calculés à partir de l'information de tous les sujets, y compris ceux qui devraient être inconnus au moment de l'évaluation. Parce que la PCA est une méthode **non-supervisée** (elle n'utilise pas les labels de classe), le biais introduit reste faible — mais la pratique demeure méthodologiquement incorrecte.
 
De plus, le projet original utilisait un `GroupKFold` standard. Le `StratifiedGroupKFold` (selon le cours sur la sélection de modèles) constitue une meilleure option dans ce contexte, car il garantit simultanément que les groupes (sites) ne se chevauchent pas entre les folds *et* que la proportion ASD/contrôles est équilibrée dans chaque fold, ce qui est décrit comme le « meilleur des deux mondes » pour ce type de données.
 
### Corrections appliquées
 
**1. PCA intégrée dans la validation croisée** via un `sklearn.pipeline.Pipeline` :
 
```
CV split
└─> Pour chaque fold :
      PCA(99%)        → fit sur train, transform train+test
      LinearSVC       → fit sur train, score sur test
```
 
**2. Comparaison de deux stratégies de validation croisée :**
 
```python
# Avant (avec leakage)
X_pca = PCA(0.99).fit_transform(X)  # Appliqué sur tous les sujets
cv_scores = cross_val_score(LinearSVC(), X_pca, y, cv=GroupKFold())
 
# Après (sans leakage)
pipeline = Pipeline([
    ('pca', PCA(0.99)),
    ('classifier', LinearSVC(max_iter=10000))
])
cv_scores_gkf  = cross_val_score(pipeline, X, y, cv=GroupKFold())
cv_scores_sgkf = cross_val_score(pipeline, X, y, cv=StratifiedGroupKFold())
```
 
### Fichiers
 
| Fichier | Description |
|---|---|
| `prepare_data_v2.py` | Extraction des features sans PCA — retourne les features brutes en 2016 dimensions |
| `Taches/Tache2_PCA/Tache_2_pca_pipeline_cv.ipynb` | Notebook comparant les 4 scénarios (2 CV × leakage/corrigé) |
 
`prepare_data_v2.py` se distingue du script original par la suppression du bloc PCA (fit + transform), retournant les features brutes `(X, y)` en 2016 dimensions au lieu des features réduites.
 
### Résultats
 
| Approche | CV | Accuracy moyenne |
|---|---|---|
| PCA avant CV (leakage) | GroupKFold | 63.6% |
| PCA avant CV (leakage) | StratifiedGroupKFold | 62.8% |
| PCA dans CV (corrigé) | GroupKFold | **65.3%** |
| PCA dans CV (corrigé) | StratifiedGroupKFold | 64.7% |

 <img width="1262" height="489" alt="image" src="https://github.com/user-attachments/assets/c921b89d-1ef8-4ddf-b99b-ac31c0d560a3" />

### Interprétation
 
La correction produit une accuracy légèrement **plus élevée** dans les deux types de CV (+1.7% pour GKF, +1.9% pour SGKF). Cela s'explique par le fait que fitter la PCA sur un plus petit set d'entraînement retient moins de composantes (~538 vs 577), ce qui équivaut à une régularisation plus forte et améliore la généralisation à de nouveaux sites.
 
Le `StratifiedGroupKFold` donne une accuracy légèrement plus basse que le `GroupKFold` standard, ce qui est attendu : en imposant un équilibre des classes dans chaque fold, on obtient une évaluation plus rigoureuse mais légèrement plus pessimiste.La différence est cependant négligeable (<1%) pour ABIDE, qui est un dataset relativement équilibré (~46/54% ASD/contrôles)
 
L'enjeu principal n'est pas la magnitude de ces écarts, mais le **principe méthodologique** : toute transformation qui apprend depuis les données doit être fittée *exclusivement* sur le fold d'entraînement. Le contraste avec la Tâche 3 l'illustre clairement.
 
---
 
## Tâche 3 : Data leakage avec `SelectKBest`, essai d'une nouvelle méthode de réduction de features supervisée et démonstration du data leakage 
Cette tâche est divisée en deux parties : **3a** compare PCA et SelectKBest dans des pipelines correctement implémentés, et **3b** démontre et quantifie l'impact du data leakage avec une méthode supervisée.
 
### Tâche 3a : Comparaison PCA vs SelectKBest (pipelines corrigés)
 
#### Objectif
 
Comparer une méthode de réduction de dimensionnalité **non-supervisée** (PCA) à une méthode **supervisée** (SelectKBest), en gardant le même classifieur (LinearSVC) et la même validation croisée (GroupKFold, 10 splits), avec les deux méthodes correctement intégrées dans un pipeline. J'étais curieuse de savoir comment un changement de méthode de réduction de dimensionnalité affectait la performance. 
 
#### Pipelines comparés
 
 
```
pipeline = Pipeline([
    ('pca', PCA(0.99)),
    ('classifier', LinearSVC(max_iter=10000))
])
pipeline = Pipeline([
    ('selector', SelectKBest(f_classif, k=100)),
    ('clf',      LinearSVC(max_iter=10000))
])

```
 
`SelectKBest(f_classif, k=100)` utilise un test ANOVA F pour sélectionner les 100 connexions fonctionnelles les plus discriminantes entre ASD et contrôles.
 
#### Fichier
 
| Fichier | Description |
|---|---|
| `Taches/Tache3_SelectKBest/Tache_3a_selectkbest_cv.ipynb` | Comparaison PCA vs SelectKBest dans CV (pipelines corrigés) |
 
---
 
### Tâche 3b : Démonstration du leakage supervisé
 
#### Objectif
 
Démontrer ce qui arrive si une méthode de réduction supervisée (`SelectKBest`) est appliqué sur l'ensemble des données *avant* la validation croisée :
 
```
Tous les sujets → SelectKBest(f_classif, y) → CV split → LinearSVC
```
 
#### Pipeline comparés
 
```

Approche 1 — PCA avant CV (leakage)
X_pca = PCA(0.99).fit_transform(X)
scores_pca_leakage = cross_val_score(LinearSVC(max_iter=10000), X_pca, y, groups=groups, cv=gkf, n_jobs=-1)

Approche 2 — PCA dans CV (corrigé)
scores_pca_corrected = cross_val_score(
    Pipeline([("pca", PCA(0.99)), ("clf", LinearSVC(max_iter=10000))]),
    X, y, groups=groups, cv=gkf, n_jobs=-1)

Approche 3 — SelectKBest avant CV (leakage)
X_kbest = SelectKBest(f_classif, k=100).fit_transform(X, y)
scores_kbest_leakage = cross_val_score(LinearSVC(max_iter=10000), X_kbest, y, groups=groups, cv=gkf, n_jobs=-1)

Approche 4 — SelectKBest dans CV (corrigé)
scores_kbest_corrected = cross_val_score(
    Pipeline([("selector", SelectKBest(f_classif, k=100)), ("clf", LinearSVC(max_iter=10000))]),
    X, y, groups=groups, cv=gkf, n_jobs=-1)

```

#### Fichier
 
| Fichier | Description |
|---|---|
| `Taches/Tache3_SelectKBest/Tache_3b_comparaison.ipynb` | Démonstration du leakage supervisé, correction et comparaison des 4 approches |
 
#### Résultats
 
| Approche | Accuracy moyenne |
|---|---|
| SelectKBest avant CV (leakage) | 64.8% |
| SelectKBest dans CV (corrigé) | **61.0%** |
| Différence | **−3.8%** |

<img width="1263" height="519" alt="image" src="https://github.com/user-attachments/assets/021c055c-c9fb-499f-8d91-eb1e1679e11b" />

 
#### Pourquoi le leakage supervisé est plus grave
 
| Méthode | Type | Direction de l'effet | Magnitude |
|---|---|---|---|
| PCA (Tâche 2) | Non-supervisée | Imprévisible (+ ou −) | ~1–2% |
| SelectKBest (Tâche 3) | Supervisée | **Toujours à la hausse** | ~3.8% |
 
Avec la PCA, le leakage est indirect : connaître la structure de variance des sujets test n'aide pas directement à les classifier. L'effet est faible et peut aller dans les deux sens, dans ce cas ci, intégrer PCA dans un pipeline séparé était bénéfique.
 
Avec `SelectKBest`, le leakage est direct : les features sont choisies précisément parce qu'elles séparent bien ASD et contrôles sur **l'ensemble** des données, y compris les sujets test. Le modèle dispose d'une information qu'il ne devrait pas avoir, et cet avantage artificiel gonfle systématiquement les performances estimées.
 
---

  
## Outils utilisés
 
- **[nilearn](https://nilearn.github.io/)** — téléchargement ABIDE, extraction de connectivité fonctionnelle
- **[scikit-learn](https://scikit-learn.org/)** — pipelines, validation croisée, modèles ML
- **[numpy](https://numpy.org/) & [pandas](https://pandas.pydata.org/)** — manipulation de données
- **[matplotlib](https://matplotlib.org/) & [seaborn](https://seaborn.pydata.org/)** — visualisations
- **[invoke](https://www.pyinvoke.org/)** — automatisation des tâches (template [airoh](https://github.com/airoh-pipeline/airoh-template/tree/main))
- Assistance pour debug et structurer le repo github : [Claude](https://claude.ai) (Anthropic)
---

## Sources
 
### Documentation technique

- Cross-validation : https://scikit-learn.org/stable/modules/cross_validation.html
- Pipelines scikit-learn : https://scikit-learn.org/stable/modules/compose.html
- PCA : https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
- Sélection de features : https://scikit-learn.org/stable/modules/feature_selection.html
- Exemples de sélection de features : https://scikit-learn.org/stable/auto_examples/feature_selection/

### Projet original
 
Chen E., Proulx A., Schöttner M. (2020). *Using fMRI Data to Predict Autism Diagnoses with Various Machine Learning Models and Cross-Validation Methods.* BrainHack School 2020.  
https://github.com/brainhack-school2020/abide-fmri/tree/master

###### Données 
ABIDE: http://fcon_1000.projects.nitrc.org/indi/abide/
###### Articles scientifiques 
Nielsen, J. A., Zielinski, B. A., Fletcher, P. T., Alexander, A. L., Lange, N., Bigler, E. D., ... & Anderson, J. S. (2013). Multisite functional connectivity MRI classification of autism: ABIDE results. *Frontiers in Human Neuroscience*, 7, 599.

Anderson, J. S., Patel, V. B., Preedy, V. R., & Martin, C. R. (2014). Cortical underconnectivity hypothesis in autism. *Comprehensive Guide to Autism*, 1457–1471.
###### Licence 
MIT (voir [LICENSE](LICENSE))
Projet original sous licence Creative Commons (CC0 1.0 Universal)
