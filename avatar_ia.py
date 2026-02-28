import arcade
import math
import threading
import ctypes
import tkinter as tk
from tkinter import messagebox
from tracking.motion_tracker import MotionTracker
from features.face import draw_face
from features.eyes import draw_eyes
from features.mouth import draw_mouth

# Módulos de IA e Voz
from vocal.stt_handler import STTHandler
from vocal.tts_handler import TTSHandler
from brain.gemini_brain import GeminiBrain
from brain.claude_brain import ClaudeBrain
from config.settings_manager import load_settings, save_settings
from config.updater import check_for_updates, download_and_apply_update
from config.i18n import t

# Configurações da Janela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Avatar IA Interativo - JARVIS"

# Posição/tamanho do botão de engrenagem (⚙)
GEAR_BTN = {"x": SCREEN_WIDTH - 35, "y": SCREEN_HEIGHT - 35, "r": 20}


import tkinter.ttk as ttk

def open_settings_dialog(tts, brain_gemini, brain_claude, on_saved):
    """Abre uma janela Tkinter de configurações usando traduções e Combobox listando Edge-TTS."""
    settings = load_settings()
    agent_name = settings.get("agent_name", "JARVIS")

    root = tk.Tk()
    root.title(t('settings_title', name=agent_name))
    root.configure(bg="#1a1a2e")
    root.resizable(False, False)

    w, h = 500, 360
    user32 = ctypes.windll.user32
    scr_w = user32.GetSystemMetrics(0)
    scr_h = user32.GetSystemMetrics(1)
    root.geometry(f"{w}x{h}+{(scr_w - w) // 2}+{(scr_h - h) // 2}")

    style_lbl = {"bg": "#1a1a2e", "fg": "#7ecfff", "font": ("Arial", 11, "bold")}

    frame = tk.Frame(root, padx=20, pady=16, bg="#1a1a2e")
    frame.pack(fill="both", expand=True)

    # --- Nome do Avatar ---
    tk.Label(frame, text=t('name_lbl'), **style_lbl).grid(row=0, column=0, sticky="w", pady=(0, 4))
    name_var = tk.StringVar(value=agent_name)
    name_entry = tk.Entry(frame, textvariable=name_var, width=50,
                          bg="#16213e", fg="#7ecfff", insertbackground="#7ecfff", font=("Arial", 10))
    name_entry.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 10))

    # --- Voz ---
    tk.Label(frame, text=t('voice_lbl'), **style_lbl).grid(row=2, column=0, sticky="w", pady=(0, 4))
    
    # Criar Combobox
    combo_style = ttk.Style()
    combo_style.theme_use('clam')
    combo_style.configure(
        "TCombobox", 
        fieldbackground="#16213e", 
        background="#1a1a2e", 
        foreground="#7ecfff",
        selectbackground="#2196F3",
        selectforeground="white"
    )
    
    voice_var = tk.StringVar()
    voice_combo = ttk.Combobox(frame, textvariable=voice_var, state="readonly", width=47, font=("Arial", 10))
    voice_combo.grid(row=3, column=0, columnspan=3, sticky="w", pady=(0, 10))
    voice_combo.set(t('loading_voices'))
    
    global_voices_dict = {}
    
    def load_voices_async():
        nonlocal global_voices_dict
        global_voices_dict = tts.get_available_voices()
        
        if global_voices_dict:
            current_id = settings.get("voice", "pt-BR-AntonioNeural")
            voice_list = list(global_voices_dict.keys())
            
            selected_idx = 0
            for i, (k, v) in enumerate(global_voices_dict.items()):
                if v == current_id:
                    selected_idx = i
                    break
            
            root.after(0, lambda: _update_combo(voice_list, selected_idx))
            
    def _update_combo(voice_list, selected_idx):
        voice_combo['values'] = voice_list
        if voice_list:
            voice_combo.current(selected_idx)
            
    threading.Thread(target=load_voices_async, daemon=True).start()

    # --- Chaves API ---
    tk.Label(frame, text=t('gemini_lbl'), **style_lbl).grid(row=4, column=0, sticky="w", pady=(0, 4))
    gemini_var = tk.StringVar(value=settings.get("gemini_api_key", ""))
    gemini_entry = tk.Entry(frame, textvariable=gemini_var, width=50, show="*",
                            bg="#16213e", fg="#7ecfff", insertbackground="#7ecfff")
    gemini_entry.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    def toggle_gemini():
        gemini_entry.config(show="" if gemini_entry.cget("show") == "*" else "*")
    tk.Button(frame, text="👁", command=toggle_gemini, width=3,
              bg="#16213e", fg="white", relief="flat").grid(row=5, column=2, padx=4)

    tk.Label(frame, text=t('claude_lbl'), **style_lbl).grid(row=6, column=0, sticky="w", pady=(0, 4))
    claude_var = tk.StringVar(value=settings.get("claude_api_key", ""))
    claude_entry = tk.Entry(frame, textvariable=claude_var, width=50, show="*",
                            bg="#16213e", fg="#7ecfff", insertbackground="#7ecfff")
    claude_entry.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 15))
    def toggle_claude():
        claude_entry.config(show="" if claude_entry.cget("show") == "*" else "*")
    tk.Button(frame, text="👁", command=toggle_claude, width=3,
              bg="#16213e", fg="white", relief="flat").grid(row=7, column=2, padx=4)

    # --- Botões ---
    def on_save():
        selected_label = voice_var.get()
        # Se tiver escolhido algo válido no combo_dict, pega o ID, senão mantém o anterior
        final_voice = global_voices_dict.get(selected_label, settings.get("voice", "pt-BR-AntonioNeural"))

        new_settings = {
            "agent_name": name_var.get().strip() or "JARVIS",
            "voice": final_voice,
            "gemini_api_key": gemini_var.get().strip(),
            "claude_api_key": claude_var.get().strip(),
        }
        save_settings(new_settings)
        tts.reload_voice()
        brain_gemini.reload()
        brain_claude.reload()
        on_saved(new_settings)
        root.destroy()

    def on_check_updates():
        has_update, remote_sha = check_for_updates()
        if not has_update:
            messagebox.showinfo(t('update_title', name=agent_name), t('no_update'))
            return
            
        res = messagebox.askyesno(
            t('update_title', name=agent_name),
            t('update_avail')
        )
        if res:
            success = download_and_apply_update(remote_sha)
            if success:
                messagebox.showinfo(t('update_title', name=agent_name), t('update_success'))
                root.destroy()
                import sys
                sys.exit(0)
            else:
                messagebox.showerror(t('update_title', name=agent_name), t('update_fail'))

    btn_frame = tk.Frame(frame, bg="#1a1a2e")
    btn_frame.grid(row=8, column=0, columnspan=3, pady=(10,0))
    
    tk.Button(btn_frame, text=t('save_btn'), command=on_save, width=12,
              bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
              relief="flat", padx=4, pady=4).pack(side="left", padx=4)
              
    tk.Button(btn_frame, text=t('update_btn'), command=on_check_updates, width=16,
              bg="#ff9800", fg="white", font=("Arial", 10, "bold"),
              relief="flat", padx=4, pady=4).pack(side="left", padx=4)
              
    tk.Button(btn_frame, text=t('cancel_btn'), command=root.destroy, width=12,
              bg="#444", fg="white", relief="flat", padx=4, pady=4).pack(side="left", padx=4)

    root.mainloop()


