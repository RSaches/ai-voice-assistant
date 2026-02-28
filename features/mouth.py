import arcade

def draw_mouth(center_x, center_y, mouth_open_ratio):
    mouth_width = 100
    mouth_height = 20 + (mouth_open_ratio * 60)
    arcade.draw_ellipse_filled(
        center_x, 
        center_y - 80, 
        mouth_width, 
        mouth_height, 
        arcade.color.BLACK_BEAN
    )
