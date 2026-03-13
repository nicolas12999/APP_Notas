# Gestor de Items — Guía de uso en Windows

## Requisitos previos

| Herramienta | Versión mínima | Descarga |
|---|---|---|
| **Docker Desktop** | 4.x (WSL2 backend) | https://www.docker.com/products/docker-desktop |
| **Python** | 3.10+ | https://www.python.org/downloads/ |

> [!IMPORTANT]
> Durante la instalación de Python en Windows, marca la opción **"Add Python to PATH"**.

---

## Arranque rápido (recomendado)

```
doble clic en  iniciar.bat
```

El script hace automáticamente:
1. Verifica que Docker y Python estén instalados
2. Levanta MySQL con `docker compose up -d`
3. Instala las dependencias Python si faltan (`pip install -r requirements.txt`)
4. Lanza la aplicación gráfica (`main.py`)
5. Al cerrar la app, te pregunta si quieres detener Docker

---

## Arranque manual paso a paso

### 1. Configurar variables de entorno
```bat
copy .env.example .env
```
Edita `.env` si quieres cambiar las contraseñas.

### 2. Levantar la base de datos
```bat
docker compose up -d
```

### 3. Instalar dependencias Python
```bat
pip install -r app\requirements.txt
```

### 4. Lanzar la aplicación
```bat
python app\src\main.py
```

### 5. Detener la base de datos (cuando termines)
```bat
docker compose down
```

---

## Estructura del proyecto

```
programa/
├── .env                  ← Variables de entorno (NO subir a Git)
├── .env.example          ← Plantilla para crear tu .env
├── docker-compose.yml    ← Configuración de MySQL
├── iniciar.bat           ← Script de arranque para Windows
├── app/
│   ├── requirements.txt  ← Dependencias Python
│   └── src/
│       ├── main.py       ← Interfaz gráfica (CustomTkinter)
│       ├── database.py   ← Lógica CRUD con MySQL
│       └── config.py     ← Configuración (lee el .env automáticamente)
└── db/
    └── init.sql          ← Script de inicialización de la BD
```

---

## Solución de problemas en Windows

| Problema | Causa probable | Solución |
|---|---|---|
| `docker: command not found` | Docker Desktop no instalado o no iniciado | Instala Docker Desktop y ábrelo antes de ejecutar |
| `python: command not found` | Python no está en el PATH | Reinstala Python marcando "Add to PATH" |
| La app no conecta a MySQL | MySQL todavía arrancando | Espera 30 segundos y pulsa **Refrescar** |
| Puerto 3306 ocupado | Otro MySQL local en ejecución | Detén el servicio MySQL local: `net stop MySQL` |
| Error de permisos en PowerShell | Política de ejecución restrictiva | Ejecuta `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
