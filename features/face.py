import arcade

def draw_face(center_x, center_y):
    # Desenhar a Cabeça (Emoji)
    arcade.draw_circle_filled(
        center_x, center_y, 200, arcade.color.PEACH_PUFF
    )
