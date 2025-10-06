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
        return resposta.status_code == 200
    except requests.exceptions.RequestException:
        return False


def perguntar_ollama(prompt, modelo="llama3"):
    """
    Envia uma pergunta para o modelo Ollama local e retorna a resposta em texto.
    Se o Ollama não estiver rodando, avisa o usuário (por voz).
    """
    if not verificar_ollama():
        falar("O Ollama não está rodando. Abra o aplicativo do Ollama para que eu possa responder perguntas.")
        return None

    try:
        resposta = requests.post(
            OLAMA_URL,
            json={"model": modelo, "prompt": prompt, "stream": False, "max_tokens": 500},
            timeout=60
        )

        if resposta.status_code == 200:
            # Alguns modelos retornam a resposta diretamente, outros dentro de JSON lines
            try:
                data = resposta.json()
                texto = data.get("response", "").strip()
            except Exception:
                texto = resposta.text.strip()

            return texto or "Não consegui entender a resposta do modelo."

        else:
            print("Erro na resposta do Ollama:", resposta.text)
            return "Erro ao se comunicar com o modelo local."

    except Exception as e:
        print(f"Erro Ollama: {e}")
        return "Houve um erro ao tentar usar o Ollama."
