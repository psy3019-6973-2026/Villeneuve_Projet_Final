"""
Tâches invoke pour le projet abide-fmri.

Reproduire les analyses depuis un clone frais :

  Option A — conda :
    conda env create -f environment.yml
    conda activate abide-fmri
    invoke tache1
    invoke tache2
    invoke tache3

  Option B — venv :
    python -m venv venv_abide
    source venv_abide/bin/activate      # Linux/Mac
    pip install -r requirements-modern.txt
    invoke tache1
    invoke tache2
    invoke tache3

Tâches individuelles :
    invoke tache1        # setup : kernel + téléchargement des données ABIDE
    invoke tache2        # correction du data leakage PCA
    invoke tache3        # correction du data leakage SelectKBest
    invoke visualisation # comparaison des 4 approches
    invoke run           # tache1 + tache2 + tache3 + visualisation
    invoke clean         # supprime les figures (préserve les features cachées)
"""

from pathlib import Path
from invoke import task

ROOT        = Path(__file__).parent
TACHES_DIR  = ROOT / "Taches"
SOURCE_DATA = ROOT / "data"
OUTPUT_DATA = TACHES_DIR / "output"

TACHE2_DIR  = TACHES_DIR / "Tache2_PCA"
TACHE3_DIR  = TACHES_DIR / "Tache3_SelectKBest"


def _env():
    return {
        "SOURCE_DATA_DIR": str(SOURCE_DATA),
        "OUTPUT_DATA_DIR": str(OUTPUT_DATA),
    }


def _nbconvert(c, notebook, env):
    c.run(
        f"jupyter nbconvert --to notebook --execute --inplace {notebook} "
        "--ExecutePreprocessor.timeout=600",
        env=env,
    )


#Tâche 1 — Setup

@task
def tache1(c):
    """Tâche 1 — Setup : enregistrer le kernel et télécharger les données ABIDE."""
    # Enregistrement du kernel Jupyter
    c.run(
        'python -m ipykernel install --user '
        '--name=abide-fmri '
        '--display-name="Python (abide-fmri)"'
    )
    OUTPUT_DATA.mkdir(parents=True, exist_ok=True)
    print("Kernel enregistré.")

    # Téléchargement et extraction des features (ignoré si déjà en cache)
    feat_file = OUTPUT_DATA / "ABIDE_BASC064_features.npz"
    if feat_file.exists():
        print(f"Features déjà en cache : {feat_file}")
        print("Supprimer le fichier manuellement pour forcer une ré-extraction.")
        return
    SOURCE_DATA.mkdir(parents=True, exist_ok=True)
    c.run(
        f"python {TACHES_DIR / 'prepare_data_v2.py'} {SOURCE_DATA} {OUTPUT_DATA}",
        pty=True
    )


# Tâche 2 — Correction data leakage PCA

@task
def tache2(c):
    """Tâche 2 — Correction du data leakage : PCA avant vs dans le pipeline CV."""
    print("Exécution Tâche 2 — PCA...")
    _nbconvert(c, TACHE2_DIR / "Tache_2_pca_pipeline_cv.ipynb", _env())
    print("Tâche 2 terminée.")


# Tâche 3 — Correction data leakage SelectKBest

@task
def tache3(c):
    """Tâche 3 — Correction du data leakage : SelectKBest avant vs dans le pipeline CV."""
    print("Exécution Tâche 3 — SelectKBest...")
    _nbconvert(c, TACHE3_DIR / "Tache_3a_selectkbest_cv.ipynb", _env())
    print("Tâche 3 terminée.")


# Visualisation finale

@task
def visualisation(c):
    """Comparaison des 4 approches — Impact du data leakage."""
    print("Exécution comparaison 4 approches...")
    _nbconvert(c, TACHE3_DIR / "Tache_3b_comparaison.ipynb", _env())
    print("Visualisation terminée.")


# Pipeline complet

@task(pre=[tache1, tache2, tache3, visualisation])
def run(c):
    """Exécuter le pipeline complet : tache1 + tache2 + tache3 + visualisation."""
    print("Toutes les analyses sont terminées.")


# Nettoyage

@task
def clean(c):
    """Supprimer les figures générées (préserve les features cachées)."""
    preserved = {"ABIDE_BASC064_features.npz"}
    removed = []
    for f in OUTPUT_DATA.iterdir():
        if f.name not in preserved and f.is_file():
            f.unlink()
            removed.append(f.name)
    if removed:
        print(f"Supprimé : {', '.join(removed)}")
    print(f"Préservé : {', '.join(preserved)}")
