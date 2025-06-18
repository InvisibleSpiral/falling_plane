import pygame, sys, time, random
from settings import *
from sprites import BG, Ground, Plane, Obsticle

# https://www.youtube.com/watch?v=VUFvY349ess

print("Hello World! - Spiral ™")
reject = ["no", "nah", "nope", "n"]
accept = ["yeah", "yes", "i do", "y"]
ICON = pygame.image.load('flappy bird/assets/main_icon.jpg')

class Game:
    def __init__(self):
        
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Falling Plane - Spiral Clan™')
        pygame.display.set_icon(ICON)
        self.clock = pygame.time.Clock()
        self.active = True
        self.music_state = None
        self.high_score = 0

        # Scales
        bg_height = pygame.image.load('flappy bird/assets/background.jpg').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height
    
        # Sprites
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # Sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.plane = Plane(self.all_sprites, self.scale_factor / 1.3) # else 1.6 or 1.7

        # Timer
        self.obsticle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obsticle_timer, 1200)

        # Text
        self.font = pygame.font.Font('flappy bird/assets/BD_Cartoon_Shout.ttf', 30)
        self.score = 0
        self.start_offset = 0

        # Menu
        self.menu_surface = pygame.image.load('flappy bird/assets/menu.png').convert_alpha()
        self.menu_rect = self.menu_surface.get_rect(center = (WINDOW_WIDTH  // 2, WINDOW_HEIGHT // 2))

        # Music
        self.end_music = pygame.mixer.Sound('flappy bird/assets/end_music.mp3')
        self.background_music = pygame.mixer.Sound('flappy bird/assets/music.mp3')
        self.crash_sound = pygame.mixer.Sound('flappy bird/assets/crash.wav')
        


        # Collision
    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask) or self.plane.rect.top <=0 :
            pygame.time.wait(12) # So kewl
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':  
                    self.crash_sound.set_volume(0.3)
                    self.crash_sound.play()  
                    sprite.kill()
            self.active = False
            self.plane.kill()

    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1200
            if self.score > int(self.high_score):
                self.high_score = int(self.score)
            
            y = WINDOW_HEIGHT // 10
        else:
            y = WINDOW_HEIGHT // 2 + (self.menu_rect.height / 1.5)

            high_score_text = f"High Score: {self.high_score}"
            high_score_surf = self.font.render(high_score_text, True, 'black')
            high_score_rect = high_score_surf.get_rect(midtop = (WINDOW_WIDTH // 2, 25))
            self.display_surface.blit(high_score_surf, high_score_rect)

        score_surf = self.font.render(str(self.score), True, 'black')
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH // 2, y))
        self.display_surface.blit(score_surf, score_rect)

    def run(self):

        last_time = time.time()

        while True:

            # Delta Time
            dt = time.time() - last_time
            last_time = time.time()

            # Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.plane.jump()
                    else:
                        self.crash_sound.stop()
                        self.end_music.stop()
                        self.plane = Plane(self.all_sprites, self.scale_factor / 1.3)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()
                        self.music_state = None  # Reset music when game restarts

                if self.active:
                    if self.music_state != 'background':
                        self.end_music.stop()
                        self.background_music.play(loops=-1)
                        self.music_state = 'background'
                else:
                    if self.music_state != 'end':
                        self.background_music.stop()
                        self.end_music.set_volume(0.5)
                        self.end_music.play(loops=-1)
                        self.music_state = 'end'


                if event.type == self.obsticle_timer and self.active:
                    Obsticle([self.all_sprites, self.collision_sprites], self.scale_factor * round(random.uniform(1.6, 2.7))) # larger mountains with *
            
            # Game Logics
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            if self.active:
                self.collisions()
            else:
                self.display_surface.blit(self.menu_surface, self.menu_rect)

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()