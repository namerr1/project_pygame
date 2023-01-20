from random import *
from pygame import *
from time import time as timer
class Game(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, chirina=100, dlina=100):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (chirina, dlina))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(Game):

    
    def update(self):
        if self.rect.y < 0:
            self.kill()

        else:
            self.rect.y -= self.speed

class Player(Game):

    def go(self):
        
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < 580:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 3, 30, 50)
        bullets.add(bullet)

class Enemy(Game):
    
    def update(self):
        if self.rect.y > 480:
            self.rect.y = 0
            self.rect.x = randint(0, 600)
            global lost
            lost += 1

        else:
            self.rect.y += self.speed


    

        

window = display.set_mode((700, 500))
display.set_caption('Игра Шутер')
fon = transform.scale(image.load('galaxy.jpg'), (700, 500))
spr1 = Player('rocket.png', 300, 350, 4, 100, 100)
inoplanets = sprite.Group()
bullets = sprite.Group()
asteroid = sprite.Group()
a = 'ufo.png'
for i in range(4):
    x = randint(0, 600)
    speed = randint(1, 5)
    inopl = Enemy(a, x, 0, speed, 100, 100)
    inoplanets.add(inopl)

for i in range(3):
    x = randint(0, 600)
    speed = randint(1, 10)
    aster = Enemy('asteroid.png', x, 0, speed, 50, 50)
    asteroid.add(aster)


    

mixer.init()
mixer.music.load('245.wav')
mixer.music.play()
vol = 1.0
sound1 = mixer.Sound("1.wav") 
sound2 = mixer.Sound('game-won.wav') 
music2 = mixer.Sound('space.ogg')   
sound3 = mixer.Sound("astr.wav") 
clock = time.Clock()
lost = 0  
FPS = 60
game = True
hit = 0
font.init()
font = font.SysFont('Arial', 58)
rel_time = False
lives = 3
fort = 0
a = 'ufo.png'
zvezda1 = Player('df.jpg', 20, 150, 5, 50, 50)
zvezda2 = Player('df.jpg', 70, 150, 5, 50, 50)
zvezda3 = Player('df.jpg', 120, 150, 5, 50, 50)
igrok1 = Player(a, 380, 0, 4, 50, 50)
igrok2 = Player(a, 330, 50, 4, 50, 50)
ogranich = 0
t = 0
finish = False
pobeda = font.render('Вы проиграли!', True, (255, 255, 0))
porazenie = font.render('Вы выиграли!', True, (240 ,230, 140))
nadpic2 = font.render('Wait, reload....', True, (240, 230, 140))

while game:
    k = event.get()
    for m in k:
        if m.type == QUIT:
            game = False
        elif m.type == KEYDOWN:
            if m.key == K_SPACE:
                if ogranich < 5 and not(rel_time):
                    ogranich += 1
                    print(ogranich)
                    spr1.fire()

                if ogranich >= 5 and not(rel_time):
                    rel_time = True
                    start_time = timer()
            if m.key == K_DOWN:
                vol -= 0.1
                mixer.music.set_volume(vol)
            if m.key == K_UP:
                vol += 0.1
                mixer.music.set_volume(vol)
            if m.key == K_r:
                a = '22.jpg'


    if not(finish):
        window.blit(fon, (0, 0))
        lose = font.render('Пропущено ', True, (100 ,120, 10))
        win = font.render('Подбито ', True, (100 ,120, 10))
       
        window.blit(lose, (0, 10))
        igrok1.reset()
        igrok2.reset()
        nadpic1 = font.render(str(lost) + ' *', True, (240, 230, 140))
        nadpic3 = font.render(str(hit) + ' *', True, (240, 230, 140))
        window.blit(nadpic1, (300, 0))
        window.blit(nadpic3, (240, 50))
        window.blit(win, (0, 50))

        if rel_time:
            now_time = timer()
            if now_time - start_time <= 3:
                window.blit(nadpic2, (300, 300))
            else:
                rel_time = False
                ogranich = 0

            

        if lives == 2:
            zvezda1.reset()
            zvezda2.reset()
        if lives == 3:
            zvezda1.reset()
            zvezda2.reset()
            zvezda3.reset()
        if lives == 1:
            zvezda1.reset()
        if lives == 0:
            fon = transform.scale(image.load('21.jpg'), (700, 500))
            mixer.music.stop()
            music2.play()
            

        spr1.reset()
        spr1.go()
        

        inoplanets.update()
        inoplanets.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroid.draw(window)
        asteroid.update()
        sprites_list = sprite.groupcollide(inoplanets, bullets, True, True)
        sprites_list1 = sprite.spritecollide(spr1, asteroid, True)
        if len(sprites_list1) > 0:
            lives -= 1
            mixer.music.set_volume(0.1)
            sound3.play()
            if lives < 0:
                finish = True
                

        for i in sprites_list:
            hit += 1
            
            nadpic3 = font.render(str(hit), True, (240, 230, 140))
        
            window.blit(nadpic3, (0, 90))
            x = randint(0, 600)
            speed = randint(1, 4)
            inopl = Enemy(a, x, 0, speed)
            inoplanets.add(inopl)
        if hit > 9:
            mixer.music.set_volume(0.2)
            music2.stop()
            sound2.play()
            finish = True
            window.blit(porazenie, (200, 200))

        if lost > 30:
            window.blit(pobeda, (200, 200))
            mixer.music.set_volume(0.2)
            music2.stop()
            sound1.play()
            finish = True


        display.update()
        

    else:
        
        pass
     

    
    clock.tick(FPS)

