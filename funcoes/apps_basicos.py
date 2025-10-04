import subprocess
from .auxiliares import falar

COMANDOS_APP = {
    "navegador": "msedge.exe",
    "calculadora": "calc.exe",
    "captura": "SnippingTool.exe",
    "configurações": "ms-settings:",
    "bloco de notas": "notepad.exe"
}

def abrir_app(nome):
    """Abre um aplicativo com base no nome fornecido."""
    try:
        subprocess.Popen(COMANDOS_APP[nome])
        falar(f"Abrindo {nome}")
    except KeyError:
        falar(f"Não encontrei o aplicativo {nome} na lista.")
    except Exception as e:
        falar(f"Não consegui abrir {nome}. Erro: {e}")