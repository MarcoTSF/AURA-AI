@echo off
title Configuração do Assistente Aura
echo ==========================================
echo      INICIANDO CONFIGURACAO DO AURA
echo ==========================================
echo.

:: Verifica se o Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado. Instale pelo site oficial: https://www.python.org/downloads/
    pause
    exit /b
)

:: Cria ambiente virtual
echo Criando ambiente virtual...
python -m venv venv

:: Ativa o ambiente virtual
call venv\Scripts\activate

:: Atualiza o pip
echo Atualizando o pip...
python -m pip install --upgrade pip

:: Instala dependencias
echo Instalando dependencias do requirements.txt...
pip install -r requirements.txt

:: Teste rapido de inicializacao do motor de voz
echo Testando modulo de voz...
python - <<END
import pyttsx3
engine = pyttsx3.init()
engine.say("Setup concluido com sucesso. Aura pronta para ser iniciada.")
engine.runAndWait()
print("Teste de voz concluido com sucesso.")
END

echo.
echo ==========================================
echo   CONFIGURACAO CONCLUIDA COM SUCESSO ✅
echo   Para iniciar o assistente, use:
echo.
echo   venv\Scripts\activate
echo   python main.py
echo ==========================================
pause