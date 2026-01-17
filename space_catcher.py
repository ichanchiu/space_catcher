import pygame
import random
import os

# 初始化 Pygame & Mixer (音效)
pygame.init()
pygame.mixer.init()

# Constants / 常數設定
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors / 顏色
BLACK = (10, 10, 30)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
RED = (255, 50, 50)
BLUE = (50, 150, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 100)
ORANGE = (255, 128, 0)
CYAN = (0, 255, 255)
PURPLE = (147, 112, 219)

# Game Settings (Updated by Difficulty)

# Game Settings (Updated by Difficulty)
SETTINGS = {
    'player_speed': 8,
    'supply_speed_min': 3,
    'supply_speed_max': 7,
    'planet_speed_min': 2,
    'planet_speed_max': 5,
    'planet_count': 2
}

# Setup Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("太空捕手：星際探險")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')

# Load Sounds (假設已由 generate_sounds.py 產生)
asset_dir = os.path.join(os.path.dirname(__file__), 'assets')
snd_coin = None
snd_explosion = None
snd_select = None

try:
    snd_coin = pygame.mixer.Sound(os.path.join(asset_dir, 'coin.wav'))
    snd_explosion = pygame.mixer.Sound(os.path.join(asset_dir, 'explosion.wav'))
    snd_select = pygame.mixer.Sound(os.path.join(asset_dir, 'select.wav'))
except Exception as e:
    print(f"Warning: Sound files not found. Run generate_sounds.py first. {e}")

# Helper Functions
def draw_text(surf, text, size, x, y, color=WHITE, center=False):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surf.blit(text_surface, text_rect)

