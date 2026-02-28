import json
import os

# Caminho do config.json ao lado do executável (ou do avatar_ia.py)
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")

DEFAULT_SETTINGS = {
    "agent_name": "JARVIS",
    "voice": "pt-BR-AntonioNeural",
    "gemini_api_key": "",
    "claude_api_key": "",
}

def load_settings() -> dict:
    """Carrega configurações do config.json, criando-o se não existir."""
    path = os.path.normpath(CONFIG_PATH)
    if not os.path.exists(path):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Garante que todas as chaves existam
        for k, v in DEFAULT_SETTINGS.items():
            data.setdefault(k, v)
        return data
    except Exception as e:
        print(f"Erro ao carregar config.json: {e}")
        return DEFAULT_SETTINGS.copy()


def save_settings(data: dict):
    """Salva as configurações no config.json."""
    path = os.path.normpath(CONFIG_PATH)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar config.json: {e}")


def get_voice_id(settings: dict) -> str:
    """Retorna o nome da voz exata selecionada para edge-tts."""
    return settings.get("voice", "pt-BR-AntonioNeural")
