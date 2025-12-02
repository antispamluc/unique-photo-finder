import os
import sqlite3
import hashlib
import argparse
import shutil
import time
from datetime import datetime
from pathlib import Path

# Configuration par défaut
DB_NAME = "media_index.db"
DEFAULT_MIN_SIZE = 10 * 1024  # 10 KB (pour ignorer les très petits fichiers/miniatures)
DEFAULT_EXCLUDE_EXT = {'.xmp', '.lrcat', '.lrdata', '.db', '.tmp', '.ini', '.thm', '.ctg'}
CHUNK_SIZE = 8192

# Catégories de fichiers
FILE_CATEGORIES = {
    'photo': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.raw', '.cr2', '.nef', '.arw', '.dng'},
    'video': {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.mts', '.3gp'},
    'audio': {'.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma'},
    'document': {'.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.ods', '.odp', '.rtf', '.csv'}
}

def get_file_hash(filepath, abort_callback=None):
    """Calcule le hash SHA-256 d'un fichier."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(CHUNK_SIZE):
                if abort_callback and abort_callback():
                    return None
                hasher.update(chunk)
        return hasher.hexdigest()
    except (PermissionError, OSError) as e:
        print(f"Erreur de lecture {filepath}: {e}")
        return None

def init_db():
    """Initialise la base de données."""
    conn = sqlite3.connect(DB_NAME, timeout=60.0)  # Timeout augmenté à 60s
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            filename TEXT NOT NULL,
            extension TEXT,
            size_bytes INTEGER,
            mtime REAL,
            hash TEXT,
            source_label TEXT NOT NULL,
            scan_date TEXT,
            UNIQUE(path, source_label)
        )
    ''')
    
    # Table Historique
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_label TEXT NOT NULL,
            category TEXT NOT NULL,
            action TEXT NOT NULL, -- 'scan', 'copy', 'move'
            file_count INTEGER,
            timestamp TEXT
        )
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_hash ON files(hash)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_source ON files(source_label)')
    conn.commit()
    return conn

def scan_directory(conn, path, label, min_size, exclude_ext, update_mode, progress_callback=None, abort_callback=None, include_ext=None):
    """Scanne un répertoire et indexe les fichiers."""
    cursor = conn.cursor()
    root_path = Path(path).resolve()
    
    if not root_path.exists():
        print(f"Erreur: Le chemin {root_path} n'existe pas.")
        return

    print(f"Début du scan de : {root_path} (Label: {label})")
    count = 0
    added = 0
    skipped = 0
    errors = 0
    
    start_time = time.time()

    for root, dirs, files in os.walk(root_path):
        # Vérification d'arrêt demandé
        if abort_callback and abort_callback():
            print("\n[STOP] Scan interrompu par l'utilisateur.")
            break

        for file in files:
            if abort_callback and abort_callback():
                break

            filepath = Path(root) / file
            
            # Filtres rapides (nom/extension)
            ext = filepath.suffix.lower()
            
            # 1. Exclusion explicite
            if ext in exclude_ext:
                continue
                
            # 2. Inclusion explicite (si définie)
            if include_ext is not None and ext not in include_ext:
                continue
            
            try:
                stat = filepath.stat()
                size = stat.st_size
                
                if size < min_size:
                    continue

                # Vérifier si déjà scanné (mode update)
                if update_mode:
                    cursor.execute('SELECT hash FROM files WHERE path = ? AND source_label = ? AND size_bytes = ? AND mtime = ?', 
                                   (str(filepath), label, size, stat.st_mtime))
                    if cursor.fetchone():
                        skipped += 1
                        # Update progress for skipped files too (every 50 files)
                        if skipped % 50 == 0:
                            print(f"Skipped {skipped} files (already indexed)...", end='\r')
                            if progress_callback:
                                progress_callback({
                                    "status": "scanning",
                                    "added": added,
                                    "skipped": skipped,
                                    "current_file": file,
                                    "label": label
                                })
                        continue

                # Calcul du hash (opération lourde)
                file_hash = get_file_hash(filepath, abort_callback)
                if not file_hash:
                    # Si None retourné, soit erreur soit abort
                    if abort_callback and abort_callback():
                        break
                    errors += 1
                    continue

                # Insertion / Mise à jour
                cursor.execute('''
                    INSERT INTO files (path, filename, extension, size_bytes, mtime, hash, source_label, scan_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(path, source_label) DO UPDATE SET
                        size_bytes=excluded.size_bytes,
                        mtime=excluded.mtime,
                        hash=excluded.hash,
                        scan_date=excluded.scan_date
                ''', (
                    str(filepath), 
                    file, 
                    ext, 
                    size, 
                    stat.st_mtime, 
                    file_hash, 
                    label, 
                    datetime.now().isoformat()
                ))
                
                added += 1
                
                # Update progress frequently (every 5 files or if it's the first few)
                if added % 5 == 0 or added < 10:
                    msg = f"Indexés: {added} | Skippés: {skipped} | En cours: {file[:30]}..."
                    print(msg, end='\r')
                    # Commit less frequently to save speed
                    if added % 50 == 0:
                        conn.commit()
                        
                    if progress_callback:
                        progress_callback({
                            "status": "scanning",
                            "added": added,
                            "skipped": skipped,
                            "current_file": file,
                            "label": label
                        })

            except (PermissionError, OSError) as e:
                print(f"\nErreur accès {filepath}: {e}")
                errors += 1
        
        if abort_callback and abort_callback():
            break

    conn.commit()
    duration = time.time() - start_time
    print(f"\nScan terminé en {duration:.1f}s.")
    print(f"Total ajoutés/mis à jour: {added}")
    print(f"Total ignorés (update): {skipped}")
    print(f"Erreurs: {errors}")

def find_orphans(conn, master_label, target_label, list_files=False, export_file=None, include_ext=None, exclude_ext=None):
    """Trouve les fichiers dans target_label qui ne sont PAS dans master_label (basé sur le hash)."""
    cursor = conn.cursor()
    
    print(f"Recherche d'orphelins : {target_label} vs MASTER ({master_label})...")
    
    # On cherche les fichiers de la cible dont le hash n'existe pas dans le maître
    query = '''
        SELECT t.path, t.filename, t.size_bytes, t.hash, t.extension
        FROM files t
        WHERE t.source_label = ?
        AND t.hash NOT IN (
            SELECT m.hash FROM files m WHERE m.source_label = ?
        )
    '''
    
    cursor.execute(query, (target_label, master_label))
    raw_orphans = cursor.fetchall()
    
    # Filtrage post-requête
    orphans = []
    # Extensions système/bruit toujours ignorées par défaut (sauf si explicitement demandées ?)
    # On garde une liste minimale de "bruit" technique pur.
    ignored_patterns = ['.lrdata', '.lrprev', '.thumb', 'Thumbs.db', '.DS_Store', '_data', '.au']
    
    # Normalisation des sets d'extensions (tout en minuscule, avec point)
    allowed_exts = set()
    if include_ext:
        for ext in include_ext:
            if not ext.startswith('.'): ext = '.' + ext
            allowed_exts.add(ext.lower())
            
    blocked_exts = set()
    if exclude_ext:
        for ext in exclude_ext:
            if not ext.startswith('.'): ext = '.' + ext
            blocked_exts.add(ext.lower())

    for o in raw_orphans:
        path_str = o[0]
        filename = o[1]
        size = o[2]
        fhash = o[3]
        ext = o[4].lower() if o[4] else ""
        
        # 1. Filtre patterns ignorés (système)
        if any(pat in path_str for pat in ignored_patterns):
            continue
            
        # 2. Filtre EXCLUDE (prioritaire)
        if ext in blocked_exts:
            continue
            
        # 3. Filtre INCLUDE (si défini, on ne garde QUE ce qui est dedans)
        if allowed_exts and ext not in allowed_exts:
            continue
            
        # Si on arrive ici, c'est bon
        orphans.append((path_str, filename, size, fhash))
    
    total_size = sum(o[2] for o in orphans)
    print(f"\nRésultats pour {target_label}:")
    print(f"Fichiers orphelins trouvés (uniques): {len(orphans)}")
    print(f"Volume total à récupérer: {total_size / (1024*1024):.2f} MB")

    if export_file and orphans:
        try:
            with open(export_file, 'w', encoding='utf-8') as f:
                for o in orphans:
                    f.write(f"{o[0]}\n")
            print(f"\n[OK] Liste complète des {len(orphans)} orphelins exportée dans : {export_file}")
        except Exception as e:
            print(f"\n[Erreur] Impossible d'écrire le fichier d'export : {e}")

    if list_files and orphans:
        print("\n--- Analyse des dossiers manquants ---")
        from collections import Counter
        parent_dirs = []
        for o in orphans:
            path = Path(o[0])
            parent_dirs.append(str(path.parent))
        
        # Compter les occurrences de chaque dossier
        counts = Counter(parent_dirs).most_common(20) # Top 20
        
        print(f"Les orphelins se trouvent principalement dans ces {len(counts)} dossiers :")
        for folder, count in counts:
            print(f"[{count} fichiers] {folder}")
            
        print("\n--- Liste détaillée (premiers 50) ---")
        for o in orphans[:50]:
            print(f"{o[0]}")
        if len(orphans) > 50:
            print(f"... et {len(orphans)-50} autres.")
        print("------------------------------------")
    
    return orphans

def copy_orphans(orphans, dest_root, dry_run=False):
    """Copie les fichiers orphelins vers la destination."""
    dest_path = Path(dest_root)
    if not dest_path.exists():
        if not dry_run:
            dest_path.mkdir(parents=True)
    
    print(f"\nDébut de la copie vers {dest_path}...")
    copied = 0
    errors = 0
    
    for path_str, filename, size, fhash in orphans:
        src = Path(path_str)
        # On peut organiser par extension ou garder à plat. 
        # Ici on va faire simple : Destination/Extension/Fichier
        # Pour éviter les collisions de noms, on peut ajouter le hash ou un suffixe si besoin.
        
        # Structure : Dest/jpg/photo.jpg
        ext = src.suffix.lstrip('.').lower() or "no_ext"
        target_dir = dest_path / ext
        target_file = target_dir / filename
        
        # Gestion collision nom de fichier
        if target_file.exists():
            # Si le fichier existe déjà (même nom), on vérifie si c'est le même contenu (hash déjà fait par le scan, mais ici on parle du fichier physique destination)
            # Mais ici on copie des orphelins, donc par définition ils ne sont pas dans le set "Maître".
            # Si on copie plusieurs orphelins qui ont le même nom mais hash différent (ex: DSC001.jpg de voyage A et DSC001.jpg de voyage B), il faut renommer.
            stem = target_file.stem
            suffix = target_file.suffix
            counter = 1
            while target_file.exists():
                target_file = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1
        
        if dry_run:
            print(f"[DRY RUN] Copie {src} -> {target_file}")
        else:
            try:
                target_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, target_file)
                copied += 1
                print(f"Copié: {filename}", end='\r')
            except Exception as e:
                print(f"\nErreur copie {src}: {e}")
                errors += 1
                
    print(f"\nCopie terminée. Succès: {copied}, Erreurs: {errors}")

def get_orphans_from_list(conn, list_file):
    """Récupère les infos des fichiers depuis une liste texte."""
    orphans = []
    cursor = conn.cursor()
    
    try:
        with open(list_file, 'r', encoding='utf-8') as f:
            paths = [line.strip() for line in f if line.strip()]
            
        print(f"Lecture de {len(paths)} fichiers depuis la liste...")
        
        for path in paths:
            # On récupère les infos dans la DB pour avoir le hash et la taille
            cursor.execute('SELECT path, filename, size_bytes, hash FROM files WHERE path = ?', (path,))
            row = cursor.fetchone()
            if row:
                orphans.append(row)
            else:
                print(f"[Attention] Fichier non trouvé dans l'index (ignoré): {path}")
                
    except Exception as e:
        print(f"Erreur lecture liste: {e}")
        return []
        
    return orphans

def delete_source(conn, label):
    """Supprime toutes les entrées associées à un label source."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM files WHERE source_label = ?", (label,))
    deleted = cursor.rowcount
    
    # Nettoyer aussi l'historique si on veut, mais on peut le garder pour trace.
    # Pour l'instant on garde l'historique.
    
    conn.commit()
    print(f"Source '{label}' supprimée : {deleted} fichiers oubliés.")
    return deleted

