# ![AURA Logo](https://img.icons8.com/color/48/000000/virtual-reality.png) AURA - Assistente Virtual Pessoal

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python) 
![MIT License](https://img.shields.io/badge/License-MIT-green) 
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange) 
![Spotify](https://img.shields.io/badge/Spotify-API-green?logo=spotify) 
![YouTube](https://img.shields.io/badge/YouTube-API-red?logo=youtube) 

AURA é uma assistente virtual por voz desenvolvida em Python, projetada para automatizar tarefas do dia a dia, controlar mídias e realizar buscas, tudo através de comandos de voz.



## 🚀 Funcionalidades Principais

- **Spotify:** Controle de reprodução de músicas (tocar, pausar, pular, criar filas de recomendação).  
- **YouTube:** Busca e reprodução de vídeos diretamente no YouTube.  
- **Sistema:** Abertura de aplicativos do sistema operacional.  
- **Web:** Realiza buscas na internet.  
- **Data e Hora:** Consulta de data e hora atual.  
- **Modo de Espera:** Economia de recursos com reativação por palavra-chave.  

---

## 🛠️ Tecnologias e Bibliotecas

| Biblioteca | Função |
|-----------|--------|
| [Python 3.11+](https://www.python.org/) | Linguagem de programação principal |
| [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) | Reconhecimento de fala |
| [pyttsx3](https://pypi.org/project/pyttsx3/) | Síntese de voz |
| [spotipy](https://pypi.org/project/spotipy/) | Integração com API do Spotify |
| [youtube-search-python](https://pypi.org/project/youtube-search-python/) | Busca de vídeos no YouTube |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Gerenciamento de variáveis de ambiente |
| [PyAudio](https://pypi.org/project/PyAudio/) | Acesso ao microfone |

---

## 🧩 Objetivos e Futuras Implementações

A AURA está em constante evolução. Abaixo estão as principais metas e melhorias planejadas para as próximas versões:

| Prioridade | Funcionalidade | Descrição |
|-------------|----------------|------------|
| 🥇 Alta | **Detecção de Hotword (“Aura”)** | Ativar a assistente apenas ao ouvir a palavra-chave, sem escuta contínua. |
| 🥈 Alta | **Integração com Ollama / LLM Local** | Permitir conversas naturais e respostas contextuais com IA (Ollama). |
| 🥉 Média | **Logs Inteligentes (.log)** | Registro automático de comandos, respostas e erros para análise e estatísticas. |
| ⚙️ Média | **Melhorias na Interface de Voz** | Otimização das respostas e timbre da voz sintética. |
| 💡 Baixa | **Módulo de Automação Local** | Controle de dispositivos e execução de tarefas no sistema via comandos personalizados. |
| 🌐 Baixa | **Tradução Multilíngue** | Suporte a múltiplos idiomas (PT-BR, EN, ES). |

> 🧠 *Essas metas visam tornar a AURA mais inteligente, eficiente e próxima de uma assistente pessoal real.*

---

## ⚙️ Instalação e Configuração

### 1. Clone o Repositório
```bash
git clone https://github.com/MarcoTSF/IoT-e-Machine-Learning
cd IoT-e-Machine-Learning
```

### 2. Crie um Ambiente Virtual
```bash
python -m venv venv
```
- Windows: .\venv\Scripts\activate
- Linux/Mac: source venv/bin/activate

### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as Chaves da API (Spotify)

    1. Crie uma conta de desenvolvedor no [Spotify for Developers](https://developer.spotify.com/)
    
    2. Crie um App e obtenha Client ID e Client Secret.
    
    3. Crie .env na raiz do projeto (deixei um .env.exemple):
        ```
            SPOTIFY_CLIENT_ID="SEU_CLIENT_ID_AQUI"
            SPOTIFY_CLIENT_SECRET="SEU_CLIENT_SECRET_AQUI"
            SPOTIFY_REDIRECT_URI="http://localhost:8888/callback"
        ```

### ▶️ Como Usar

Com o ambiente virtual ativado, execute:
```bash
python AURA-AI.py
```
A assistente estará pronta para receber comandos.

### 🗣️ Comandos Disponíveis

O nome de ativação é "Aura".

| Categoria    | Comando                                | Ação                                     |
| ------------ | -------------------------------------- | ---------------------------------------- |
| **Spotify**  | Aura, toque [nome da música]           | Toca música e cria fila de recomendações |
|              | Aura, próxima / pula música            | Pula para próxima música                 |
|              | Aura, pausa / parar                    | Pausa música atual                       |
|              | Aura, continuar / play                 | Continua música pausada                  |
| **YouTube**  | Aura, toque no youtube [nome do vídeo] | Busca e reproduz primeiro resultado      |
| **Sistema**  | Aura, abrir [aplicativo]               | Abre aplicativo do sistema               |
| **Geral**    | Aura, pesquise por [termo]             | Realiza busca no Google                  |
|              | Aura, que horas são? / que dia é hoje? | Informa data e hora                      |
| **Controle** | Aura, modo de espera                   | Ativa modo de baixo consumo              |
|              | ativar / aura                          | Reativa assistente do modo de espera     |
|              | Aura, encerrar assistente              | Encerra o programa                       |

### 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.