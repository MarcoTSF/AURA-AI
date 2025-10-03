import speech_recognition as sr
import subprocess
import pyttsx3
import webbrowser
import datetime
import locale

# --- Configurações Iniciais ---
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    print("Locale pt_BR.UTF-8 não encontrado. A data pode aparecer em inglês.")
    # Tenta um fallback para o padrão do sistema
    locale.setlocale(locale.LC_TIME, '')

# Inicializa o motor de Text-to-Speech (TTS)
engine = pyttsx3.init()

# Mapeamento de palavras-chave para caminhos de executáveis
COMANDOS_APP = {
    "navegador": "brave.exe",           # seu navegador padrão (Edge, Chrome, Brave, etc...)
    "calculadora": "calc.exe",           # calculadora
    "captura": "SnippingTool.exe",       # ferramenta de captura
    "configurações": "ms-settings:",     # configurações do Windows
    "bloco de notas": "notepad.exe"      # bloco de notas
}

PALAVRA_ATIVACAO = "aura"

# --- Funções do Assistente ---
def falar(texto):
    """Função para o assistente falar."""
    print(f"Assistente: {texto}")
    engine.say(texto)
    engine.runAndWait()

def ouvir_microfone():
    """Habilita o microfone, ouve o usuário e retorna a frase."""
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        print("Aguardando comando...")
        microfone.adjust_for_ambient_noise(source)
        audio = microfone.listen(source)

    try:
        frase = microfone.recognize_google(audio, language='pt-BR')
        print(f"Você disse: {frase}")
        return frase.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        falar("Desculpe, estou com problemas de conexão para reconhecer a fala.")
        return ""

# --- Funções de Ações ---
def responder_horas():
    """Informa a hora atual."""
    agora = datetime.datetime.now()
    resposta = f"Agora são {agora.hour} horas e {agora.minute} minutos."
    falar(resposta)

def responder_data():
    """Informa a data atual por extenso."""
    agora = datetime.datetime.now()
    # Formatação: "sexta-feira, 3 de outubro de 2025"
    resposta = agora.strftime("Hoje é %A, %d de %B de %Y.")
    falar(resposta)

def pesquisar_web(frase):
    """Realiza uma pesquisa no Google."""
    # Encontra o termo a ser pesquisado (o que vem depois de "pesquisar por")
    termo_pesquisa = frase.split("pesquisar por")[-1].strip()
    
    if not termo_pesquisa:
        falar("Não entendi o que você quer pesquisar.")
        return

    url_pesquisa = f"https://www.google.com/search?q={termo_pesquisa}"
    falar(f"Pesquisando por '{termo_pesquisa}' no navegador.")
    webbrowser.open(url_pesquisa)

# --- Função Principal de Processamento ---
def processar_comandos(frase):
    """Processa a frase para encontrar e executar um comando."""
    # Primeiro, verifica se a palavra de ativação foi dita
    if PALAVRA_ATIVACAO not in frase:
        return # Se a palavra de ativação não estiver na frase, ignora

    falar("Sim?")
    frase = frase.replace(PALAVRA_ATIVACAO, '', 1).strip()

    # --- Verificação de Comandos Específicos ---
    if "que horas são" in frase or "me diga as horas" in frase:
        responder_horas()
        return

    elif "que dia é hoje" in frase or "qual a data de hoje" in frase:
        responder_data()
        return

    elif "pesquisar por" in frase or "pesquise por" in frase:
        pesquisar_web(frase)
        return
        
    # --- Verificação de Comandos para Abrir Aplicativos ---
    for palavra_chave, executavel in COMANDOS_APP.items():
        if palavra_chave in frase:
            falar(f"Abrindo o {palavra_chave}.")
            try:
                subprocess.Popen(executavel)
                return
            except FileNotFoundError:
                falar(f"Desculpe, não consegui encontrar o programa {palavra_chave}.")
            except Exception as e:
                falar(f"Ocorreu um erro ao tentar abrir o {palavra_chave}.")
                print(e)
            return

    # --- Comando para Desligar ---
    if "desligar" in frase or "parar" in frase:
        falar("Desligando. Até mais!")
        return "desligar"
    
    # --- Se nenhum comando for reconhecido ---
    falar("Não entendi o comando. Pode repetir?")

# --- Loop Principal de Execução ---
if __name__ == "__main__":
    falar("Assistente iniciado. Diga 'aura' seguido de um comando.")
    while True:
        frase_ouvida = ouvir_microfone()
        if frase_ouvida:
            resultado = processar_comandos(frase_ouvida)
            if resultado == "desligar":
                break
