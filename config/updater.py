import os
import sys
import urllib.request
import json
import zipfile
import shutil
import tempfile
import ssl

REPO_USER = "RSaches"
REPO_NAME = "ai-voice-assistant"
BRANCH = "main"

API_URL = f"https://api.github.com/repos/{REPO_USER}/{REPO_NAME}/commits/{BRANCH}"
ZIP_URL = f"https://github.com/{REPO_USER}/{REPO_NAME}/archive/refs/heads/{BRANCH}.zip"

VERSION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "local_version.txt")

# Contexto SSL para evitar erros em algumas conexões
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get_local_version():
    path = os.path.normpath(VERSION_FILE)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def set_local_version(sha):
    path = os.path.normpath(VERSION_FILE)
    with open(path, "w", encoding="utf-8") as f:
        f.write(sha)

def get_remote_version():
    """Consulta a API do GitHub para pegar o SHA do último commit."""
    try:
        req = urllib.request.Request(API_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode())
            return data.get("sha", "")
    except Exception as e:
        print(f"Erro ao verificar atualização: {e}")
        return None

def check_for_updates():
    """Retorna (True, remote_sha) se houver atualização, senão (False, None)."""
    remote_sha = get_remote_version()
    if not remote_sha:
        return False, None
    
    local_sha = get_local_version()
    if remote_sha != local_sha:
        return True, remote_sha
    return False, None

def download_and_apply_update(remote_sha, status_callback=None):
    """Baixa o ZIP do repositório, extrai e substitui os arquivos locais."""
    try:
        if status_callback: status_callback("Baixando atualização...")
        
        # 1. Download do ZIP
        tmp_zip = tempfile.mktemp(suffix=".zip")
        req = urllib.request.Request(ZIP_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response, open(tmp_zip, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            
        if status_callback: status_callback("Extraindo arquivos...")
        
        # 2. Extrair ZIP
        extract_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(tmp_zip, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
        # O GitHub coloca os arquivos dentro de uma pasta 'ai-voice-assistant-main'
        extracted_folder = os.path.join(extract_dir, f"{REPO_NAME}-{BRANCH}")
        
        if not os.path.exists(extracted_folder):
            raise Exception("Pasta não encontrada dentro do ZIP.")

        if status_callback: status_callback("Aplicando atualização (substituindo arquivos)...")
        
        # 3. Substituir arquivos locais (diretório raiz do projeto)
        project_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
        
        for item in os.listdir(extracted_folder):
            s = os.path.join(extracted_folder, item)
            d = os.path.join(project_root, item)
            
            # Ignorar arquivos específicos que não queremos sobrescrever
            if item in ["config.json", "venv", ".git", "__pycache__", "local_version.txt"]:
                continue
                
            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d)
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)
                
        # 4. Atualizar o SHA local
        set_local_version(remote_sha)
        
        # 5. Limpar temp
        os.remove(tmp_zip)
        shutil.rmtree(extract_dir)
        
        if status_callback: status_callback("Atualização concluída! Reinicie o aplicativo.")
        return True
        
    except Exception as e:
        print(f"Update falhou: {e}")
        if status_callback: status_callback(f"Erro na atualização: {e}")
        return False
