import pygame

def load_assets():
    assets = {
        "background": pygame.image.load("../resources/background.png"),
        "sushi": pygame.image.load("../resources/sushi.png"),
        "pipe_top": pygame.image.load("../resources/pipe_top.png"),
        "pipe_bottom": pygame.image.load("../resources/pipe_bottom.png"),
    }
    return assets
