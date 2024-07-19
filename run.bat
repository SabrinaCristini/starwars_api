@echo off

REM Verificar e instalar o pip
echo Verificando e instalando o pip...
where pip >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo pip não encontrado, instalando pip...
    python -m ensurepip
) ELSE (
    echo pip já está instalado.
)

REM Instalar os pacotes requests e flask
pip install requests flask

REM Executar o script Python
start /B python swapi.py
timeout /t 5 /nobreak >nul

echo Conectando URLs...
SET urls=("http://127.0.0.1:5000/powerful_weapon" "http://127.0.0.1:5000/hottest_planets" "http://127.0.0.1:5000/appears_most" "http://127.0.0.1:5000/fastest_ships")

FOR %%url IN %urls% DO (
    echo Acessar: %%url
    curl -s %%url
    echo.
)

echo O servidor está em execução.
pause