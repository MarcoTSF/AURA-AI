import webbrowser
from datetime import datetime
from .configuracoes import engine, recognizer, microfone

def falar(texto):
    """Faz o assistente falar e imprime o texto no console."""
    print(f"Aura: {texto}")
    engine.say(texto)
    engine.runAndWait()

def ouvir_comando():
    """Ouve o microfone e retorna o comando reconhecido."""
    with microfone as source:
        print("🎤 Ouvindo...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        comando = recognizer.recognize_google(audio, language="pt-BR").lower()
        print(f"Você disse: {comando}")
        return comando
    except Exception:
        return ""

def data_hora():
    """Fala a data e hora atuais."""
    agora = datetime.now()
    data = agora.strftime("%d/%m/%Y")
    hora = agora.strftime("%H:%M")
    falar(f"Hoje é {data} e agora são {hora}.")

def pesquisar_web(termo):
    """Abre o navegador e faz uma pesquisa no Google."""
    url = f"https://www.google.com/search?q={termo}"
    webbrowser.open(url)
    falar(f"Pesquisando por {termo} no navegador.")