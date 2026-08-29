import pygame
import random
from tkinter import messagebox
import sys
import os

def resource_path(relative_path):
    """获取打包后资源的绝对路径"""
    try:
        # PyInstaller 会将资源解压到临时文件夹，路径存在 _MEIPASS 中
        base_path = sys._MEIPASS
    except Exception:
        # 开发环境下，使用当前文件的目录
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

WIDTH,HEIGHT,FPS = 800,600,60
kill_enemys = 0
level = 1
HP = 150
kill = True
isboss = False
right = True
win = False

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('pg编程')
running = True
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self,_7):
        super().__init__()
        self._7 = _7
        self.image = self._7
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 30

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 8
        if keys[pygame.K_RIGHT]:
            self.rect.x += 8
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Bullet(pygame.sprite.Sprite):
    def __init__(self,_1,_2,_3,_4,_5):
        super().__init__()
        self._1 = _1
        self._2 = _2
        self._3 = _3
        self._4 = _4
        self._5 = _5
        self.image = self._1
        self.rect = self.image.get_rect()
        self.rect.centerx = player.rect.centerx
        self.rect.bottom = player.rect.bottom
    def update(self):
        self.rect.y -= 15
        if self.rect.bottom <= 0:
            self.kill()
        if level == 2:
            self.image = self._2
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        if level == 3:
            self.image = self._3
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        if level == 4:
            self.image = self._4
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        if level >= 5:
            self.image = self._5
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center

class Enemy(pygame.sprite.Sprite):
    def __init__(self,_8):
        super().__init__()
        self._8 = _8
        self.image = self._8
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0,WIDTH)
        self.rect.top = 30

    def update(self):
        self.rect.y += 3
        if self.rect.y > HEIGHT:
            self.rect.centerx = random.randint(0,HEIGHT)
            self.rect.top = 30 
        if isboss:
            self.kill()

class Tank(pygame.sprite.Sprite):
    def __init__(self,_9):
        super().__init__()
        self._9 = _9
        self.image = self._9
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0,WIDTH)
        self.rect.top = 30

    def update(self):
        self.rect.y += 3
        if self.rect.y > HEIGHT:
            self.rect.centerx = random.randint(0,HEIGHT)
            self.rect.top = 30
        if isboss:
            self.kill() 

class Tank_Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((5,10))
        self.image.fill('black')
        self.rect = self.image.get_rect()
        self.rect.centerx = tank.rect.centerx
        self.rect.top = tank.rect.top
    def update(self):
        self.rect.y += 6
        if self.rect.top > HEIGHT:
            self.kill()  

class Meteorite(pygame.sprite.Sprite):
    def __init__(self,_10):
        super().__init__()
        self._10 = _10
        self.image = self._10
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0,WIDTH)
        self.rect.top = 30
    def update(self):
        self.rect.y += 4
        if self.rect.y > HEIGHT:
            self.rect.centerx = random.randint(0,WIDTH)
            self.rect.top = 30 
        if isboss:
            self.kill()

class Reward(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((15,15))
        self.image.fill('yellow')
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0,WIDTH)
        self.rect.centery = 0
    def update(self):
        self.rect.y += 3
        if self.rect.y > HEIGHT:
            self.kill()
        if isboss:
            self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((200,200))
        self.image.fill('gray')
        self.rect = self.image.get_rect()
        self.rect.left = 2000
        self.rect.top = 2000
    def update(self):
        global right
        if right:
            self.rect.x += 5
        if right == False:
            self.rect.x -= 5
        if self.rect.right > WIDTH:
            right = False
        if self.rect.left < 0:
            right = True

class Boss_Bullet(pygame.sprite.Sprite):
    def __init__(self,_6):
        super().__init__()
        self._6 = _6
        self.image = self._6
        self.rect = self.image.get_rect()
        self.rect.centerx = boss.rect.centerx
        self.rect.top = boss.rect.top
    def update(self):
        global win
        self.rect.y += 6
        if self.rect.top > HEIGHT:
            self.kill()  
        if HP <= 0:
            self.kill()
            if win == False:
                messagebox.showinfo('game win','game win')
                win = True
            pygame.quit()
        
