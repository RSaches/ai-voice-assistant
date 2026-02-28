import os
import webbrowser

from google import genai
from config.i18n import t

API_ACTIVATION_URL = (
    "https://console.developers.google.com/apis/api/"
    "generativelanguage.googleapis.com/overview?project=gen-lang-client-0236676834"
)

MODEL = "gemini-2.0-flash"

def get_system_prompt(agent_name):
    return t('system_prompt', name=agent_name)


class GeminiBrain:
    def __init__(self):
        from config.settings_manager import load_settings
        settings = load_settings()
        self.agent_name = settings.get("agent_name", "JARVIS")
        api_key = settings.get("gemini_api_key", "")
        # google-genai falha se a chave for vazia, usar string dummy temporária
        if not api_key:
            api_key = "DUMMY_KEY_WAITING_FOR_SETUP"
            
        self.client = genai.Client(
            api_key=api_key,
            http_options={"api_version": "v1"}
        )
        self.history = [
            {"role": "user", "parts": [{"text": get_system_prompt(self.agent_name)}]},
            {"role": "model", "parts": [{"text": t('gemini_first_msg', name=self.agent_name)}]},
        ]

    def reload(self):
        """Reinicia o cliente com a chave mais recente do config."""
        from config.settings_manager import load_settings
        settings = load_settings()
        self.agent_name = settings.get("agent_name", "JARVIS")
        api_key = settings.get("gemini_api_key", "")
        if not api_key:
            api_key = "DUMMY_KEY_WAITING_FOR_SETUP"
            
        self.client = genai.Client(
            api_key=api_key,
            http_options={"api_version": "v1"}
        )
        self.history = [
            {"role": "user", "parts": [{"text": get_system_prompt(self.agent_name)}]},
            {"role": "model", "parts": [{"text": f"Entendido, Senhor. Protocolo {self.agent_name} ativado. Como posso ajudá-lo?"}]},
        ]

    def get_response(self, user_text):
        try:
            self.history.append({"role": "user", "parts": [{"text": user_text}]})
            response = self.client.models.generate_content(
                model=MODEL,
                contents=self.history,
            )
            reply = response.text
            self.history.append({"role": "model", "parts": [{"text": reply}]})
            return reply
        except Exception as e:
            error_msg = str(e)
            print(f"Erro no Gemini: {error_msg}")
            if "403" in error_msg or "SERVICE_DISABLED" in error_msg:
                try:
                    import subprocess
                    subprocess.Popen(["msedge", API_ACTIVATION_URL])
                except FileNotFoundError:
                    webbrowser.open(API_ACTIVATION_URL)
                return "Senhor, a API está desativada. Abri o Edge para você ativá-la."
            if "429" in error_msg:
                return "Senhor, atingi o limite de chamadas por minuto. Aguarde um instante."
            return "Sinto muito, Senhor. Tive um problema técnico nos meus circuitos."
