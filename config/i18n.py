import locale

def get_system_language():
    """Detecta o idioma do sistema operacional."""
    try:
        loc, _ = locale.getdefaultlocale()
        if loc and loc.lower().startswith('pt'):
            return 'pt'
    except Exception:
        pass
    return 'en'

LANG = get_system_language()

STRINGS = {
    'pt': {
        'settings_title': '⚙ Configurações do {name}',
        'name_lbl': 'Nome do Assistente:',
        'voice_lbl': 'Voz do Assistente:',
        'gemini_lbl': 'Chave API Gemini:',
        'claude_lbl': 'Chave API Claude:',
        'save_btn': 'Salvar',
        'cancel_btn': 'Cancelar',
        'update_btn': 'Verificar Update',
        'loading_voices': 'Carregando vozes...',
        'voice_prompt': 'Selecione uma voz',
        'success_title': '{name}',
        'success_msg': 'Configurações salvas com sucesso!',
        'update_title': '{name} - Atualizador',
        'no_update': 'O sistema já está na versão mais recente!',
        'update_avail': 'Nova arquitetura detectada nos repositórios remotos.\n\nDeseja baixar e aplicar a atualização agora?',
        'update_success': 'Atualização concluída com sucesso!\nO sistema precisa ser reiniciado.',
        'update_fail': 'Falha ao aplicar atualização. Verifique o log.',
        
        # In-App
        'space_to_speak': '[{ai}] Pressione ESPAÇO para falar',
        'recording': '[{ai}] Gravando... (solte ESPAÇO para parar)',
        'listening': '[{ai}] Ouvindo...',
        'not_understood': 'Não entendi nada. Tente de novo.',
        'responding': '{name} ({ai}) respondendo...',
        'switching': 'Alternando para {ai}, Senhor.',
        
        # System Prompts
        'system_prompt': (
            "Você é o {name}. Responda sempre em português brasileiro, "
            "como o assistente virtual inteligente, prestativo e sofisticado do Homem de Ferro. "
            "Mantenha as respostas curtas e diretas para conversação por áudio."
        ),
        'gemini_first_msg': 'Entendido, Senhor. Protocolo {name} ativado. Como posso ajudá-lo?'
    },
    'en': {
        'settings_title': '⚙ {name} Settings',
        'name_lbl': 'Assistant Name:',
        'voice_lbl': 'Assistant Voice:',
        'gemini_lbl': 'Gemini API Key:',
        'claude_lbl': 'Claude API Key:',
        'save_btn': 'Save',
        'cancel_btn': 'Cancel',
        'update_btn': 'Check Updates',
        'loading_voices': 'Loading voices...',
        'voice_prompt': 'Select a voice',
        'success_title': '{name}',
        'success_msg': 'Settings saved successfully!',
        'update_title': '{name} - Updater',
        'no_update': 'The system is already on the latest version!',
        'update_avail': 'New architecture detected in remote repositories.\n\nDo you want to download and apply the update now?',
        'update_success': 'Update completed successfully!\nThe system needs to be restarted.',
        'update_fail': 'Failed to apply update. Check the log.',
        
        # In-App
        'space_to_speak': '[{ai}] Press SPACE to speak',
        'recording': '[{ai}] Recording... (release SPACE to stop)',
        'listening': '[{ai}] Listening...',
        'not_understood': "I didn't catch that. Try again.",
        'responding': '{name} ({ai}) replying...',
        'switching': 'Switching to {ai}, Sir.',
        
        # System Prompts
        'system_prompt': (
            "You are {name}. Always reply in English, "
            "acting as the intelligent, helpful, and sophisticated virtual assistant of Iron Man. "
            "Keep answers short and direct for audio conversation."
        ),
        'gemini_first_msg': 'Understood, Sir. {name} protocol engaged. How may I assist you?'
    }
}

def t(key, **kwargs):
    """Retorna o texto traduzido de acordo com o idioma."""
    text = STRINGS.get(LANG, STRINGS['en']).get(key, key)
    try:
        return text.format(**kwargs)
    except KeyError:
        return text # Evita falha se kwargs não fechar