_1 = pygame.image.load(resource_path(os.path.join('images', '1.png'))).convert()
_2 = pygame.image.load(resource_path(os.path.join('images', '2.png'))).convert()
_3 = pygame.image.load(resource_path(os.path.join('images', '4.png'))).convert()
_4 = pygame.image.load(resource_path(os.path.join('images', '8.png'))).convert()
_5 = pygame.image.load(resource_path(os.path.join('images', '16.png'))).convert()
_6 = pygame.image.load(resource_path(os.path.join('images', 'boss bullet.png'))).convert()
_7 = pygame.image.load(resource_path(os.path.join('images', 'player.png'))).convert()
_8 = pygame.image.load(resource_path(os.path.join('images', 'enemy.png')))
_9 = pygame.image.load(resource_path(os.path.join('images', 'tank.png'))).convert()
_10 = pygame.image.load(resource_path(os.path.join('images', 'Meteorite.png'))).convert()
player = Player(_7)
boss = Boss()
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemys = pygame.sprite.Group()
tanks = pygame.sprite.Group()
tank_bullets = pygame.sprite.Group()
meteorites = pygame.sprite.Group()
rewards = pygame.sprite.Group()
boss_bullets = pygame.sprite.Group()
all_sprites.add(player)
for i in range(6):
    enemy = Enemy(_8)
    all_sprites.add(enemy)
    enemys.add(enemy)
for i in range(3):
    tank = Tank(_9)
    all_sprites.add(tank)
    tanks.add(tank)
for i in range(2):
    meteorite = Meteorite(_10)
    all_sprites.add(meteorite)
    meteorites.add(meteorite)
ENEMY_SHOOT_EVENT = pygame.USEREVENT + 1
BB_SHOOT_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(ENEMY_SHOOT_EVENT,500)
pygame.time.set_timer(BB_SHOOT_EVENT,500)


while running: 
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(_1,_2,_3,_4,_5)
                all_sprites.add(bullet)
                bullets.add(bullet)
        if event.type == ENEMY_SHOOT_EVENT:
            for tank in tanks.sprites():
                tank_bullet = Tank_Bullet()
                all_sprites.add(tank_bullet)
                tank_bullets.add(tank_bullet)
        if event.type == BB_SHOOT_EVENT and isboss:
            boss_bullet = Boss_Bullet(_6)
            all_sprites.add(boss_bullet)
            boss_bullets.add(boss_bullet)
    if kill_enemys >= 100 and isboss == False:
        isboss = True
        all_sprites.add(boss)
        boss.rect.left = 0
        boss.rect.top = 0
    if kill_enemys % 10 == 0 and kill_enemys != 0 and kill:
        reward = Reward()
        all_sprites.add(reward)
        rewards.add(reward)
        kill = False
    hits = pygame.sprite.spritecollide(player,enemys,False)
    if hits:
        messagebox.showinfo('game over','game over')
        running = False
    hits2 = pygame.sprite.groupcollide(enemys,bullets,True,False)
    if hits2:
        kill_enemys += 1
        kill = True
        enemy = Enemy(_8)
        all_sprites.add(enemy)
        enemys.add(enemy)
    hits3 = pygame.sprite.spritecollide(player,tanks,False)
    if hits3:
        messagebox.showinfo('game over','game over')
        running = False
    hits4 = pygame.sprite.groupcollide(tanks,bullets,True,False)
    if hits4:
        kill_enemys += 1
        kill = True
        tank = Tank(_9)
        all_sprites.add(tank)
        tanks.add(tank)
    hits5 = pygame.sprite.spritecollide(player,tank_bullets,False)
    if hits5:
        messagebox.showinfo('game over','game over')
        running = False
    hits6 = pygame.sprite.spritecollide(player,meteorites,False)
    if hits6:
        messagebox.showinfo('game over','game over')
        running = False
    hits7 = pygame.sprite.spritecollide(player,rewards,True)
    if hits7:
        level += 1
    hits8 = pygame.sprite.spritecollide(player,boss_bullets,True)
    if hits8:
        messagebox.showinfo('game over','game over')
        running = False
    hits9 = pygame.sprite.spritecollide(boss,bullets,True)
    if hits9:
        HP -= 5

    all_sprites.update()
    screen.fill('white')
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()