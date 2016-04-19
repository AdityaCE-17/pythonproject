# -*- coding: utf-8 -*-
#!/usr/bin/env python2

import pygame, random, os

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
TURQUOISE = (175, 238, 238)
YELLOW = (255, 255, 0)
DEMENTOR_SIZE = (30, 40)
DEMENTOR_SPACER = 20
BARRIER_ROW = 10
BARRIER_COLUMN = 5
BULLET_SIZE  = (5, 10)
MISSILE_SIZE = (5, 5)
BLOCK_SIZE = (10, 10)
RES = (800, 600)

class Wizard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.size = (60, 55)
        self.rect = self.image.get_rect()
        self.rect.x = (RES[0] / 2) - (self.size[0] / 2)
        self.rect.y = 520
        self.travel = 7
        self.speed = 350
        self.time = pygame.time.get_ticks()
        
    def update(self):
        self.rect.x += GameState.vector * self.travel
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > RES[0] - self.size[0]:
            self.rect.x = RES[0] - self.size[0]

class Dementor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.size = (DEMENTOR_SIZE) 
        self.rect = self.image.get_rect()
        self.has_moved = [0, 0]
        self.vector = [1, 1]
        self.travel = [(DEMENTOR_SIZE[0] - 7), DEMENTOR_SPACER]
        self.speed = 700
        self.time = pygame.time.get_ticks()

    def update(self):
        if GameState.dementor_time - self.time > self.speed:
            if self.has_moved[0] < 12: 
                self.rect.x += self.vector[0] * self.travel[0]
                self.has_moved[0] +=1
            else:
                if not self.has_moved[1]: 
                    self.rect.y += self.vector[1] * self.travel[1]
                self.vector[0] *= -1 
                self.has_moved = [0, 0]
                self.speed -= 20
                if self.speed <= 100:
                    self.speed = 100
            self.time = GameState.dementor_time

class Ammo(pygame.sprite.Sprite):
    def __init__(self, color, (width, height)):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect() 
        self.speed = 0
        self.vector = 0

    def update(self):
        self.rect.y += self.vector * self.speed
        if self.rect.y < 0 or self.rect.y > RES[1]:
            self.kill()

class Block(pygame.sprite.Sprite):
    def __init__(self, color, (width, height)):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

class GameState:
    pass