def draw_spaceship(surface, x, y, width, height):
    """繪製精緻的太空船"""
    # 機翼
    pygame.draw.polygon(surface, GRAY, [
        (x, y + height), (x + width, y + height), (x + width // 2, y + height // 2)
    ])
    # 機身
    points = [
        (x + width // 2, y),           
        (x + 10, y + height - 5),               
        (x + width - 10, y + height - 5)        
    ]
    pygame.draw.polygon(surface, BLUE, points)
    pygame.draw.polygon(surface, WHITE, points, 2) 

    # 駕駛艙
    pygame.draw.ellipse(surface, CYAN, (x + width//2 - 5, y + height//2 - 10, 10, 20))
    
    # 火焰
    flame_height = random.randint(10, 25)
    flame_points = [
        (x + 15, y + height - 5), 
        (x + width // 2, y + height - 5 + flame_height),
        (x + width - 15, y + height - 5)
    ]
# Sprites
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 50
        self.height = 60
        self.image = pygame.Surface((self.width, self.height + 30), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.image.fill((0,0,0,0))
        draw_spaceship(self.image, 0, 0, self.width, self.height)

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -SETTINGS['player_speed']
        if keystate[pygame.K_RIGHT]:
            self.speedx = SETTINGS['player_speed']
        
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Supply(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size_type = random.choice(['small', 'medium', 'large'])
        if self.size_type == 'small':
            self.radius = 15; self.color = GREEN; self.score_value = 10
        elif self.size_type == 'medium':
            self.radius = 20; self.color = CYAN; self.score_value = 20
        else:
            self.radius = 25; self.color = YELLOW; self.score_value = 30

        self.image = pygame.Surface((self.radius * 2 + 4, self.radius * 2 + 4), pygame.SRCALPHA)
        # 光暈效果
        pygame.draw.circle(self.image, (255, 255, 255, 100), (self.radius+2, self.radius+2), self.radius + 2)
        pygame.draw.circle(self.image, self.color, (self.radius+2, self.radius+2), self.radius)
        # 加上 "+" 號代表補給
        pygame.draw.line(self.image, WHITE, (self.radius+2, 5), (self.radius+2, self.radius*2-1), 3)
        pygame.draw.line(self.image, WHITE, (5, self.radius+2), (self.radius*2-1, self.radius+2), 3)
        
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-300, -50) 
        self.speedy = random.randrange(SETTINGS['supply_speed_min'], SETTINGS['supply_speed_max'])

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.reset_position()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame > 10:
                self.kill()
            else:
                center = self.rect.center
                self.image.fill((0,0,0,0))
                # Expanding circle effect
                r = int(self.size * (self.frame / 10))
                pygame.draw.circle(self.image, ORANGE, (self.size//2, self.size//2), r)
                self.rect = self.image.get_rect()
                self.rect.center = center

class Planet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = random.randint(35, 65)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        
        # 畫壞星球 (紅色/紫色系)
        planet_color = random.choice([(139, 0, 0), (75, 0, 130), (50, 50, 50)])
        pygame.draw.circle(self.image, planet_color, (self.radius, self.radius), self.radius)
        
        # 畫危險標記和紋理
        pygame.draw.circle(self.image, (0,0,0,80), (self.radius-15, self.radius-15), 10) # 坑洞
        pygame.draw.circle(self.image, (0,0,0,80), (self.radius+20, self.radius+10), 15) # 坑洞
        
        # 紅色邊框警告
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius, 2)
        
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-1000, -100)
        self.speedy = random.randrange(SETTINGS['planet_speed_min'], SETTINGS['planet_speed_max'])

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.reset_position()

class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = random.randint(1, 3)
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH)
        self.rect.y = random.randrange(0, HEIGHT)
        self.speedy = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randrange(0, WIDTH)

# 難度選單畫面
def show_start_screen():
    screen.fill(BLACK)
    draw_text(screen, "Space Catcher: Galaxy", 64, WIDTH / 2, HEIGHT / 4, BLUE, center=True)
    draw_text(screen, "Select Difficulty", 22, WIDTH / 2, HEIGHT / 2, WHITE, center=True)
    
    # Buttons
    btn_y = HEIGHT / 2 + 50
    options = [
        ("1. TRAINEE (Easy)", GREEN, {'player_speed': 6, 'supply_speed_min': 2, 'supply_speed_max': 5, 'planet_speed_min': 2, 'planet_speed_max': 4, 'planet_count': 1}),
        ("2. PILOT (Normal)", YELLOW, {'player_speed': 9, 'supply_speed_min': 4, 'supply_speed_max': 8, 'planet_speed_min': 3, 'planet_speed_max': 7, 'planet_count': 3}),
        ("3. COMMANDER (Hard)", RED, {'player_speed': 12, 'supply_speed_min': 6, 'supply_speed_max': 12, 'planet_speed_min': 6, 'planet_speed_max': 10, 'planet_count': 5})
    ]
    
    for i, (text, color, _) in enumerate(options):
        draw_text(screen, text, 30, WIDTH / 2, btn_y + i * 50, color, center=True)
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if snd_select: snd_select.play()
                    return options[0][2]
                if event.key == pygame.K_2:
                    if snd_select: snd_select.play()
                    return options[1][2]
                if event.key == pygame.K_3:
                    if snd_select: snd_select.play()
                    return options[2][2]

def show_game_over_screen(final_score):
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", 64, WIDTH / 2, HEIGHT / 4, RED, center=True)
    draw_text(screen, f"Final Score: {final_score}", 48, WIDTH / 2, HEIGHT / 2, YELLOW, center=True)
    draw_text(screen, "Press Any Key to Restart", 22, WIDTH / 2, HEIGHT * 3 / 4, WHITE, center=True)
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Main Game Logic
running = True
game_state = "MENU" # MENU, PLAYING, GAMEOVER
final_score = 0

all_sprites = pygame.sprite.Group()
supplies = pygame.sprite.Group()
planets = pygame.sprite.Group()
background_stars = pygame.sprite.Group()
player = None

while running:
    if game_state == "MENU":
        new_settings = show_start_screen()
        SETTINGS.update(new_settings)
        
        # Init Game
        all_sprites.empty()
        supplies.empty()
        planets.empty()
        background_stars.empty()
        
        for i in range(50):
            s = Star()
            all_sprites.add(s)
            background_stars.add(s)
            
        player = Player()
        all_sprites.add(player)
        
        for i in range(3):
            s = Supply()
            all_sprites.add(s)
            supplies.add(s)
            
        for i in range(SETTINGS['planet_count']):
            p = Planet()
            all_sprites.add(p)
            planets.add(p)
            
        score = 0
        game_state = "PLAYING"

    elif game_state == "PLAYING":
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()

        # Hits: Supply
        hits = pygame.sprite.spritecollide(player, supplies, True)
        if hits:
            if snd_coin: snd_coin.play()
        for hit in hits:
            score += hit.score_value
            s = Supply()
            all_sprites.add(s)
            supplies.add(s)

        # Hits: Planet
        hits = pygame.sprite.spritecollide(player, planets, False, pygame.sprite.collide_circle)
        if hits:
            # Explosion effect
            for hit in hits:
                expl = Explosion(hit.rect.center, hit.radius * 2)
                all_sprites.add(expl)
            
            if snd_explosion: snd_explosion.play()
            
            # Simple game over sequence: Wait a bit then show game over
            # Draw one last time to show explosion
            screen.fill(BLACK)
            all_sprites.draw(screen)
            draw_text(screen, f"Score: {score}", 30, 20, 20)
            pygame.display.flip()
            pygame.time.delay(500) # Wait for half a second
            
            final_score = score
            game_state = "GAMEOVER"

        # Draw
        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_text(screen, f"Score: {score}", 30, 20, 20)
        pygame.display.flip()

    elif game_state == "GAMEOVER":
        show_game_over_screen(final_score)
        game_state = "MENU" # Back to menu after key press

pygame.quit()
