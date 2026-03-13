"""
Configuración de la aplicación.
Lee variables de entorno para la conexión a MySQL.
Carga automáticamente el archivo .env del proyecto (compatible con Windows).
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Buscar el .env en la raíz del proyecto (dos niveles arriba de src/)
_BASE_DIR = Path(__file__).resolve().parent.parent.parent
_ENV_FILE = _BASE_DIR / ".env"
if _ENV_FILE.exists():
    load_dotenv(_ENV_FILE)
else:
    # Fallback: buscar en directorio de trabajo actual
    load_dotenv()


class Config:
    """Configuración centralizada desde variables de entorno."""

    MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
    MYSQL_USER = os.environ.get("MYSQL_USER", "app_user")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "app_db")
