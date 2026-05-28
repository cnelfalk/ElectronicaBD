#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# setup_cron.sh — Configura la automatización diaria de los bots a las 3 AM
# ═══════════════════════════════════════════════════════════════════════════

PROJECT_DIR="/home/fabrizio/ProyectosWeb/ElectronicaBD"
BACKEND_DIR="$PROJECT_DIR/backend"
PYTHON_BIN="$BACKEND_DIR/venv/bin/python"
LOG_FILE="$BACKEND_DIR/bots.log"

echo "Configurando la automatización de scrapers para TechMatch..."

# Verificar existencia de archivos clave
if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ ERROR: No se encuentra la carpeta backend en $BACKEND_DIR"
    exit 1
fi

if [ ! -f "$PYTHON_BIN" ]; then
    echo "❌ ERROR: No se encuentra el entorno virtual python en $PYTHON_BIN"
    exit 1
fi

# Línea del cron job (Todos los días a las 3:00 AM)
CRON_JOB="0 3 * * * cd $BACKEND_DIR && $PYTHON_BIN run_bots.py >> $LOG_FILE 2>&1"

# Verificar si ya existe en crontab
crontab -l 2>/dev/null | grep -Fq "run_bots.py"
if [ $? -eq 0 ]; then
    echo "ℹ️  La tarea ya se encuentra registrada en el crontab de este usuario."
else
    # Registrar en crontab
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    if [ $? -eq 0 ]; then
        echo "✅ Tarea programada registrada exitosamente en crontab:"
        echo "   $CRON_JOB"
    else
        echo "❌ ERROR al registrar la tarea en crontab."
        exit 1
    fi
fi

echo ""
echo "Instrucciones de verificación manual:"
echo "1. Ejecutar 'crontab -l' para listar todas las tareas programadas."
echo "2. Para ver el archivo de log generado por la ejecución, abrir: $LOG_FILE"
echo ""
