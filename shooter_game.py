from pygame import *
from random import *
import time as tm

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255,255,255))
lose = font1.render('YOU LOSE!', True, (180,0,0))

font2 = font.SysFont('Arial', 36)

# звуки
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
monster_pass_sound = mixer.Sound('zzz.ogg')  # Добавили звук для монстров

font.init()

lost = 0
score = 0
max_lost = 3
goal = 10
max_bullets = 11
bullets_left = max_bullets

# нам нужны такие картинки:
img_back = "background.png"
img_hero = "dddddd.png"
img_enemy = 'ipuchi.png'
img_bullet = 'bullet.png'

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    def fire(self):
        global bullets_left
        if bullets_left > 0:
            bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
            bullets.add(bullet)
            bullets_left -= 1
            return True
        return False

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            monster_pass_sound.play()  # Воспроизводим звук когда монстр уходит за экран
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

# Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 20)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,6))
    monsters.add(monster)

last_fired = tm.time()
finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if tm.time() - last_fired >= 0.7 and bullets_left > 0:
                    if ship.fire():
                        fire_sound.play()
                        last_fired = tm.time()
            elif e.key == K_ESCAPE:
                run = False
            elif e.key == K_p:
                paused = True
                mixer.music.pause()
                while paused:
                    for e in event.get():
                        if e.type == QUIT:
                            paused = False
                            run = False
                        elif e.type == KEYDOWN:
                            if e.key == K_p:
                                paused = False
                                mixer.music.unpause()
            elif e.key == K_BACKSPACE:
                score = 0
                lost = 0
                bullets_left = max_bullets
                finish = False
                for bullet in bullets:
                    bullet.kill()
                for monster in monsters:
                    monster.rect.x = randint(80, win_width - 80)
                    monster.rect.y = 0

    if not finish:
        window.blit(background,(0,0))
        
        text = font2.render('Счет: ' + str(score), 1, (0,0,0), None)
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено: ' + str(lost), 1, (0,0,0), None)
        window.blit(text_lose, (10, 50))
        
        text_bullets = font2.render('Пули: ' + str(bullets_left) + '/' + str(max_bullets), 1, (0,0,0), None)
        window.blit(text_bullets, (10, 80))

        ship.update()
        monsters.update()
        bullets.update()
        bullets.draw(window)

        ship.reset()
        monsters.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()
    
    time.delay(50)