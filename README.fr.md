# Unique Photo Finder v1.1 🚀

Un outil web puissant pour consolider vos sauvegardes désorganisées. Conçu pour vous aider à trouver les fichiers orphelins (fichiers présents sur un vieux disque mais manquants dans votre sauvegarde principale) et gérer efficacement vos collections multimédias.

## 💡 Cas d'Utilisation - Quand Avez-Vous Besoin de Cet Outil ?

**Problème** : Vous avez plusieurs disques durs de sauvegarde accumulés sur plusieurs années. Certains fichiers sont en double, d'autres ont été renommés sur certains disques mais pas sur d'autres, les sauvegardes ont été faites à différents moments, et vous n'êtes jamais vraiment sûr qu'un disque particulier contient toutes vos photos ou documents d'une époque donnée. Tout est désorganisé, et vous voulez **consolider et nettoyer** sans rien perdre d'important.

**Solution** : Cet outil vous aide à :
1. **Comparer** n'importe quel disque avec votre sauvegarde "principale" pour trouver ce qui **manque**
2. **Consolider** tous les fichiers uniques sur un seul disque sans craindre de perdre des données
3. **Préparer** vos disques pour le formatage et la création de sauvegardes propres et organisées

**Flux de travail** :
- Scannez tous vos disques de sauvegarde désorganisés
- Trouvez les fichiers orphelins (fichiers qui existent sur d'anciennes sauvegardes mais manquent dans votre sauvegarde maître actuelle)
- Copiez ces orphelins vers votre sauvegarde maître
- Une fois tout consolidé, utilisez un autre outil pour organiser vos fichiers proprement
- Reformatez les anciens disques et créez des sauvegardes fraîches et propres

## 🚀 Fonctionnalités

- **Scan Intelligent** : Indexe les fichiers (Photos, Vidéos, Audio, Documents) avec déduplication basée sur le hachage.
- **Mode Mise à jour** : Capacité de "Reprise" pour ne scanner que les nouveaux fichiers ou ceux modifiés, beaucoup plus rapide pour les re-scans.
- **Détection d'Orphelins** : Compare un disque "Source" (à nettoyer) contre un disque "Coffre-fort" (sauvegarde) pour trouver les fichiers uniques.
- **Interface Visuelle** :
    - **Grille Responsive** : Visualisez des milliers de photos dans une grille dense à chargement différé (jusqu'à 10 colonnes).
    - **Recherche Instantanée** : Filtrez les résultats par chemin de dossier ou nom de fichier.
    - **Aperçus** : Aperçus de haute qualité pour les images.
- **Gestion de Fichiers** :
    - **Copier/Déplacer** : Copie ou déplacement par lot vers un dossier de destination.
    - **Supprimer** : Déplacez en toute sécurité les fichiers indésirables vers la **Corbeille** (supporte `gio trash` sur Linux).
    - **Nettoyage Auto** : Supprime automatiquement les fichiers effacés de la base de données pour garder votre index propre.
    - **Ouvrir dans l'Explorateur** : Double-cliquez ou utilisez le bouton [↗️] pour ouvrir les dossiers dans votre gestionnaire de fichiers.
- **Confidentialité** : Fonctionne localement sur votre machine. Aucune donnée ne quitte votre réseau.
- **Multi-langue** : 🇫🇷 Français, 🇬🇧 English, 🇪🇸 Español.

## 🛠️ Installation

### Prérequis
- Python 3.8+
- Linux (Support principal) ou Windows (Expérimental)

### Configuration

1.  **Cloner le dépôt**
    ```bash
    git clone https://github.com/antispamluc/unique-photo-finder.git
    cd unique-photo-finder
    ```

2.  **Installer les dépendances**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Lancer l'application**
    ```bash
    python server.py
    ```
    Ou utilisez le script shell fourni :
    ```bash
    ./Lancer_Tri.sh
    ```

4.  **Ouvrir votre navigateur**
    Allez à `http://localhost:8000`

## 📖 Guide d'Utilisation

1.  **Accueil** :
    - Sélectionnez un disque à scanner dans la section "À Trier / Nettoyer".
    - Sélectionnez votre disque de sauvegarde dans la section "Coffre-fort".
    - Cliquez sur "Scanner" pour indexer les fichiers.

2.  **Résultats** :
    - L'outil compare automatiquement les deux disques.
    - Parcourez la structure des dossiers des fichiers "orphelins" (fichiers sur la Source non trouvés dans le Coffre-fort).
    - Utilisez la barre de recherche pour filtrer par nom (ex: "vacances", "2023").
    - Sélectionnez des fichiers/dossiers et utilisez la barre inférieure pour les Copier, Déplacer ou Supprimer.

## ⚠️ Avertissement

**Ce logiciel modifie et supprime des fichiers.**
Bien que des mesures de sécurité soient en place (dialogues de confirmation, vérification de hachage), assurez-vous toujours d'avoir des sauvegardes avant d'effectuer des opérations de suppression ou de déplacement en masse. Les auteurs ne sont pas responsables de la perte de données.

## 💻 Compatibilité

- **Linux** : Entièrement supporté et testé. Utilise des outils système comme `lsblk` et `xdg-open`.
- **Windows** : Expérimental. Les fonctionnalités de base devraient fonctionner, mais la détection des disques et l'ouverture de fichiers peuvent nécessiter des ajustements.

## 📄 Licence

GNU General Public License v3.0 (GPLv3).
Vous êtes libre d'utiliser, modifier et distribuer ce logiciel selon les termes de la GPLv3.
