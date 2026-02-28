import speech_recognition as sr
import threading
import pyaudio
import wave
import io
import tempfile
import os

class STTHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self._stop_event = threading.Event()

    def start_recording(self):
        """Inicia a gravação (SPACE pressionado)."""
        self._stop_event.clear()

    def stop_recording(self):
        """Finaliza a gravação (SPACE solto)."""
        self._stop_event.set()

    def listen_and_transcribe(self, callback):
        """Grava enquanto start_recording() estiver ativo e _stop_event não for disparado."""
        threading.Thread(target=self._listen, args=(callback,), daemon=True).start()

    def _listen(self, callback):
        """Grava áudio via PyAudio até o stop_event ser chamado, então transcreve."""
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000

        p = pyaudio.PyAudio()
        frames = []

        print("Ouvi... (Gravando — solte ESPAÇO para parar)")
        self.is_listening = True

        try:
            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                            input=True, frames_per_buffer=CHUNK)
            # Grava enquanto o evento de parada não for disparado
            while not self._stop_event.is_set():
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
            stream.stop_stream()
            stream.close()
        except Exception as e:
            print(f"Erro na gravação: {e}")
            self.is_listening = False
            p.terminate()
            callback(None)
            return

        self.is_listening = False
        p.terminate()

        if not frames:
            callback(None)
            return

        # Salvar em arquivo WAV temporário para o recognizer
        tmp_file = tempfile.mktemp(suffix=".wav")
        try:
            with wave.open(tmp_file, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))

            print("Transcrevendo...")
            with sr.AudioFile(tmp_file) as source:
                audio = self.recognizer.record(source)

            text = self.recognizer.recognize_google(audio, language="pt-BR")
            print(f"Transcrita enviada para a IA... [{text}]")
            callback(text)
        except sr.UnknownValueError:
            print("Não entendi o áudio.")
            callback(None)
        except Exception as e:
            print(f"Erro no STT: {e}")
            callback(None)
        finally:
            try:
                os.remove(tmp_file)
            except:
                pass