class Game(object):
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font('data/LUMOS.ttf', 24)
        self.intro_font = pygame.font.Font('data/HARRYP__.ttf', 72)
        self.screen = pygame.display.set_mode([RES[0], RES[1]])
        self.time = pygame.time.get_ticks()
        self.refresh_rate = 20
        self.rounds_won = 0
        self.level_up = 50
        self.score = 0
        self.lives = 3
        self.Wizard_group = pygame.sprite.Group()
        self.dementor_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.missile_group = pygame.sprite.Group()
        self.barrier_group = pygame.sprite.Group()
        self.all_sprite_list = pygame.sprite.Group()
        self.intro_screen = pygame.image.load(os.path.join('data', 'hp2.jpg')).convert()
        self.background = pygame.image.load(os.path.join('data', 'hp.jpg')).convert()
        pygame.display.set_caption('DEMENTOR DEFENSE - Press ESC to quit')
        pygame.mouse.set_visible(False) 
        Wizard.image = pygame.image.load(os.path.join("data", "wiz.png")).convert()
        Wizard.image.set_colorkey(BLACK)
        Dementor.image = pygame.image.load(os.path.join("data", "d1.jpg")).convert()
        Dementor.image.set_colorkey(GRAY)
        GameState.end_game = False
        GameState.start_screen = True
        GameState.vector = 0
        GameState.shoot_bullet = False

    def control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameState.start_screen = False
                GameState.end_game = True
            if event.type == pygame.KEYDOWN \
            and event.key == pygame.K_ESCAPE:
                if GameState.start_screen:
                    GameState.start_screen = False
                    GameState.end_game = True
                    self.kill_all()
                else:
                    GameState.start_screen = True
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LEFT]:
            GameState.vector = -1
        elif self.keys[pygame.K_RIGHT]:
            GameState.vector = 1
        else:
            GameState.vector = 0
        if self.keys[pygame.K_SPACE]:
            if GameState.start_screen:
                GameState.start_screen = False
                self.lives = 3
                self.score = 0
                self.make_Wizard()
                self.make_defenses()
                self.alien_wave(0)
            else:
                GameState.shoot_bullet = True

    def splash_screen(self):
        while GameState.start_screen:
            self.kill_all()
            self.screen.blit(self.intro_screen, [0, 0])
            self.screen.blit(self.intro_font.render("DEMETOR DEFENSE", 1, WHITE), (265, 120))
            self.screen.blit(self.game_font.render("Press SPACE to play", 1, WHITE), (274, 191))
            pygame.display.flip()
            self.control()

    def make_Wizard(self):
        self.Wizard = Wizard()
        self.Wizard_group.add(self.Wizard)
        self.all_sprite_list.add(self.Wizard)

    def refresh_screen(self):
        self.all_sprite_list.draw(self.screen) 
        self.refresh_scores()
        pygame.display.flip() 
        self.screen.blit(self.background, [0, 0])
        self.clock.tick(self.refresh_rate) 

    def refresh_scores(self):
        self.screen.blit(self.game_font.render("SCORE : " + str(self.score), 1, YELLOW), (10, 8))
        self.screen.blit(self.game_font.render("LIVES : " + str(self.lives), 1, YELLOW), (355, 570))

    def alien_wave(self, speed):
        for column in range(BARRIER_COLUMN):
            for row in range(BARRIER_ROW):
                alien = Dementor()
                alien.rect.y = 65 + (column * (DEMENTOR_SIZE[1] + DEMENTOR_SPACER))
                alien.rect.x = DEMENTOR_SPACER + (row * (DEMENTOR_SIZE[0] + DEMENTOR_SPACER))
                self.dementor_group.add(alien) 
                self.all_sprite_list.add(alien)
                alien.speed -= speed

    def make_bullet(self):
        if GameState.game_time - self.Wizard.time > self.Wizard.speed:
            bullet = Ammo(BLUE, BULLET_SIZE)
            bullet.vector = -1
            bullet.speed = 26
            bullet.rect.x = self.Wizard.rect.x + 28
            bullet.rect.y = self.Wizard.rect.y
            self.bullet_group.add(bullet)
            self.all_sprite_list.add(bullet)
            self.Wizard.time = GameState.game_time
        GameState.shoot_bullet = False

    def make_missile(self):
        if len(self.dementor_group):
            shoot = random.random()
            if shoot <= 0.05:
                shooter = random.choice([alien for alien in self.dementor_group])
                missile = Ammo(RED, MISSILE_SIZE)
                missile.vector = 1
                missile.rect.x = shooter.rect.x + 15
                missile.rect.y = shooter.rect.y + 40
                missile.speed = 10
                self.missile_group.add(missile)
                self.all_sprite_list.add(missile)

    def make_barrier(self, columns, rows, spacer):
        for column in range(columns):
            for row in range(rows):
                barrier = Block(TURQUOISE, (BLOCK_SIZE))
                barrier.rect.x = 55 + (200 * spacer) + (row * 10)
                barrier.rect.y = 450 + (column * 10)
                self.barrier_group.add(barrier)
                self.all_sprite_list.add(barrier)

    def make_defenses(self):
        for spacing, spacing in enumerate(xrange(4)):
            self.make_barrier(3, 12, spacing)

    def kill_all(self):
        for items in [self.bullet_group, self.Wizard_group, 
        self.missile_group, self.dementor_group, self.barrier_group]:
            for i in items:
                i.kill()

    def is_dead(self):
        if self.lives < 1:
            self.screen.blit(self.game_font.render("The battle is lost! You scored: " + str(self.score), 1, YELLOW), (250, 15))
            self.rounds_won = 0
            self.refresh_screen()
            pygame.time.delay(3000)
            return True

    def win_round(self):
        if len(self.dementor_group) < 1:
            self.rounds_won += 1
            self.screen.blit(self.game_font.render("You won round " + str(self.rounds_won) + "  but the battle rages on", 1, YELLOW), (200, 15))
            self.refresh_screen()
            pygame.time.delay(3000)
            return True

    def defenses_breached(self):
        for alien in self.dementor_group:
            if alien.rect.y > 410:
                self.screen.blit(self.game_font.render("The dementors have breached the Patronus shield!", 1, YELLOW), (180, 15))
                self.refresh_screen()
                pygame.time.delay(3000)
                return True

    def calc_collisions(self):
        pygame.sprite.groupcollide(self.missile_group, self.barrier_group, True, True)
        pygame.sprite.groupcollide(self.bullet_group, self.barrier_group, True, True)
        if pygame.sprite.groupcollide(self.bullet_group, self.dementor_group, True, True):
            self.score += 10
        if pygame.sprite.groupcollide(self.Wizard_group, self.missile_group, False, True):
            self.lives -= 1

    def next_round(self):
        for actor in [self.missile_group, 
        self.barrier_group, self.bullet_group]:
            for i in actor:
                i.kill()
        self.alien_wave(self.level_up)
        self.make_defenses()
        self.level_up += 50

    def Main(self):
        while not GameState.end_game:
            while not GameState.start_screen:
                GameState.game_time = pygame.time.get_ticks()
                GameState.dementor_time = pygame.time.get_ticks()
                self.control()
                self.make_missile()
                for actor in [self.Wizard_group, self.bullet_group, 
                self.dementor_group, self.missile_group]:
                    for i in actor:
                        i.update()
                if GameState.shoot_bullet:
                    self.make_bullet()
                self.calc_collisions()
                if self.is_dead() or self.defenses_breached():
                    GameState.start_screen = True
                if self.win_round():
                    self.next_round()
                self.refresh_screen()
            self.splash_screen()
        pygame.quit()

if __name__ == '__main__':
    pv = Game()
    pv.Main()
