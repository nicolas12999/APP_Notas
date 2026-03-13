@echo off
REM ============================================================
REM  iniciar.bat — Lanzador de la aplicación en Windows
REM  Requisitos: Docker Desktop + Python 3.10+
REM ============================================================
setlocal

echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║       Gestor de Items — Arranque Windows     ║
echo  ╚══════════════════════════════════════════════╝
echo.

REM --- 1. Verificar Docker ---
where docker >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker no encontrado. Instala Docker Desktop y vuelve a intentarlo.
    pause
    exit /b 1
)

REM --- 2. Verificar Python ---
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado. Instala Python 3.10+ y agrega al PATH.
    pause
    exit /b 1
)

REM --- 3. Verificar que existe el .env ---
if not exist "%~dp0.env" (
    echo [ERROR] No se encontro el archivo .env en la raiz del proyecto.
    echo         Copia .env.example a .env y configura tus credenciales.
    pause
    exit /b 1
)

REM --- 4. Levantar la base de datos MySQL con Docker ---
echo [1/3] Levantando MySQL con Docker...
docker compose -f "%~dp0docker-compose.yml" up -d
if errorlevel 1 (
    echo [ERROR] Fallo al levantar Docker. Revisa que Docker Desktop este ejecutandose.
    pause
    exit /b 1
)
echo        MySQL arrancando (espera unos segundos para el healthcheck)...
echo.

REM --- 5. Instalar dependencias Python si falta alguna ---
echo [2/3] Comprobando dependencias Python...
pip show customtkinter >nul 2>&1
if errorlevel 1 (
    echo        Instalando dependencias desde requirements.txt...
    pip install -r "%~dp0app\requirements.txt"
    if errorlevel 1 (
        echo [ERROR] Fallo al instalar dependencias.
        pause
        exit /b 1
    )
) else (
    echo        Dependencias OK.
)
echo.

REM --- 6. Lanzar la aplicacion ---
echo [3/3] Iniciando la aplicacion...
echo.
python "%~dp0app\src\main.py"

REM --- 7. Al cerrar la app, preguntar si detener Docker ---
echo.
set /p STOP="¿Detener MySQL (Docker)? [s/N]: "
if /i "%STOP%"=="s" (
    docker compose -f "%~dp0docker-compose.yml" down
    echo        MySQL detenido.
)

endlocal
pause
