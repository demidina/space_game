import pygame
from pygame import mixer
import random
import time

FPS = 60
WINDOW_SIZE = 700, 500
WIN_H = 700
WIN_W = 500
window_color = 0, 0, 255
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, image_filename):
        super().__init__()
        self.image = pygame.image.load(image_filename)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x       
        self.rect.y = y

    def reset(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, x, y, width, height, speed, image_filename):
        super().__init__(x, y, width, height, speed, image_filename)
        self.keys = None
        self.bullets = pygame.sprite.Group()
        self.last_shoot_time = 0
    def set_control(self, key_up, key_down, key_left, key_right, key_fire):
        self.keys = {
            'UP': key_up,
            'DOWN': key_down,
            'LEFT': key_left,
            'RIGHT': key_right,
            'FIRE': key_fire                                    
        }
        
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[self.keys['UP']]:
            self.rect.y -= self.speed
        if pressed_keys[self.keys['DOWN']]:
            self.rect.y += self.speed
        if pressed_keys[self.keys['LEFT']]:
            self.rect.x -= self.speed
        if pressed_keys[self.keys['RIGHT']]:
            self.rect.x += self.speed
        if pressed_keys[self.keys['FIRE']]:
            current_time = time.time()
            if  current_time - self.last_shoot_time > random.uniform(0.3, 1):
                self.fire()
                self.last_shoot_time = current_time

    def fire(self):
        bullet = Bullet(rocket.rect.centerx, rocket.rect.top, 15, 20, 15, 'bullet.png')
        self.bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, pos_x, pos_y, sprite_weight, sprite_height, step_size, sprite_image_file):
        super().__init__(pos_x, pos_y, sprite_weight, sprite_height, step_size, sprite_image_file)
        self.x_start = None
        self.y_start = None
        self.x_end = None
        self.y_end = None

    def set_waypoint(self, x_start, y_start, x_end, y_end):
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end 

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > WIN_H:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, WIN_W - self.rect.width) 

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Label():
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)
    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        main_window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


main_window = pygame.display.set_mode(WINDOW_SIZE)
galaxy = pygame.transform.scale(pygame.image.load('galaxy.jpg'),WINDOW_SIZE)
rocket = Player(350, 430, 30, 50, 4, 'rocket.png')
rocket.set_control(pygame.K_UP, pygame.K_DOWN,pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE)
enemies = pygame.sprite.Group()
for i in range(5):
    enemy = Enemy(random.randint(0, WINDOW_SIZE[0] - 50), random.randint(-100, 40), 50, 50, 2, 'ufo.png')
    enemies.add(enemy)
    enemy.set_waypoint(enemy.rect.x, enemy.rect.y, enemy.rect.x, WIN_H)
pygame.display.set_caption("CONTR STRIKE 1.6")
clock = pygame.time.Clock()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play() 
missed_counter = 0
is_win = False
is_lose = False
is_running = True
while is_running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            is_running = False

    if is_lose:
        result_text = fonr.render('LOSER', True, LOSE_TEXT_COLOR)
        main_window.blit(result_text, (WIN_W, WIN_H))



    hit_amount = len(pygame.sprite.groupcollide(rocket.bullets, enemies, True, True))
    main_window.blit(galaxy,(0, 0))
    rocket.update()
    rocket.reset(main_window)
    enemies.update()
    enemies.draw(main_window)
    rocket.bullets.update()
    rocket.bullets.draw(main_window)
    pygame.display.update()
    clock.tick(FPS)