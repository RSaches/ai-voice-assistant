import cv2

class MotionTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.screen_width = 800
        self.screen_height = 600
        
        # Variáveis para suavização (Exponential Moving Average)
        self.smooth_x = self.screen_width // 2
        self.smooth_y = self.screen_height // 2
        self.alpha = 0.2  # Fator de suavização
        
        # Sensibilidade (multiplicador para pequenos movimentos)
        self.sensitivity = 1.8 

    def get_eye_position(self):
        success, frame = self.cap.read()
        if not success:
            return None

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)

        if len(faces) > 0:
            (fx, fy, fw, fh) = faces[0]
            
            # Centro da face detectada
            raw_center_x = fx + fw // 2
            raw_center_y = fy + fh // 2
            
            # 1. Normalização Relativa (0.0 a 1.0) baseada no centro do frame
            cam_w, cam_h = frame.shape[1], frame.shape[0]
            
            # Distância do centro do frame (em porcentagem)
            # Invertemos o X para efeito espelho
            rel_x = (0.5 - raw_center_x / cam_w) * self.sensitivity
            rel_y = (0.5 - raw_center_y / cam_h) * self.sensitivity
            
            # 2. Mapeamento para coordenadas da tela
            target_x = (self.screen_width // 2) + (rel_x * self.screen_width)
            target_y = (self.screen_height // 2) + (rel_y * self.screen_height)
            
            # 3. Aplicar Suavização EMA
            self.smooth_x = self.alpha * target_x + (1 - self.alpha) * self.smooth_x
            self.smooth_y = self.alpha * target_y + (1 - self.alpha) * self.smooth_y
            
            # Limitar bordas
            self.smooth_x = max(0, min(self.screen_width, self.smooth_x))
            self.smooth_y = max(0, min(self.screen_height, self.smooth_y))

            return self.smooth_x, self.smooth_y
        
        return None

    def release(self):
        self.cap.release()
