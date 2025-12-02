# User Manual - Unique Photo Finder

Welcome to the **Unique Photo Finder** user manual. This software helps you identify **orphan** files - files that are present on a source drive but **missing** from your backup drive. The goal is to help you complete your backups and organize your media collections.

---

## 🏁 Quick Start

1.  **Launch the application**: Double-click on `Lancer_Tri.sh` or run `./Lancer_Tri.sh` in a terminal.
2.  **Open browser**: The interface opens automatically at `http://localhost:8000`.
3.  **Choose language**: Click on the flags 🇫🇷 / 🇬🇧 / 🇪🇸 in the top right corner.

---

## 🏠 Home Tab (Scan)

This is where you index the content of your hard drives.

### 1. Select Drives
- **Drive to Sort (Source)**: The drive you want to clean or organize.
- **Backup Drive (Master)**: Your main backup drive (the one that contains "everything").

### 2. Scan Options
- **"Update" Mode** (Checked by default):
  - ✅ Recommended. Scans only new or modified files. Much faster.
  - Uncheck to force a full re-scan (if you suspect errors).
- **Filters**: Choose which file types to scan (Photos, Videos, Audio, Documents).

### 3. Start Scan
Click the **"SCAN"** button. A progress bar appears. You can pause or stop the scan at any time.

---

## 📊 Results Tab (Compare)

Once scans are complete, go to this tab to find "orphans" (files present on Source but NOT in Vault).

### 1. Configuration
- **Source Drive**: Select the drive to clean.
- **Vault Drive**: Select the reference drive.
- **Filters**: Check the file types to display.
- **Compare Everything**: Check this box to select everything at once.

### 2. Start Search
Click **"🔍 Find orphans"**.

### 3. Manage Results
- **Folder List** (left): Click a folder to see its content.
- **File Grid** (center):
  - View your photos and videos.
  - Check files to process (or use "Select All").
  - Double-click an image to view it full size (if supported).
  - Right-click to open the file in your file explorer.

### 4. Actions (bottom)
- **🗑️ DELETE**: Sends selected files to the trash.
  - *Note: The database is automatically updated.*
- **COPY / MOVE**:
  - Choose a destination folder.
  - Click "COPY" (duplicates) or enable "MOVE Mode" then click "MOVE" (moves and deletes original).

---

## ❓ FAQ

**Q: I deleted files manually, but they still appear?**
A: The software updates its database when you delete via the interface. If you delete manually via Windows/Linux explorer, run a scan in "Update" mode to refresh the list.

**Q: The scan is stuck?**
A: Check the console (F12 in browser) or terminal to see if there are errors. You can stop and restart the server safely.

**Q: Where are my deleted files?**
A: They are in your system's Trash, unless the trash is unavailable (network drives, etc.), in which case they might be permanently deleted (the software will warn you).