class Avatar(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Centralizar janela usando ctypes (instantâneo, sem piscar)
        user32 = ctypes.windll.user32
        scr_w = user32.GetSystemMetrics(0)
        scr_h = user32.GetSystemMetrics(1)
        self.set_location((scr_w - width) // 2, (scr_h - height) // 2)

        self.face_center_x = width // 2
        self.face_center_y = height // 2
        self.target_x = self.face_center_x
        self.target_y = self.face_center_y
        self.mouth_open_ratio = 0.0
        self.time_elapsed = 0.0

        self.tracker = MotionTracker()

        # Configurações iniciais
        settings = load_settings()
        self.agent_name = settings.get("agent_name", "JARVIS")

        # Módulos de IA e configuração
        self.brain_gemini = GeminiBrain()
        self.brain_claude = ClaudeBrain()
        self.active_brain = self.brain_gemini
        self.active_brain_name = "Gemini"

        self.stt = STTHandler()
        self.tts = TTSHandler()

        self.is_processing = False
        self.settings_open = False
        self.status_queue = []

        # Textos de status
        self.status_display = arcade.Text(
            t('space_to_speak', ai=self.active_brain_name),
            10, 10, arcade.color.WHITE, 14
        )
        self.ia_label = arcade.Text(
            f"IA: {self.active_brain_name}  |  G=Gemini  C=Claude  ⚙=Cfg",
            10, SCREEN_HEIGHT - 28, arcade.color.LIGHT_BLUE, 12
        )

        # Forçar setup se chaves ausentes
        self._needs_setup = not settings.get("gemini_api_key") and not settings.get("claude_api_key")

    def on_close(self):
        self.tracker.release()
        super().on_close()

    def on_draw(self):
        self.clear()

        draw_face(self.face_center_x, self.face_center_y)
        draw_eyes(self.face_center_x, self.face_center_y, self.target_x, self.target_y)

        m_ratio = self.mouth_open_ratio if self.tts.is_speaking else 0.0
        draw_mouth(self.face_center_x, self.face_center_y, m_ratio)

        self.status_display.draw()
        self.ia_label.draw()

        # Botão de engrenagem — estilo HUD
        g = GEAR_BTN
        cx, cy, r = g["x"], g["y"], g["r"]
        # Teeth (dentes da engrenagem) — 8 pequenas capsulas em volta
        for i in range(8):
            angle = math.pi * 2 / 8 * i
            tx = cx + math.cos(angle) * (r - 4)
            ty = cy + math.sin(angle) * (r - 4)
            arcade.draw_circle_filled(tx, ty, 5, (30, 140, 220))
        # Anel externo
        arcade.draw_circle_outline(cx, cy, r, (30, 140, 220), 2)
        # Corpo central
        arcade.draw_circle_filled(cx, cy, r - 6, (20, 80, 160))
        # Anel interno
        arcade.draw_circle_outline(cx, cy, r - 6, (100, 200, 255), 1)
        # Buraco central
        arcade.draw_circle_filled(cx, cy, 5, (10, 30, 70))
        # Hover: mostrar "CFG" próximo quando settings_open
        if not self.settings_open:
            arcade.draw_text("CFG", cx - 12, cy - 24, (100, 200, 255), 9, bold=True)

        if self.stt.is_listening:
            arcade.draw_circle_filled(SCREEN_WIDTH - 30, 60, 10, arcade.color.RED)

    def on_mouse_press(self, x, y, button, modifiers):
        g = GEAR_BTN
        dist = ((x - g["x"]) ** 2 + (y - g["y"]) ** 2) ** 0.5
        if dist <= g["r"] and not self.settings_open and not self.is_processing:
            self.settings_open = True
            threading.Thread(target=self._open_settings, daemon=True).start()

    def _open_settings(self):
        def on_saved(new_settings):
            self.agent_name = new_settings.get("agent_name", "JARVIS")
            self.status_queue.append(t('success_msg'))

        open_settings_dialog(self.tts, self.brain_gemini, self.brain_claude, on_saved)
        self.settings_open = False

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and not self.is_processing:
            self.start_voice_interaction()
        elif key == arcade.key.G and not self.is_processing:
            self._switch_brain("Gemini", self.brain_gemini)
        elif key == arcade.key.C and not self.is_processing:
            self._switch_brain("Claude", self.brain_claude)

    def on_key_release(self, key, modifiers):
        """Para a gravação ao soltar ESPAÇO (push-to-talk)."""
        if key == arcade.key.SPACE and self.is_processing:
            self.stt.stop_recording()

    def _switch_brain(self, name, brain):
        self.active_brain = brain
        self.active_brain_name = name
        self.ia_label.text = f"IA: {name}  |  G=Gemini  C=Claude  ⚙=Cfg"
        self.status_queue.append(t('space_to_speak', ai=name))
        self.tts.speak(t('switching', ai=name), None)

    def start_voice_interaction(self):
        self.is_processing = True
        self.stt.start_recording()
        self.status_queue.append(t('recording', ai=self.active_brain_name))
        self.stt.listen_and_transcribe(self.handle_transcription)

    def handle_transcription(self, text):
        if text:
            self.status_queue.append(f"Você: {text[:30]}...")
            response = self.active_brain.get_response(text)
            self.status_queue.append(t('responding', name=self.agent_name, ai=self.active_brain_name))
            self.tts.speak(response, self.interaction_complete)
        else:
            self.status_queue.append(t('not_understood'))
            self.is_processing = False

    def interaction_complete(self):
        self.is_processing = False
        self.status_queue.append(t('space_to_speak', ai=self.active_brain_name))

    def on_mouse_motion(self, x, y, dx, dy):
        self.target_x = x
        self.target_y = y

    def on_update(self, delta_time):
        self.time_elapsed += delta_time

        # Abrir configurações automaticamente no primeiro uso (Thread principal)
        if hasattr(self, '_needs_setup') and self._needs_setup:
            self._needs_setup = False
            self.settings_open = True
            threading.Thread(target=self._open_settings, daemon=True).start()

        while self.status_queue:
            msg = self.status_queue.pop(0)
            self.status_display.text = msg

        pos = self.tracker.get_eye_position()
        if pos:
            self.target_x, self.target_y = pos

        self.mouth_open_ratio = abs(math.sin(self.time_elapsed * 12))


if __name__ == "__main__":
    Avatar(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()
