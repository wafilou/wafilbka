
from pygame import *
import sys


mixer.init()
 
mixer.music.load('music.mp3')
mixer.music.play()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    def update(self):#
        if self.rect.x <= win_width-80 and self.x_speed > 0 or self.rect.x >= 0 and self.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: 
            for p in platforms_touched:
                self.rect.right = p.rect.left
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = p.rect.right
        if self.rect.y <= win_height-80 and self.y_speed > 0 or self.rect.y >= 0 and self.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.y_speed = 0 
                self.rect.top = p.rect.bottom 

    def fire(self): #
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 150, 20, 1)
        bullets.add(bullet)

class Enemy(GameSprite): #

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.side = "left"

    def update(self):
        if self.rect.x <= 420:
            self.side = "right"
        if self.rect.x >= win_width-85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite): #
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width+10:
            self.kill()

win_width = 800
win_height = 600
window = display.set_mode((win_width, win_height))
display.set_caption("Лабиринт")
#back = (119, 210, 223)
back = transform.scale(image.load('fon.jpg'), (win_width, win_height))

barriers = sprite.Group() 
bullets = sprite.Group() #
monsters = sprite.Group() #

w1 = GameSprite('platform1.png',116, 250, 300, 50)
w2 = GameSprite('platform2.png', 370, 100, 50, 400)
w3 = GameSprite('platform1.png',370,100,50,400)
w4 = GameSprite('platform1.png',70,300,200,40)
barriers.add(w1) 
barriers.add(w2) 
barriers.add(w3)
barriers.add(w4)

packman = Player('hero.png', 5, 420, 80, 80, 0, 0)

monster = Enemy('cyborg.png', win_width - 80, 180, 80, 80, 5) 
final_sprite = GameSprite('pac-1.png', win_width - 85, win_height - 100, 80, 80) 
monsters.add(monster) #
finish = False 

run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE: #
                packman.fire() #

        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
                
    if finish == False: 

        #window.fill(back)
        window.blit(back, (0,0))
        packman.update()
        bullets.update() #
        packman.reset()
        bullets.draw(window) #
        barriers.draw(window)
        final_sprite.reset()

        sprite.groupcollide(bullets, barriers, True, False) #

        if not(sprite.groupcollide(monsters, bullets, True, True)): #
            monsters.draw(window) #
            monsters.update() #
        
        if sprite.spritecollide(packman, monsters, True): #
            finish = True
            img = image.load('game-over_1.png')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
        
        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('thumb.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))

    time.delay(50)
    display.update()
