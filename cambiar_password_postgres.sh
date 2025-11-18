#!/bin/bash
# Script para cambiar la contraseña de PostgreSQL a "123"

echo "Cambiando contraseña de PostgreSQL..."

# Opción 1: Con sudo (requiere tu contraseña de usuario)
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD '123';"

if [ $? -eq 0 ]; then
    echo "✓ Contraseña cambiada exitosamente a '123'"
    echo ""
    echo "Ahora puedes ejecutar:"
    echo "  python3 setup_database.py"
else
    echo "✗ No se pudo cambiar la contraseña"
    echo ""
    echo "Intenta ejecutar manualmente:"
    echo "  sudo -u postgres psql"
    echo "Luego dentro de psql escribe:"
    echo "  ALTER USER postgres WITH PASSWORD '123';"
    echo "  \\q"
fi
