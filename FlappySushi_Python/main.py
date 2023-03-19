import pygame
from settings import WIDTH, HEIGHT, FPS
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("FlappySushi")
    clock = pygame.time.Clock()

    game = Game(screen)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        game.update()
        game.draw()

    pygame.quit()

if __name__ == "__main__":
    main()