def rename_source(conn, old_label, new_label):
    """Renomme un label source dans la base de données."""
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE files SET source_label = ? WHERE source_label = ?", (new_label, old_label))
        updated = cursor.rowcount
        conn.commit()
        print(f"Source '{old_label}' renommée en '{new_label}' : {updated} fichiers mis à jour.")
        return updated
    except sqlite3.IntegrityError:
        print(f"Erreur: Le label '{new_label}' existe déjà pour certains fichiers.")
        return 0

def main():
    parser = argparse.ArgumentParser(description="Outil de consolidation de photos/vidéos.")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Commande SCAN
    cmd_scan = subparsers.add_parser('scan', help='Scanner un dossier et indexer les fichiers')
    cmd_scan.add_argument('--path', required=True, help='Chemin du dossier à scanner')
    cmd_scan.add_argument('--label', required=True, help='Nom unique pour ce disque/source (ex: MASTER, USB1)')
    cmd_scan.add_argument('--min-size', type=int, default=DEFAULT_MIN_SIZE, help='Taille min en octets (défaut 10KB)')
    cmd_scan.add_argument('--update', action='store_true', help='Ne pas re-hasher les fichiers inchangés (chemin+taille+date identiques)')
    
    # Commande REPORT
    cmd_report = subparsers.add_parser('report', help='Afficher les fichiers orphelins (présents sur Cible mais pas sur Maître)')
    cmd_report.add_argument('--master', required=True, help='Label du disque MAÎTRE')
    cmd_report.add_argument('--target', required=True, help='Label du disque à analyser (CIBLE)')
    cmd_report.add_argument('--list', action='store_true', help='Lister les chemins des fichiers orphelins')
    cmd_report.add_argument('--export', help='Chemin du fichier texte pour exporter la liste complète')
    
    # Commande COPY
    cmd_copy = subparsers.add_parser('copy', help='Copier les orphelins vers un dossier')
    cmd_copy.add_argument('--master', help='Label du disque MAÎTRE')
    cmd_copy.add_argument('--target', help='Label du disque SOURCE (où sont les orphelins)')
    cmd_copy.add_argument('--dest', required=True, help='Dossier de destination pour la copie')
    cmd_copy.add_argument('--dry-run', action='store_true', help='Simuler sans copier')
    cmd_copy.add_argument('--from-list', help='Chemin d\'un fichier texte contenant la liste des fichiers à copier (ignorer master/target)')

    args = parser.parse_args()
    
    conn = init_db()
    
    if args.command == 'scan':
        scan_directory(conn, args.path, args.label, args.min_size, DEFAULT_EXCLUDE_EXT, args.update)
    
    elif args.command == 'report':
        find_orphans(conn, args.master, args.target, args.list, args.export)
        
    elif args.command == 'copy':
        orphans = []
        if args.from_list:
            orphans = get_orphans_from_list(conn, args.from_list)
        elif args.master and args.target:
            orphans = find_orphans(conn, args.master, args.target, list_files=False)
        else:
            print("Erreur: Vous devez spécifier soit --from-list, soit --master ET --target")
            return

        if orphans:
            print(f"Prêt à copier {len(orphans)} fichiers vers {args.dest}")
            confirm = input(f"Confirmer ? (o/n) ")
            if confirm.lower() == 'o':
                copy_orphans(orphans, args.dest, args.dry_run)
            else:
                print("Annulé.")
    
    conn.close()

if __name__ == "__main__":
    main()
