from pygame import *
from time import time as timer
from random import *
from math import *


#####

#####

font.init()
font = font.SysFont("Cascadia Code", 70)
win = font.render("Win", True, (100, 175, 100))
lose = font.render("Lose", True, (175, 100, 100))
counter = font.render("Отбито врагов:", True, (10, 10, 10))

bg = "background.png"
hero = "chuvak.png"
enemy = "chuvakzloy.png"
goal = "kubok.png"
bullet = "kamen.png"

mixer.init()
mixer.music.load("whatislove.ogg")
mixer.music.play()

class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, width, height, speedx, speedy, health):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speedx = speedx
        self.speedy = speedy
        self.www = width
        self.hhh = height
        self.health = health
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):

    def update(self):
        global j_cooldown
        global time_now
        global time_then
        time_now = timer()
        j_cooldown = time_now - time_then
        prevpos = [self.rect.x, self.rect.y]
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x >= self.speedx:
            self.rect.x -= self.speedx
        if keys[K_d] and self.rect.x <= win_w - self.www - self.speedx:
            self.rect.x += self.speedx
        if keys[K_SPACE] and j_cooldown >= 0.5: #and self.rect.y >= self.speedy:
            self.speedy = -15
            time_then = timer()
        self.rect.y += self.speedy

        if self.rect.y < win_h - 100:
            self.speedy += 0.5
        if self.rect.y > win_h - 100:
            self.rect.y = win_h - 100
        """for wall in walls:
            if self.rect.y < """
        """if not sprite.spritecollide(player_char, walls, False):
            self.rect.y += self.speedy
        else:
            self.speedy = 0"""
        """else:
            for wall in walls:
                if sprite.collide_rect(player_char, wall):
                    if wall.rect.y > self.rect.y:
                        self.rect.y -= 1
                        self.speedy = 0
                    if wall.rect.y < self.rect.y:
                        self.rect.y += 1"""

    def fire(self):
        kamen = Bullet("kamen.png", self.rect.right, self.rect.centery, 20, 12, 10, 0.5, 10)
        kamens.add(kamen)
        if mousepos[0] < player_char.rect.x:
            kamen.speedx = abs(player_char.rect.x - mousepos[0]) * -0.075
        if mousepos[0] > player_char.rect.x:
            kamen.speedx = abs(player_char.rect.x - mousepos[0]) * 0.075
        kamen.speedy = (mousepos[1] - player_char.rect.y) * 0.075

class Enemy(GameSprite):
    def update(self):
        if self.rect.x < player_char.rect.x:
            self.speedx = abs(self.speedx)
        if self.rect.x > player_char.rect.x:
            self.speedx = abs(self.speedx) * -1
        self.rect.x += self.speedx

        global time1
        global time2
        global cooldown
        cooldown = 2.5
        time2 = timer()
        if time2 - time1 >= cooldown:
            time1 = timer()
            self.speedy = -5
        if self.rect.y < win_h - 100:
            self.speedy += 0.5
        if self.rect.y > win_h - 120:
            self.rect.y = win_h - 120
        self.rect.y += self.speedy


class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speedx
        self.speedy += 0.5
        self.rect.y += self.speedy
        if self.rect.x > win_w or self.rect.y > win_h:
            self.kill()

win_w = 700
win_h = 500
display.set_caption("Чувак проходит через прямоугольники")
window = display.set_mode((win_w, win_h))
backgrnd = transform.scale(image.load(bg), (win_w, win_h))

player_char = Player(hero, 5, win_h - 100, 50, 80, 10, 0, 1000)
enemy_char = Enemy(enemy, 500, 400, 50, 80, randint(1, 5) * 0.5, 5, 5)
final = GameSprite("kubok.png", 630, 425, 48, 48, 0, 0, 1000000)

enemies = sprite.Group()
enemies.add(enemy_char)
kamens = sprite.Group()

game = True
finish = False
clock = time.Clock()
FPS = 60
time1 = timer()
timee1 = timer()
time_then = timer()
cooldown1 = 1
sp1 = 10
sp2 = 50
en_counter = 0
while game:
    count_text = font.render(str(en_counter), True, (10, 10, 10))

    if timer() - timee1 >= cooldown1:
        a = randint(1,2)
        if a == 1:
            enemies.add(Enemy("chuvakzloy.png", win_w, win_h - 100, 50, 80, randint(sp1, sp2) * 0.05, 5, 5))
        else:
            enemies.add(Enemy("chuvakzloy.png", -50, win_h - 100, 50, 80, randint(sp1, sp2) * 0.05, 5, 5))
        timee1 = timer()
        cooldown1 -= 0.001
        sp1 += 1
        sp2 += 1
 
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                mousepos = mouse.get_pos()
                player_char.fire()
    if finish != True:
        window.blit(backgrnd, (0, 0))
        player_char.reset()
        player_char.update()
        enemies.update()
        enemies.draw(window)
        kamens.update()
        kamens.draw(window)
        window.blit(counter, (10, 10))
        window.blit(count_text, (375, 10))

        if sprite.spritecollide(player_char, enemies, False):
            finish = True
            window.blit(lose, (350, 250))
        """if sprite.spritecollide(player_char, walls, False):
            finish = True
            window.blit(lose, (350, 250))"""
        if sprite.collide_rect(player_char, final):
            finish = True
            window.blit(win, (350, 250))
        for enemy in enemies:
            if sprite.spritecollide(enemy, kamens, True):
                enemy.kill()
                en_counter += 1
#????????????????????????????????????????????????????

    display.update()
    clock.tick(FPS)

