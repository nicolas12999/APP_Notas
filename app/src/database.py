"""
Módulo de base de datos.
Conexión segura a MySQL con queries parametrizadas
para prevenir SQL injection.
"""
import pymysql
import time
from config import Config


class Database:
    """Gestión segura de conexión y operaciones CRUD contra MySQL."""

    def __init__(self):
        self.connection = None

    def connect(self, retries: int = 10, delay: int = 3) -> bool:
        """Conectar a MySQL con reintentos automáticos."""
        for attempt in range(1, retries + 1):
            try:
                self.connection = pymysql.connect(
                    host=Config.MYSQL_HOST,
                    port=Config.MYSQL_PORT,
                    user=Config.MYSQL_USER,
                    password=Config.MYSQL_PASSWORD,
                    database=Config.MYSQL_DATABASE,
                    charset="utf8mb4",
                    cursorclass=pymysql.cursors.DictCursor,
                    connect_timeout=10,
                )
                print(f"[OK] Conectado a MySQL (intento {attempt})")
                return True
            except pymysql.MySQLError as e:
                print(f"[WARN] Intento {attempt}/{retries} fallido: {e}")
                if attempt < retries:
                    time.sleep(delay)
        print("[ERROR] No se pudo conectar a MySQL")
        return False

    def _ensure_connection(self):
        """Reconectar si la conexión se perdió."""
        if self.connection is None or not self.connection.open:
            self.connect(retries=3, delay=2)

    def get_items(self) -> list:
        """Obtener todos los items (lectura segura)."""
        self._ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT id, nombre, descripcion, created_at FROM items ORDER BY id DESC")
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"[ERROR] get_items: {e}")
            return []

    def add_item(self, nombre: str, descripcion: str) -> bool:
        """Insertar item con query parametrizada (anti SQL injection)."""
        self._ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                # Query parametrizada — NUNCA concatenar strings
                cursor.execute(
                    "INSERT INTO items (nombre, descripcion) VALUES (%s, %s)",
                    (nombre, descripcion),
                )
            self.connection.commit()
            return True
        except pymysql.MySQLError as e:
            print(f"[ERROR] add_item: {e}")
            self.connection.rollback()
            return False

    def delete_item(self, item_id: int) -> bool:
        """Eliminar item por ID con query parametrizada."""
        self._ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
            self.connection.commit()
            return True
        except pymysql.MySQLError as e:
            print(f"[ERROR] delete_item: {e}")
            self.connection.rollback()
            return False

    def close(self):
        """Cerrar conexión limpiamente."""
        if self.connection and self.connection.open:
            self.connection.close()
            print("[OK] Conexión MySQL cerrada")
