# Unique Photo Finder v1.1 🚀

[![Français](https://img.shields.io/badge/Langue-Français-blue)](README.fr.md) [![Español](https://img.shields.io/badge/Idioma-Español-yellow)](README.es.md)

[📘 User Manual](USER_MANUAL.md) | [📘 Manuel Utilisateur](MANUEL_UTILISATEUR.md) | [📘 Manual de Usuario](MANUAL_USUARIO.md)

A powerful, self-hosted web tool to consolidate messy backups. Designed to help you find orphan files (files present on old drives but missing from your main backup) and manage your media collections efficiently.

## 💡 Use Case - When Do You Need This?

**Problem**: You have multiple backup hard drives accumulated over several years. Some files are duplicated, some have been renamed on certain drives but not others, backups were made at different times, and you're never quite sure if a particular drive has all your photos or documents from a specific period. Everything is disorganized, and you want to **consolidate and clean up** without losing anything important.

**Solution**: This tool helps you:
1. **Compare** any drive against your "main" backup to find what's **missing**
2. **Consolidate** all unique files onto a single drive without worrying about losing data
3. **Prepare** your drives for reformatting and creating clean, organized backups

**Workflow**:
- Scan all your messy backup drives
- Find orphan files (files that exist on old backups but are missing from your current master backup)
- Copy those orphans to your master backup
- Once everything is consolidated, use another tool to organize your files properly
- Reformat the old drives and create fresh, clean backups

## 🚀 Features

- **Smart Scanning**: Indexes files (Photos, Videos, Audio, Documents) with hash-based deduplication.
- **Update Mode**: "Resume" capability to scan only new/changed files, significantly faster for re-scans.
- **Orphan Detection**: Compare a "Source" drive (to clean) against a "Vault" drive (backup) to find unique files.
- **Visual Interface**:
    - **Responsive Grid**: View thousands of photos in a dense, lazy-loaded grid (up to 10 columns).
    - **Instant Search**: Filter results by folder path or file name.
    - **Previews**: High-quality previews for images.
- **File Management**:
    - **Copy/Move**: Batch copy or move files to a destination folder.
    - **Delete**: Securely move unwanted files to the **Trash/Recycle Bin** (supports `gio trash` on Linux).
    - **Auto-Cleanup**: Automatically removes deleted files from the database to keep your index clean.
    - **Open in Explorer**: Double-click or use the [↗️] button to open folders in your OS file manager.
- **Privacy First**: Runs locally on your machine. No data leaves your network.
- **Multi-language**: 🇫🇷 Français, 🇬🇧 English, 🇪🇸 Español.

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Linux (Primary support) or Windows (Experimental)

### Setup

1.  **Clone the repository**
    ```bash
    git clone https://github.com/antispamluc/unique-photo-finder.git
    cd unique-photo-finder
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**
    ```bash
    python server.py
    ```
    Or use the provided shell script:
    ```bash
    ./Lancer_Tri.sh
    ```

4.  **Open your browser**
    Go to `http://localhost:8000`

## 📖 Usage Guide

1.  **Accueil (Home)**:
    - Select a drive to scan in the "À Trier / Nettoyer" section.
    - Select your backup drive in the "Coffre-fort" section.
    - Click "Scanner" to index the files.

2.  **Résultats (Results)**:
    - The tool automatically compares the two drives.
    - Browse the folder structure of "orphan" files (files on Source not found in Vault).
    - Use the search bar to filter by name (e.g., "vacation", "2023").
    - Select files/folders and use the bottom bar to Copy, Move, or Delete them.

## ⚠️ Disclaimer

**This software modifies and deletes files.**
While safety checks are in place (confirmation dialogs, hash verification), always ensure you have backups before performing bulk delete or move operations. The authors are not responsible for data loss.

## 💻 Compatibility

- **Linux**: Fully supported and tested. Uses system tools like `lsblk` and `xdg-open`.
- **Windows**: Experimental. Basic functionality should work, but drive detection and file opening might require adjustments.

## 📄 License

GNU General Public License v3.0 (GPLv3).
You are free to use, modify, and distribute this software under the terms of the GPLv3.

