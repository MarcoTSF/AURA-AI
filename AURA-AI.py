from funcoes.ollama_integra import perguntar_ollama
from funcoes.auxiliares import falar, ouvir_comando, data_hora, pesquisar_web
from funcoes.apps_basicos import COMANDOS_APP, abrir_app
from funcoes.spotify import inicializar_spotify, buscar_musica, pular_musica, pausar, play
from funcoes.youtube import tocar_youtube

NOME_ASSISTENTE = "aura"
PALAVRA_ATIVACAO = "ativar"

sp = inicializar_spotify()

def executar_comando(comando):
    if NOME_ASSISTENTE in comando:
        comando = comando.replace(NOME_ASSISTENTE, "").strip()

    # --- Spotify ---
    if comando.startswith("toque") and "youtube" not in comando:
        musica = comando.replace("toque", "").strip()
        buscar_musica(sp, musica)
    elif "pula" in comando or "próxima" in comando:
        pular_musica(sp)
    elif "pausa" in comando or "parar" in comando:
        pausar(sp)
    elif "continuar" in comando or "play" in comando:
        play(sp)

    # --- YouTube ---
    elif "toque no youtube" in comando:
        termo = comando.replace("toque no youtube", "").strip()
        if termo:
            tocar_youtube(termo)
        else:
            falar("O que você quer tocar no YouTube?")

    # --- Apps básicos ---
    elif comando.startswith("abrir"):
        app_nome = comando.replace("abrir", "").strip()
        if app_nome in COMANDOS_APP:
            abrir_app(app_nome)
        else:
            falar("Não reconheci o aplicativo que você pediu.")

    # --- Data e hora ---
    elif "que horas são" in comando or "que dia é hoje" in comando:
        data_hora()

    # --- Pesquisar no navegador ---
    elif comando.startswith("pesquise por") or comando.startswith("procure por"):
        termo = comando.replace("pesquise por", "").replace("procure por", "").strip()
        if termo:
            pesquisar_web(termo)
        else:
            falar("O que você deseja pesquisar?")

    # --- Encerrar assistente ---
    elif "encerrar assistente" in comando:
        falar("Encerrando assistente. Até logo!")
        exit()

    else:
        if comando:
            # Envia para o modelo local (Ollama) tentar responder
            resposta = perguntar_ollama(comando)
            if not resposta:
                falar("Desculpe, não entendi o comando.")

if __name__ == "__main__":
    estado_assistente = "ativo"

    falar("Aura iniciada com sucesso. Como posso ajudar?")
    
    while True:
        comando = ouvir_comando()
        if not comando:
            continue

        comando = comando.lower()

        # --- LÓGICA PARA REATIVAR O ASSISTENTE ---
        if estado_assistente == "espera":
            if PALAVRA_ATIVACAO in comando or NOME_ASSISTENTE in comando:
                estado_assistente = "ativo"
                # Remove apenas a palavra de ativação do comando
                comando = comando.replace(PALAVRA_ATIVACAO, "").replace(NOME_ASSISTENTE, "").strip()
                falar("Aura reativada.")
                # Se sobrou algum comando além do gatilho, execute
                if comando:
                    executar_comando(comando)
                continue
            else:
                # Se estiver em espera e não mencionou a ativação, ignora
                continue

        # --- LÓGICA PARA ENTRAR EM MODO DE ESPERA ---
        if "modo de espera" in comando or "fique em espera" in comando:
            estado_assistente = "espera"
            falar(f"Entrando em modo de espera. Diga '{PALAVRA_ATIVACAO}' ou '{NOME_ASSISTENTE}' para me reativar.")
            continue
            
        # --- EXECUTAR COMANDOS ---
        if NOME_ASSISTENTE in comando:
            comando = comando.replace(NOME_ASSISTENTE, "").strip()
            executar_comando(comando)