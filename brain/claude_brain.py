import anthropic
from config.i18n import t

MODEL = "claude-haiku-4-5-20251001"

def get_system_prompt(agent_name):
    return t('system_prompt', name=agent_name)


class ClaudeBrain:
    def __init__(self):
        from config.settings_manager import load_settings
        settings = load_settings()
        self.agent_name = settings.get("agent_name", "JARVIS")
        api_key = settings.get("claude_api_key", "")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.history = []

    def reload(self):
        """Reinicia o cliente com a chave mais recente do config."""
        from config.settings_manager import load_settings
        settings = load_settings()
        self.agent_name = settings.get("agent_name", "JARVIS")
        api_key = settings.get("claude_api_key", "")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.history = []

    def get_response(self, user_text):
        try:
            self.history.append({"role": "user", "content": user_text})
            response = self.client.messages.create(
                model=MODEL,
                max_tokens=512,
                system=get_system_prompt(self.agent_name),
                messages=self.history,
            )
            reply = response.content[0].text
            self.history.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            error_msg = str(e)
            print(f"Erro no Claude: {error_msg}")
            if "credit balance is too low" in error_msg or "402" in error_msg:
                import subprocess, webbrowser
                try:
                    subprocess.Popen(["msedge", "https://console.anthropic.com/settings/billing"])
                except FileNotFoundError:
                    webbrowser.open("https://console.anthropic.com/settings/billing")
                return "Senhor, o saldo de créditos do Claude está esgotado. Abri a página de cobrança. Pressione G para usar o Gemini."
            if "401" in error_msg or "authentication" in error_msg.lower():
                return "Senhor, chave de API do Claude inválida. Por favor, verifique as credenciais nas configurações."
            if "429" in error_msg:
                return "Senhor, atingi o limite de chamadas por minuto. Aguarde um instante."
            return "Sinto muito, Senhor. O módulo Claude encontrou uma falha técnica."
