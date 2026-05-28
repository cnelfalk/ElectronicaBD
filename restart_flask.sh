#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# restart_flask.sh — Mata los procesos viejos de Flask y reinicia la API
# ═══════════════════════════════════════════════════════════════════════════

PROJECT_DIR="/home/fabrizio/ProyectosWeb/ElectronicaBD"
BACKEND_DIR="$PROJECT_DIR/backend"
PYTHON_BIN="$BACKEND_DIR/venv/bin/python"

echo "Buscando procesos activos de app.py..."
# Listar procesos antes de matar
ps aux | grep "[a]pp.py"

echo "Matando procesos de Flask antiguos..."
pkill -f "python.*app.py"
sleep 1

echo "Iniciando Flask en segundo plano..."
cd "$BACKEND_DIR"
nohup "$PYTHON_BIN" app.py > flask.log 2>&1 &

sleep 2
echo "Procesos de Python actuales:"
ps aux | grep "[a]pp.py"

echo "¡Listo! Flask reiniciado. Logs guardados en $BACKEND_DIR/flask.log"
