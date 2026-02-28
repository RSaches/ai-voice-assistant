import arcade
import math

def draw_pupil(eye_x, eye_y, target_x, target_y):
    # Calcular ângulo e distância para o alvo
    dx = target_x - eye_x
    dy = target_y - eye_y
    angle = math.atan2(dy, dx)
    
    # Limitar o movimento da pupila dentro do olho
    distance = min(15, math.sqrt(dx**2 + dy**2) / 10)
    
    pupil_x = eye_x + math.cos(angle) * distance
    pupil_y = eye_y + math.sin(angle) * distance
    
    arcade.draw_circle_filled(pupil_x, pupil_y, 12, arcade.color.BLACK)

def draw_eyes(center_x, center_y, target_x, target_y):
    eye_offset_x = 70
    eye_offset_y = 50
    eye_radius = 35
    
    left_eye_x = center_x - eye_offset_x
    left_eye_y = center_y + eye_offset_y
    right_eye_x = center_x + eye_offset_x
    right_eye_y = center_y + eye_offset_y
    
    arcade.draw_circle_filled(left_eye_x, left_eye_y, eye_radius, arcade.color.WHITE)
    arcade.draw_circle_filled(right_eye_x, right_eye_y, eye_radius, arcade.color.WHITE)
    
    draw_pupil(left_eye_x, left_eye_y, target_x, target_y)
    draw_pupil(right_eye_x, right_eye_y, target_x, target_y)
