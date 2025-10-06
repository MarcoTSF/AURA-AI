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

:: Verifica se o Ollama está rodando na porta 11434
echo Verificando Ollama...
powershell -Command ^
    "$port=11434; " ^
    "$connection = Test-NetConnection -ComputerName 127.0.0.1 -Port $port; " ^
    "exit ($connection.TcpTestSucceeded -eq $false ? 1 : 0)"

if %ERRORLEVEL% == 1 (
    echo Ollama nao esta rodando. Iniciando Ollama em segundo plano...
    :: start "" /B "C:\Caminho\Para\Ollama.exe" serve

    echo Aguardando Ollama iniciar...
    timeout /t 5 >nul

    :check_port
    powershell -Command ^
        "$port=11434; " ^
        "$connection = Test-NetConnection -ComputerName 127.0.0.1 -Port $port; " ^
        "exit ($connection.TcpTestSucceeded -eq $false ? 1 : 0)"
    if %ERRORLEVEL% == 1 (
        echo Aguardando Ollama iniciar...
        timeout /t 2 >nul
        goto check_port
    )
) else (
    echo Ollama ja esta rodando.
)

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
echo   python AURA-AI.py
echo ==========================================
pause
