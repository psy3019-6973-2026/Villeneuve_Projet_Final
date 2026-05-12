#!/usr/bin/env python
"""
Préparation des données ABIDE pour la classification de l'autisme.

Ce script télécharge le dataset ABIDE (si nécessaire), extrait les features
de connectivité fonctionnelle (matrices de corrélation, atlas BASC 64 régions),
et retourne les features brutes sans réduction de dimensionnalité.

Contrairement à prepare_data.py (original), la PCA est intentionnellement
exclue ici. Elle sera appliquée à l'intérieur de la validation croisée
pour éviter le data leakage.
"""

from nilearn.maskers import NiftiLabelsMasker #mise à jour de l'appel pour NiftiLabelsMaskers
from nilearn import datasets
from nilearn.connectome import ConnectivityMeasure
from argparse import ArgumentParser
import numpy as np
import os
import pandas as pd

def prepare_data(data_dir, output_dir, pipeline="cpac", quality_checked=True, n_subjects=None):
    # Chargement du dataset ABIDE (téléchargement si nécessaire)
    print("Chargement du dataset...")
    abide = datasets.fetch_abide_pcp(data_dir=data_dir,
                                     pipeline=pipeline,
                                     quality_checked=quality_checked,
                                     n_subjects=n_subjects)

    # Liste des fichiers fMRI preprocessés
    fmri_filenames = abide.func_preproc

    # Chargement de l'atlas BASC multiscale (64 régions, symétrique)
    multiscale = datasets.fetch_atlas_basc_multiscale_2015(version="sym", resolution=64)
    atlas_filename = multiscale.maps

    # Initialisation du masker (extraction des séries temporelles par région)
    masker = NiftiLabelsMasker(labels_img=atlas_filename,
                               standardize=True,
                               memory='nilearn_cache',
                               verbose=0)

    # Mesure de connectivité : corrélation vectorisée (diagonale exclue)
    correlation_measure = ConnectivityMeasure(kind='correlation', vectorize=True,
                                             discard_diagonal=True)

    try:
        # Chargement des features depuis le fichier cache si disponible
        feat_file = os.path.join(output_dir, 'ABIDE_BASC064_features.npz')
        X_features = np.load(feat_file)['a']
        print("Fichier de features trouvé.")

    except:
        # Extraction des features depuis les données fMRI brutes (temps d'exraction estimé : 8h)
        X_features = []
        print("Aucun fichier de features trouvé. Extraction en cours...")

        for i, sub in enumerate(fmri_filenames):
            #extraction de la série temporelle des ROIs de l'atlas
            time_series = masker.fit_transform(sub)
            #creation d'une matrcie région x région
            correlation_matrix = correlation_measure.fit_transform([time_series])[0]
            #ajouter au contenant
            X_features.append(correlation_matrix)
            #garder le fil de l'extraction
            print('Extraction terminée : %s sur %s' % (i + 1, len(fmri_filenames)))

        # Sauvegarde des features pour les exécutions suivantes
        np.savez_compressed(os.path.join(output_dir, 'ABIDE_BASC064_features'),
                            a=X_features)

    # Extraction des données phénotypiques et stockage en dataframe
    abide_pheno = pd.DataFrame(abide.phenotypic)

    # Variable cible : diagnostic 
    y_target = abide_pheno['DX_GROUP']

    # Retourne les features brutes 
    return X_features, y_target


def run():
    description = "Prépare les données ABIDE pour la classification de l'autisme"
    parser = ArgumentParser(__file__, description)
    parser.add_argument("data_dir", action="store",
                        help="""Chemin vers le répertoire de données contenant le dataset ABIDE.
                        Si les données sont déjà présentes, ce doit être le dossier contenant
                        le sous-dossier 'ABIDE_pcp'. Sinon, il sera créé automatiquement.""")
    parser.add_argument("output_dir", action="store",
                        help="""Chemin vers le répertoire où sauvegarder les résultats
                        (features extraites).""")
    parser.add_argument("--n-subjects", type=int, default=None,
                        help="Nombre de sujets à charger (None = tous).")
    args = parser.parse_args()
    X_features, y_target = prepare_data(args.data_dir, args.output_dir,
                                        n_subjects=args.n_subjects)

    return X_features, y_target


if __name__ == "__main__":
    run()
