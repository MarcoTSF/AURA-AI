import webbrowser
from youtubesearchpython import VideosSearch
from .auxiliares import falar

def tocar_youtube(termo):
    """Busca e toca o primeiro resultado no YouTube."""
    try:
        videos = VideosSearch(termo, limit=1).result()
        if videos["result"]:
            link = videos["result"][0]["link"]
            webbrowser.open(link)
            falar(f"Tocando {termo} no YouTube.")
        else:
            falar("Não encontrei resultados no YouTube.")
    except Exception as e:
        falar("Houve um erro ao buscar no YouTube.")
        print(f"Erro: {e}")