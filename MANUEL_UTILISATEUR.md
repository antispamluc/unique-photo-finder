# Guide d'Utilisation - Chercheur de Photos Uniques

Bienvenue dans le guide d'utilisation du **Chercheur de Photos Uniques** (Unique Photo Finder). Ce logiciel vous aide à identifier les fichiers **orphelins** - c'est-à-dire les fichiers présents sur un disque source mais **manquants** dans votre disque de sauvegarde. Le but est de vous aider à compléter vos sauvegardes et à organiser vos collections multimédias.

---

## 🏁 Démarrage Rapide

1.  **Lancer l'application** : Double-cliquez sur `Lancer_Tri.sh` ou exécutez `./Lancer_Tri.sh` dans un terminal.
2.  **Ouvrir le navigateur** : L'interface s'ouvre automatiquement à l'adresse `http://localhost:8000`.
3.  **Choisir la langue** : Cliquez sur les drapeaux 🇫🇷 / 🇬🇧 / 🇪🇸 en haut à droite.

---

## 🏠 Onglet Accueil (Scanner)

C'est ici que vous indexez le contenu de vos disques durs.

### 1. Sélectionner les Disques
- **Disque à Trier (Source)** : Le disque que vous voulez nettoyer ou organiser.
- **Sauvegarde Principale (Maître)** : Votre disque de sauvegarde principal (celui qui contient "tout").

### 2. Options de Scan
- **Mode "Mise à jour"** (Coché par défaut) : 
  - ✅ Recommandé. Ne scanne que les nouveaux fichiers ou ceux modifiés. Beaucoup plus rapide.
  - Décochez pour forcer un re-scan complet (si vous suspectez des erreurs).
- **Filtres** : Choisissez quels types de fichiers scanner (Photos, Vidéos, Audio, Documents).

### 3. Lancer le Scan
Cliquez sur le bouton **"SCANNER"**. Une barre de progression s'affiche. Vous pouvez mettre en pause ou arrêter le scan à tout moment.

---

## 📊 Onglet Résultats (Comparer)

Une fois les scans terminés, allez dans cet onglet pour trouver les "orphelins" (fichiers présents sur la Source mais PAS dans le Coffre-fort).

### 1. Configuration
- **Disque Source** : Sélectionnez le disque à nettoyer.
- **Disque Coffre-fort** : Sélectionnez le disque de référence.
- **Filtres** : Cochez les types de fichiers à afficher.
- **Tout Comparer** : Cochez cette case pour tout sélectionner d'un coup.

### 2. Lancer la Recherche
Cliquez sur **"🔍 Chercher les orphelins"**.

### 3. Gérer les Résultats
- **Liste des dossiers** (à gauche) : Cliquez sur un dossier pour voir son contenu.
- **Grille de fichiers** (au centre) :
  - Visualisez vos photos et vidéos.
  - Cochez les fichiers à traiter (ou utilisez "Tout cocher").
  - Double-cliquez sur une image pour l'ouvrir en grand (si supporté).
  - Clic-droit pour ouvrir le fichier dans votre explorateur de fichiers.

### 4. Actions (en bas)
- **🗑️ SUPPRIMER** : Envoie les fichiers sélectionnés à la corbeille.
  - *Note : La base de données est automatiquement mise à jour.*
- **COPIER / DÉPLACER** :
  - Choisissez un dossier de destination.
  - Cliquez sur "COPIER" (duplique) ou activez "Mode DÉPLACEMENT" puis cliquez sur "DÉPLACER" (déplace et supprime l'original).

---

## ❓ FAQ

**Q: J'ai supprimé des fichiers manuellement, mais ils apparaissent encore ?**
R: Le logiciel met à jour sa base de données quand vous supprimez via l'interface. Si vous supprimez manuellement via l'explorateur Windows/Linux, relancez un scan en mode "Mise à jour" pour rafraîchir la liste.

**Q: Le scan est bloqué ?**
R: Vérifiez la console (F12 dans le navigateur) ou le terminal pour voir s'il y a des erreurs. Vous pouvez arrêter et relancer le serveur sans risque.

**Q: Où sont mes fichiers supprimés ?**
R: Ils sont dans la corbeille de votre système (Trash), sauf si la corbeille n'est pas disponible (disques réseau, etc.), auquel cas ils peuvent être supprimés définitivement (le logiciel vous avertira).
