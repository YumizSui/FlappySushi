import random

import pygame
from settings import WIDTH, HEIGHT, FPS, SUSHI_SPEED, GRAVITY, GAP_SIZE, WEAK_FLAP_THRESHOLD, STRONG_FLAP_THRESHOLD, WEAK_FLAP_STRENGTH, MAX_FLAP_STRENGTH
from assets import load_assets

class Sushi(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)
        self.image = assets['sushi']
        self.rect = self.image.get_rect()
        self.rect.center = (50, HEIGHT // 2)
        self.speed_y = 0

    def update(self):
        self.speed_y += GRAVITY
        self.rect.y += self.speed_y

    def flap(self, held_frames):
        if held_frames < WEAK_FLAP_THRESHOLD:
            self.speed_y = -WEAK_FLAP_STRENGTH
            print('weak flap: held_frames: {}'.format(held_frames))
        else:
            flap_strength = WEAK_FLAP_STRENGTH + min(MAX_FLAP_STRENGTH - WEAK_FLAP_STRENGTH, (held_frames - WEAK_FLAP_THRESHOLD) * (MAX_FLAP_STRENGTH - WEAK_FLAP_STRENGTH) / (STRONG_FLAP_THRESHOLD - WEAK_FLAP_THRESHOLD))
            self.speed_y = -flap_strength
            print('strong flap: held_frames: {}, flap_strength: {}'.format(held_frames, flap_strength))


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, is_bottom, assets):
        pygame.sprite.Sprite.__init__(self)
        self.image = assets['pipe_bottom'] if is_bottom else assets['pipe_top']
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= SUSHI_SPEED



class Game:
    def __init__(self, screen):
        self.screen = screen
        self.assets = load_assets()
        self.background = self.assets['background']
        self.sushi = Sushi(self.assets)
        self.pipes = pygame.sprite.Group()
        self.game_started = False
        self.game_over = False
        self.score = 0
        self.best_score = 0
        self.font = pygame.font.Font(None, 36)
        self.pipe_timer = 0
        self.last_log_time = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.game_over:
                self.restart_game()
            elif not self.game_started:
                self.game_started = True
                self.flap_start_frame = pygame.time.get_ticks()
                self.sushi.flap(0)
            else:
                self.flap_start_frame = pygame.time.get_ticks()
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE and not self.game_over and self.game_started:
            held_frames = (pygame.time.get_ticks() - self.flap_start_frame) // (1000 // FPS)
            self.sushi.flap(held_frames)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.game_over:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def restart_game(self):
        self.game_started = False
        self.game_over = False
        self.score = 0
        self.sushi.rect.center = (50, HEIGHT // 2)
        self.sushi.speed_y = 0
        self.pipes.empty()

    def update(self):
        if not self.game_over and self.game_started:
            self.sushi.update()
            self.pipes.update()

            self.pipe_timer += 1
            if self.pipe_timer >= 80:
                self.pipe_timer = 0
                self.add_pipe_pair()

            if pygame.sprite.spritecollide(self.sushi, self.pipes, False) or self.sushi.rect.y > HEIGHT or self.sushi.rect.y < 0:
                self.game_over = True

            # Update the score
            self.score += 1
            if self.score > self.best_score:
                self.best_score = self.score

        # Logging game state every second
        current_time = pygame.time.get_ticks()
        if current_time - self.last_log_time >= 1000:
            self.last_log_time = current_time
            self.log_game_state()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.sushi.image, self.sushi.rect)
        for pipe in self.pipes:
            self.screen.blit(pipe.image, pipe.rect)

        # Display the best score
        score_text = self.font.render(f"Best: {self.best_score:03d}", True, (255, 255, 255))
        self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

        pygame.display.flip()

    def add_pipe_pair(self):
        gap_y = random.randint(HEIGHT // 8, HEIGHT - GAP_SIZE - HEIGHT // 8)
        pipe_top = Pipe(WIDTH, gap_y - 512, False, self.assets)
        pipe_bottom = Pipe(WIDTH, gap_y + GAP_SIZE, True, self.assets)

        self.pipes.add(pipe_top, pipe_bottom)

    def log_game_state(self):
        print("==== Game State ====")
        print(f"Game over: {self.game_over}")
        print(f"Sushi position: ({self.sushi.rect.x}, {self.sushi.rect.y})")
        print(f"Sushi speed: {self.sushi.speed_y}")

        for i, pipe in enumerate(self.pipes):
            print(f"Pipe {i + 1}: ({pipe.rect.x}, {pipe.rect.y})")
        print("====================")
