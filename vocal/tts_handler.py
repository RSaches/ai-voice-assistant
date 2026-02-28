import edge_tts
import asyncio
import pygame
import os
import threading

class TTSHandler:
    def __init__(self):
        from config.settings_manager import load_settings, get_voice_id
        settings = load_settings()
        self.voice = get_voice_id(settings)
        self.is_speaking = False
        pygame.mixer.init()

    def get_available_voices(self) -> dict:
        """Busca todas as vozes e retorna um dict { 'PT-BR - AntonioNeural - Male': 'pt-BR-AntonioNeural' }."""
        try:
            voices = asyncio.run(edge_tts.list_voices())
            # Formato desejado: "PT-BR - AntonioNeural - Male"
            formatted_dict = {}
            for v in voices:
                loc = v.get('Locale', 'Unknown').upper()
                raw_name = v.get('Name', 'Unknown')
                # Extrair o nome curto final do raw_name (ex: pt-BR-AntonioNeural -> AntonioNeural)
                short_name = raw_name.split('-')[-1] if '-' in raw_name else raw_name
                
                g = v.get('Gender', 'Unknown')
                label = f"{loc} - {short_name} - {g}"
                formatted_dict[label] = raw_name
            
            # Ordenar por chave e retornar dicionário ordenado
            return dict(sorted(formatted_dict.items()))
        except Exception as e:
            print(f"Erro ao carregar vozes: {e}")
            return {}

    def reload_voice(self):
        """Recarrega a voz do config.json (chamado após salvar configurações)."""
        from config.settings_manager import load_settings, get_voice_id
        settings = load_settings()
        self.voice = get_voice_id(settings)

    def speak(self, text, completion_callback=None):
        """Converte texto em voz e reproduz."""
        threading.Thread(target=self._run_speak, args=(text, completion_callback), daemon=True).start()

    def _run_speak(self, text, completion_callback):
        asyncio.run(self._speak_async(text, completion_callback))

    async def _speak_async(self, text, completion_callback):
        import time
        import re
        
        # Limpar caracteres markdown ou especiais antes de falar
        clean_text = re.sub(r'[*_#~`\[\]]', '', text)
        
        output_file = f"response_{int(time.time())}.mp3"
        
        communicate = edge_tts.Communicate(clean_text, self.voice)
        await communicate.save(output_file)
        
        self.is_speaking = True
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load(output_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.05)
        except Exception as e:
            print(f"Erro ao tocar áudio: {e}")
        finally:
            self.is_speaking = False
            try:
                pygame.mixer.music.unload()
                os.remove(output_file)
            except:
                pass
        if completion_callback:
            completion_callback()
