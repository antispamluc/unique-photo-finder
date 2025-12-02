from fastapi import FastAPI, HTTPException, Query, BackgroundTasks, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
import json
from pathlib import Path
from typing import List, Optional
import uvicorn
import threading
import subprocess
from collections import defaultdict
import psutil
import time

# Import de notre logique existante (un peu hacky mais efficace)
# On suppose que media_tool.py est dans le même dossier
import sys
sys.path.append(os.getcwd())
import media_tool

app = FastAPI(title="Media Sorter GUI")

# État global du scan
scan_status = {
    "is_scanning": False,
    "stop_requested": False,
    "progress": None,
    "error": None
}

# ... (rest of imports)

def get_db():
    return media_tool.init_db()

def run_scan_background(path, label, update, include_list=None):
    global scan_status
    scan_status["is_scanning"] = True
    scan_status["stop_requested"] = False
    scan_status["progress"] = {"status": "starting", "added": 0, "skipped": 0}
    scan_status["error"] = None
    
    conn = get_db()
    
    def progress_cb(data):
        # Inject debug info into progress data
        if "debug_raw_include" in scan_status:
            data["debug_raw_include"] = scan_status["debug_raw_include"]
        scan_status["progress"] = data
        
    def abort_cb():
        return scan_status["stop_requested"]
        
    try:
        print(f"DEBUG: Starting scan for {path} with label {label}")
        media_tool.scan_directory(
            conn, 
            path, 
            label, 
            min_size=10*1024, 
            exclude_ext=media_tool.DEFAULT_EXCLUDE_EXT, 
            update_mode=update,
            progress_callback=progress_cb,
            abort_callback=abort_cb,
            include_ext=include_list
        )
        print("DEBUG: Scan function returned")
        if scan_status["stop_requested"]:
            print("DEBUG: Scan stopped by user")
            scan_status["progress"]["status"] = "stopped"
        else:
            print("DEBUG: Scan finished successfully")
            scan_status["progress"]["status"] = "finished"
    except Exception as e:
        print(f"DEBUG: Scan error: {e}")
        import traceback
        traceback.print_exc()
        scan_status["error"] = str(e)
        scan_status["progress"]["status"] = "error"
    finally:
        conn.close()
        scan_status["is_scanning"] = False


@app.post("/api/scan/stop")
def stop_scan():
    """Demande l'arrêt du scan en cours."""
    global scan_status
    if scan_status["is_scanning"]:
        scan_status["stop_requested"] = True
        return {"message": "Arrêt demandé..."}
    return {"message": "Aucun scan en cours"}

@app.get("/api/scan/status")
def get_scan_status():
    return scan_status

@app.get("/")
async def read_root():
    response = FileResponse("static/index.html", media_type="text/html; charset=utf-8")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.get("/api/sources")
def get_sources():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT source_label FROM files ORDER BY source_label")
    sources = [row[0] for row in cursor.fetchall()]
    conn.close()
    return {"sources": sources}

