import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from .auxiliares import falar

def inicializar_spotify():
    """Inicializa e retorna a conexão com o Spotify."""
    try:
        scope = "user-read-playback-state user-modify-playback-state user-top-read"
        return spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
            scope=scope
        ))
    except Exception as e:
        falar("Não consegui conectar ao Spotify. Verifique suas credenciais.")
        print(f"Erro de conexão: {e}")
        return None

def buscar_musica(sp, nome):
    """Busca uma música e a reproduz, com fallback em recomendações."""
    if not sp:
        falar("Spotify não está conectado.")
        return

    dispositivos = sp.devices()
    if not dispositivos or not dispositivos["devices"]:
        falar("Nenhum dispositivo Spotify ativo foi encontrado.")
        return

    device_id = dispositivos["devices"][0]["id"]
    resultados = sp.search(q=nome, limit=1, type="track", market="BR")

    if not resultados["tracks"]["items"]:
        falar("Não encontrei essa música.")
        return

    musica = resultados["tracks"]["items"][0]
    id_musica = musica["id"]
    id_artista = musica["artists"][0]["id"]
    uris_para_tocar = [musica["uri"]]

    try:
        recomendacoes = sp.recommendations(seed_tracks=[id_musica], limit=15, market="BR")
        uris_para_tocar += [faixa["uri"] for faixa in recomendacoes["tracks"]]
        falar(f"Tocando {musica['name']} e criando uma playlist personalizada.")
    except Exception:
        try:
            recomendacoes = sp.recommendations(seed_artists=[id_artista], limit=15, market="BR")
            uris_para_tocar += [faixa["uri"] for faixa in recomendacoes["tracks"]]
            falar(f"Tocando {musica['name']} e criando uma playlist baseada no artista.")
        except Exception:
            falar("Tocando apenas a música solicitada.")

    sp.start_playback(device_id=device_id, uris=uris_para_tocar)

def adicionar_recomendacoes_fila(sp):
    """Adiciona músicas relacionadas à fila."""
    try:
        playback = sp.current_playback()
        if not playback or not playback["item"]:
            return
        id_atual = playback["item"]["id"]
        recomendacoes = sp.recommendations(seed_tracks=[id_atual], limit=5, market="BR")
        for faixa in recomendacoes["tracks"]:
            sp.add_to_queue(faixa["uri"])
        print("INFO: 5 novas recomendações adicionadas à fila.")
    except Exception as e:
        print(f"Erro ao adicionar recomendações: {e}")

def pular_musica(sp):
    try:
        sp.next_track()
        falar("Próxima música.")
        adicionar_recomendacoes_fila(sp)
    except Exception as e:
        falar("Não consegui pular a música.")
        print(f"Erro: {e}")

def pausar(sp):
    try:
        sp.pause_playback()
        falar("Música pausada.")
    except Exception as e:
        falar("Não consegui pausar a música.")
        print(f"Erro: {e}")

def play(sp):
    try:
        sp.start_playback()
        falar("Reproduzindo.")
        adicionar_recomendacoes_fila(sp)
    except Exception as e:
        falar("Não consegui dar play.")
        print(f"Erro: {e}")