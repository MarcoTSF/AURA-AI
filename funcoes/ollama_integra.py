import requests
from .auxiliares import falar

OLAMA_URL = "http://localhost:11434/api/generate"

def verificar_ollama():
    """
    Verifica se o servidor Ollama está ativo.
    Retorna True se estiver rodando, False caso contrário.
    """
    try:
        resposta = requests.get(OLAMA_URL.replace("/generate", "/models"), timeout=2)
        if resposta.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        return False
    return False

def perguntar_ollama(prompt, modelo="llama3"):
    """
    Envia uma pergunta para o modelo Ollama local e retorna a resposta.
    Se o servidor não estiver rodando, avisa o usuário.
    """
    if not verificar_ollama():
        falar("O Ollama não está rodando. Abra o aplicativo do Ollama para que eu possa responder perguntas.")
        return None

    try:
        resposta = requests.post(
            OLAMA_URL,
            json={"model": modelo, "prompt": prompt, "max_tokens": 500}
        )

        if resposta.status_code == 200:
            texto = resposta.json().get("response", "").strip()
            if texto:
                falar(texto)
                return texto
            else:
                falar("Não consegui entender a resposta do modelo.")
        else:
            falar("Erro ao se comunicar com o modelo local.")
            print("Resposta do servidor:", resposta.text)

    except Exception as e:
        falar("Houve um erro ao tentar usar o Ollama.")
        print(f"Erro Ollama: {e}")