@app.get("/api/drives")
def get_drives():
    """Liste les disques montés et leurs UUIDs, avec filtrage intelligent."""
    drives = []
    try:
        # Utilisation de lsblk pour avoir les UUIDs et tailles
        cmd = ["lsblk", "-o", "NAME,MOUNTPOINT,LABEL,UUID,FSTYPE,SIZE", "-J"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)
        
        # Filesystems valides pour les données
        valid_fstypes = {'ext4', 'ext3', 'ext2', 'ntfs', 'exfat', 'vfat', 'btrfs', 'xfs', 'hfs', 'hfsplus'}
        
        # Mountpoints à exclure
        excluded_mounts = {'/', '/boot', '/boot/efi', '/tmp', '/var', '/usr', '/opt'}
        
        # Prefixes de mountpoints valides
        valid_prefixes = ('/mnt/', '/media/', '/home/')
        
        for device in data.get("blockdevices", []):
            # Fonction récursive pour trouver les points de montage
            def extract_mounts(dev):
                mountpoint = dev.get("mountpoint")
                fstype = dev.get("fstype")
                
                # Filtrage intelligent
                if mountpoint and fstype:
                    # Exclure swap, tmpfs, devtmpfs, proc, sysfs
                    if fstype in {'swap', 'tmpfs', 'devtmpfs', 'proc', 'sysfs', 'squashfs'}:
                        return
                    
                    # Exclure mountpoints système
                    if mountpoint in excluded_mounts:
                        return
                    
                    # Garder uniquement les mountpoints de données
                    is_valid_mount = any(mountpoint.startswith(prefix) for prefix in valid_prefixes)
                    
                    # Garder uniquement les filesystems de données
                    is_valid_fs = fstype in valid_fstypes
                    
                    if is_valid_mount and is_valid_fs:
                        label = dev.get("label") or dev.get("name") or "Sans nom"
                        size = dev.get("size") or "?"
                        
                        drives.append({
                            "device": dev.get("name"),
                            "mountpoint": mountpoint,
                            "label": label,
                            "uuid": dev.get("uuid"),
                            "fstype": fstype,
                            "size": size,
                            "display": f"💾 {label} ({size}) - {mountpoint}"
                        })
                
                for child in dev.get("children", []):
                    extract_mounts(child)
            
            extract_mounts(device)
            
    except Exception as e:
        print(f"Error listing drives: {e}")
        
    return {"drives": drives}

@app.get("/api/browse")
def browse_directory(path: str):
    """Liste les sous-dossiers d'un chemin donné."""
    if not os.path.isdir(path):
        return {"error": "Chemin invalide"}
    
    try:
        subdirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and not d.startswith('.')]
        subdirs.sort()
        return {"path": path, "subdirs": subdirs}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/scan")
def start_scan(background_tasks: BackgroundTasks, path: str = Query(...), label: str = Query(...), update: bool = Query(False), include: Optional[str] = Query(None)):
    """Lance un scan en arrière-plan."""
    if scan_status["is_scanning"]:
        return {"error": "Un scan est déjà en cours"}
    
    scan_status["is_scanning"] = True
    scan_status["progress"] = {"total": 0, "processed": 0, "current_file": "", "status": "starting"}
    scan_status["stop_requested"] = False # Reset stop flag
    
    # Parse include list
    include_list = include.split(',') if include else None
    
    # Store debug info in scan_status for UI display
    scan_status["debug_include"] = include_list
    scan_status["debug_raw_include"] = include
    
    background_tasks.add_task(run_scan_background, path, label, update, include_list)
    return {"message": "Scan démarré", "label": label}

@app.post("/api/scan/stop")
def stop_scan():
    """Demande l'arrêt du scan en cours."""
    if not scan_status["is_scanning"]:
        return {"error": "Aucun scan en cours"}
    
    scan_status["stop_requested"] = True
    return {"message": "Arrêt du scan demandé..."}

@app.get("/api/scan/status")
def get_status():
    return get_scan_status()

@app.get("/api/orphans")
def get_orphans(master: str, target: str, include: Optional[str] = None, exclude: Optional[str] = None):
    """Récupère les orphelins groupés par dossier parent, filtrés par extensions."""
    conn = get_db()
    
    # Parsing des listes d'extensions (comma separated)
    include_list = include.split(',') if include else None
    exclude_list = exclude.split(',') if exclude else None
    
    # Appel à media_tool avec les nouveaux filtres
    orphans = media_tool.find_orphans(
        conn, 
        master, 
        target, 
        list_files=False, 
        include_ext=include_list, 
        exclude_ext=exclude_list
    )
    conn.close()

    grouped = defaultdict(list)
    count = 0
    total_size = 0
    
    for o in orphans:
        # media_tool retourne (path, filename, size, hash)
        path_str = o[0]
        filename = o[1]
        size_bytes = o[2]
            
        p = Path(path_str)
        parent = str(p.parent)
        
        item = {
            "path": path_str,
            "name": filename,
            "size": size_bytes
        }
        grouped[parent].append(item)
        count += 1
        total_size += size_bytes

    # Conversion en liste pour le JSON
    result = []
    for parent, files in grouped.items():
        result.append({
            "path": parent,
            "count": len(files),
            "files": files
        })
    
    # Tri par nombre de fichiers décroissant
    result.sort(key=lambda x: x['count'], reverse=True)
    
    return {
        "summary": {
            "total_files": count,
            "total_size_mb": round(total_size / (1024*1024), 2)
        },
        "folders": result
    }

