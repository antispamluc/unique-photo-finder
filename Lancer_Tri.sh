#!/bin/bash
cd "$(dirname "$0")"
echo "Lancement du Chercheur de Photos Uniques..."
xdg-open http://localhost:8000 &
python3 server.py
