# ==========================================
# 🤖 AURA - ASSISTENTE VIRTUAL COM OLLAMA
# ==========================================
# Desenvolvido por: Marco Túlio Salvador Filho
# Integrações: Spotify API, YouTube Search, Ollama (LLM local)
# ==========================================

import os
import datetime
import logging
from funcoes.auxiliares import falar, ouvir_comando, data_hora, pesquisar_web
from funcoes.apps_basicos import abrir_app
from funcoes.spotify import (
    inicializar_spotify,
    buscar_musica,
    pular_musica,
    pausar,
    play
)
from funcoes.youtube import tocar_youtube
from funcoes.ollama_integration import perguntar_ollama

# --- CONFIGURAÇÕES GERAIS ---
NOME_ASSISTENTE = "aura"
PALAVRA_ATIVACAO = "ativar"

# Inicializa Spotify
sp = inicializar_spotify()

# Cria pasta de logs, se não existir
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/aura.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ===================================
# 💡 FUNÇÃO PRINCIPAL DE EXECUÇÃO
# ===================================
def executar_comando(comando):
    """
    A função principal usa o Ollama como cérebro da Aura.
    Ele interpreta o comando do usuário, gera respostas e,
    quando apropriado, aciona as funções do sistema.
    """
    try:
        logging.info(f"Comando recebido: {comando}")

        # Normaliza texto
        comando = comando.lower().strip()

        # --- ENCERRAR ASSISTENTE ---
        if "encerrar" in comando or "fechar assistente" in comando:
            falar("Encerrando assistente. Até logo!")
            logging.info("Assistente encerrada pelo usuário.")
            exit()

        # --- INTERPRETAÇÃO PRINCIPAL COM OLLAMA ---
        resposta = perguntar_ollama(
            f"Você é a assistente Aura. Analise e entenda este comando do usuário e responda de forma útil. "
            f"Se o comando implicar uma ação (como abrir app, tocar música, pausar, pular, pesquisar, etc.), "
            f"responda naturalmente mencionando a ação, e a execução será feita em seguida. Comando: {comando}"
        )

        if not resposta:
            falar("Desculpe, não consegui entender o comando.")
            return

        resposta_lower = resposta.lower()
        logging.info(f"Ollama respondeu: {resposta}")

        # ==========================================
        # 🔸 AÇÕES DETECTADAS
        # ==========================================
        # Spotify
        if "spotify" in resposta_lower and ("tocar" in resposta_lower or "ouvir" in resposta_lower):
            musica = comando.replace("tocar", "").replace("ouvir", "").replace("no spotify", "").strip()
            buscar_musica(sp, musica)
            return

        elif "pular" in resposta_lower or "próxima" in resposta_lower:
            pular_musica(sp)
            return

        elif "pausar" in resposta_lower or "parar" in resposta_lower:
            pausar(sp)
            return

        elif "continuar" in resposta_lower or "play" in resposta_lower:
            play(sp)
            return

        # YouTube
        elif "youtube" in resposta_lower:
            termo = comando.replace("toque no youtube", "").replace("no youtube", "").strip()
            if termo:
                tocar_youtube(termo)
            else:
                falar("Qual vídeo você quer ver no YouTube?")
            return

        # Abrir aplicativo
        elif "abrir" in resposta_lower:
            app = comando.replace("abrir", "").strip()
            abrir_app(app)
            return

        # Pesquisar na web
        elif "pesquisar" in resposta_lower or "procure" in resposta_lower:
            termo = comando.replace("pesquise por", "").replace("procure por", "").strip()
            if termo:
                pesquisar_web(termo)
            else:
                falar("O que você deseja pesquisar?")
            return

        # Data e hora
        elif "hora" in resposta_lower:
            agora = datetime.datetime.now()
            falar(f"Agora são {agora.strftime('%H:%M')}")
            return

        elif "data" in resposta_lower or "dia" in resposta_lower:
            hoje = datetime.datetime.now()
            falar(f"Hoje é {hoje.strftime('%d/%m/%Y')}")
            return

        # ==========================================
        # 🔹 RESPOSTAS NORMAIS (SEM AÇÃO DETECTADA)
        # ==========================================
        falar(resposta)

    except Exception as e:
        falar("Houve um erro ao processar seu comando.")
        logging.error(f"Erro ao executar comando: {comando} | Erro: {e}")


# ==========================================================
# 🔄 LOOP PRINCIPAL DE ESCUTA
# ==========================================================
if __name__ == "__main__":
    estado_assistente = "ativo"
    falar("Aura iniciada com sucesso. Como posso ajudar?")

    while True:
        comando = ouvir_comando()
        if not comando:
            continue

        comando = comando.lower()

        # --- MODO DE ESPERA ---
        if estado_assistente == "espera":
            if PALAVRA_ATIVACAO in comando or NOME_ASSISTENTE in comando:
                estado_assistente = "ativo"
                comando = comando.replace(PALAVRA_ATIVACAO, "").replace(NOME_ASSISTENTE, "").strip()
                falar("Aura reativada.")
                if comando:
                    executar_comando(comando)
                continue
            else:
                continue

        # --- ENTRAR EM ESPERA ---
        if "modo de espera" in comando or "fique em espera" in comando:
            estado_assistente = "espera"
            falar(f"Entrando em modo de espera. Diga '{PALAVRA_ATIVACAO}' ou '{NOME_ASSISTENTE}' para me reativar.")
            continue

        # --- EXECUTAR COMANDO PRINCIPAL ---
        if NOME_ASSISTENTE in comando:
            comando = comando.replace(NOME_ASSISTENTE, "").strip()
            executar_comando(comando)
