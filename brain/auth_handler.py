import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Escopos válidos para a API do Gemini
SCOPES = ['https://www.googleapis.com/auth/generative-language.tuning',
          'https://www.googleapis.com/auth/cloud-platform',
          'https://www.googleapis.com/auth/generative-language']

class AuthHandler:
    def __init__(self, client_secret_path):
        self.client_secret_path = client_secret_path
        self.token_path = 'token.json'

    def get_credentials(self):
        creds = None
        # O arquivo token.json armazena os tokens de acesso e atualização do usuário
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        
        # Se não houver credenciais válidas, peça ao usuário para fazer login.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secret_path, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Salva as credenciais para a próxima execução
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        
        return creds
