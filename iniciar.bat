@echo off
title NIGHTFALL GAMES
cd /d "%~dp0"

echo ==========================================
echo  INICIANDO O SITE NIGHTFALL GAMES
echo ==========================================
echo.

where py >nul 2>nul
if %errorlevel% neq 0 (
    echo Python nao foi encontrado.
    echo Instale o Python e marque a opcao "Add Python to PATH".
    pause
    exit /b
)

py -m pip show flask >nul 2>nul
if %errorlevel% neq 0 (
    echo Instalando o Flask pela primeira vez...
    py -m pip install flask
)

echo.
echo O site sera aberto automaticamente.
echo Para fechar o site, feche esta janela.
echo.

py app.py
pause