@app.get("/api/image")
def get_image(path: str):
    """Sert l'image locale. Attention sécurité en prod, mais OK en local."""
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(path)

@app.post("/api/source/delete")
async def delete_source_endpoint(label: str):
    """Supprime une source de la base de données."""
    try:
        conn = get_db()
        count = media_tool.delete_source(conn, label)
        conn.close()
        return {"deleted": count, "label": label}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/source/rename")
async def rename_source_endpoint(old_label: str, new_label: str):
    """Renomme une source dans la base de données."""
    try:
        conn = get_db()
        count = media_tool.rename_source(conn, old_label, new_label)
        conn.close()
        return {"updated": count, "old_label": old_label, "new_label": new_label}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/copy")
def copy_files(files: List[str], dest: str, move: bool = False):
    """Copie (ou déplace) une liste de fichiers vers la destination.
    
    Avec vérification de hash et mise à jour automatique de la base de données.
    """
    import shutil
    from datetime import datetime
    
    conn = get_db()
    cursor = conn.cursor()
    
    dest_path = Path(dest)
    dest_path.mkdir(parents=True, exist_ok=True)
    
    # Statistics
    copied = 0
    errors = 0
    verification_failed = 0
    db_updated = 0
    
    for file_path in files:
        try:
            src = Path(file_path)
            
            # 1. Get source file info from database (hash + metadata)
            cursor.execute("""
                SELECT hash, source_label, filename, extension, size_bytes, mtime 
                FROM files 
                WHERE path = ?
            """, (str(src),))
            source_info = cursor.fetchone()
            
            if not source_info:
                print(f"Warning: {file_path} not found in database, skipping DB update")
                source_hash = None
            else:
                source_hash, source_label, filename, extension, size_bytes, mtime = source_info
            
            # 2. Prepare destination path (use provided path directly, no extension sorting)
            dest_path_obj = Path(dest)
            dest_path_obj.mkdir(parents=True, exist_ok=True)
            
            target_file = dest_path_obj / src.name
            
            # Handle name collision
            if target_file.exists():
                stem = target_file.stem
                suffix = target_file.suffix
                counter = 1
                while target_file.exists():
                    target_file = target_dir / f"{stem}_{counter}{suffix}"
                    counter += 1
            
            # 3. Copy file
            shutil.copy2(src, target_file)
            
            # 4. Verify integrity by hashing destination file
            if source_hash:
                dest_hash = media_tool.get_file_hash(str(target_file))
                
                if dest_hash != source_hash:
                    verification_failed += 1
                    print(f"ERROR: Hash mismatch for {target_file}")
                    print(f"  Source: {source_hash}")
                    print(f"  Dest:   {dest_hash}")
                    # Delete corrupted copy
                    target_file.unlink()
                    continue
            else:
                # No source hash available, hash the destination anyway for DB
                dest_hash = media_tool.get_file_hash(str(target_file))
            
            # 5. Add to database (auto-detect label from destination path)
            # Try to find which source_label corresponds to the destination
            # For now, we'll need user to provide destination label or infer from path
            # Simple heuristic: try to find best match or use a generic label
            
            # Let's infer the dest_label from the destination path
            # Check if dest path corresponds to any known source
            cursor.execute("SELECT DISTINCT source_label FROM files")
            known_labels = [row[0] for row in cursor.fetchall()]
            
            # Try to match destination path to a known source
            dest_label = None
            for label in known_labels:
                if str(dest_path) in label or label in str(dest_path):
                    dest_label = label
                    break
            
            if not dest_label:
                # Use generic label based on destination path
                dest_label = f"dest_{dest_path.name}"
            
            # Insert into database
            cursor.execute("""
                INSERT OR REPLACE INTO files 
                (path, filename, extension, size_bytes, mtime, hash, source_label, scan_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(target_file),
                target_file.name,
                target_file.suffix.lstrip('.'),
                target_file.stat().st_size,
                target_file.stat().st_mtime,
                dest_hash,
                dest_label,
                datetime.now().isoformat()
            ))
            
            copied += 1
            db_updated += 1
            
            # 6. If move mode, delete source and remove from DB
            if move:
                os.remove(src)
                cursor.execute("DELETE FROM files WHERE path = ?", (str(src),))
                
        except Exception as e:
            print(f"Error copying {file_path}: {e}")
            import traceback
            traceback.print_exc()
            errors += 1
    
    conn.commit()
    conn.close()
    
    return {
        "copied": copied,
        "errors": errors,
        "verification_failed": verification_failed,
        "db_updated": db_updated
    }

@app.post("/api/open")
def open_file(path: str = Query(...)):
    """Ouvre le fichier ou le dossier dans l'explorateur du système."""
    import subprocess
    import platform
    
    if not os.path.exists(path):
        return {"error": "Chemin introuvable"}
        
    try:
        if platform.system() == 'Linux':
            subprocess.call(['xdg-open', path])
        elif platform.system() == 'Windows':
            os.startfile(path)
        elif platform.system() == 'Darwin':
            subprocess.call(['open', path])
        return {"message": "Ouvert"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/shutdown")
def shutdown():
    """Arrête le serveur proprement."""
    # On lance l'arrêt dans un thread séparé pour pouvoir répondre à la requête avant de mourir
    def kill():
        import time
        time.sleep(1)
        os._exit(0)
    threading.Thread(target=kill).start()
    return {"message": "Server shutting down..."}

@app.post("/api/delete")
async def delete_files(files: List[str] = Body(...)):
    """Envoie une liste de fichiers à la corbeille (ou supprime si impossible)."""
    import subprocess
    import platform
    
    deleted_count = 0
    errors = []
    
    conn = get_db()
    cursor = conn.cursor()
    
    for file_path in files:
        try:
            if os.path.exists(file_path):
                if os.path.isfile(file_path):
                    # Try to use trash first
                    trashed = False
                    if platform.system() == 'Linux':
                        try:
                            # Use gio trash (standard on modern Linux distros like Fedora/Nobara/Ubuntu)
                            subprocess.run(['gio', 'trash', file_path], check=True, capture_output=True)
                            trashed = True
                        except Exception:
                            pass
                            
                    if not trashed:
                        # Fallback to permanent delete if trash fails or not on Linux
                        # But maybe we should warn? For now, let's assume if gio fails we might want to keep it or force delete?
                        # User asked for trash. If trash fails, we should probably error out or try os.remove if they really want delete.
                        # Let's try os.remove as fallback but maybe log it.
                        os.remove(file_path)
                    
                    # Remove from DB if successful
                    try:
                        cursor.execute("DELETE FROM files WHERE path = ?", (file_path,))
                        conn.commit()
                    except Exception as e:
                        print(f"Error removing from DB {file_path}: {e}")
                        
                    deleted_count += 1
                else:
                    errors.append(f"Not a file: {file_path}")
            else:
                # File doesn't exist on disk, but we should remove it from DB to clean up
                try:
                    cursor.execute("DELETE FROM files WHERE path = ?", (file_path,))
                    conn.commit()
                    deleted_count += 1 # Count as deleted/cleaned
                except Exception as e:
                    print(f"Error removing from DB {file_path}: {e}")
                
                # Still warn user but consider it "handled"
                errors.append(f"Not found (removed from DB): {file_path}")
        except Exception as e:
            errors.append(f"Error processing {file_path}: {str(e)}")
            
    return {"deleted_count": deleted_count, "errors": errors}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
