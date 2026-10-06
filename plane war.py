import pygame
import random
from PyQt6.QtWidgets import QMessageBox, QApplication
import sys
import os

qt_app = QApplication(sys.argv)

def resource_path(relative_path):
    """获取打包后资源的绝对路径"""
    try:
        # PyInstaller 会将资源解压到临时文件夹，路径存在 _MEIPASS 中
        base_path = sys._MEIPASS
    except Exception:
        # 开发环境下，使用当前文件的目录
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

WIDTH, HEIGHT, FPS = 800, 600, 60

# ---------- 难度配置 ----------
DIFFICULTY_CONFIG = {
    'easy':   {'enemy_speed':2, 'enemy2_speed':2, 'meteor_speed':3, 'enemy2_bullet_speed':4, 'boss_bullet_speed':4, 'enemy_count':4, 'enemy2_count':2, 'meteor_count':1, 'hp':260},
    'normal': {'enemy_speed':3, 'enemy2_speed':3, 'meteor_speed':4, 'enemy2_bullet_speed':6, 'boss_bullet_speed':6, 'enemy_count':6, 'enemy2_count':3, 'meteor_count':2, 'hp':150},
    'hard':   {'enemy_speed':4, 'enemy2_speed':4, 'meteor_speed':5, 'enemy2_bullet_speed':8, 'boss_bullet_speed':9, 'enemy_count':9, 'enemy2_count':5, 'meteor_count':3, 'hp':80},
}
DIFFICULTY_LABEL = {'easy': '简单', 'normal': '普通', 'hard': '困难'}

difficulty = 'normal'
CFG = DIFFICULTY_CONFIG[difficulty].copy()

# 游戏状态机：'MENU' 开始界面 / 'RULES' 规则界面 / 'PLAYING' 游戏中
STATE = 'MENU'

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('飞机大战')
running = True
clock = pygame.time.Clock()

# ---------- 中文字体加载（带缓存）----------
_font_cache = {}
def load_cn_font(size):
    if size in _font_cache:
        return _font_cache[size]
    candidates = [
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/System/Library/Fonts/Hiragino Sans GB.ttc',
        'C:/Windows/Fonts/msyh.ttc',
        'C:/Windows/Fonts/simhei.ttf',
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
    ]
    font = None
    for p in candidates:
        if os.path.exists(p):
            try:
                font = pygame.font.Font(p, size)
                break
            except Exception:
                continue
    if font is None:
        font = pygame.font.Font(None, size)
    _font_cache[size] = font
    return font

# 游戏全局状态
kill_enemys = 0
level = 1
HP = CFG['hp']
kill = True
isboss = False
right = True
win = False

class Player(pygame.sprite.Sprite):
    def __init__(self, _7):
        super().__init__()
        self._7 = _7
        self.image = self._7
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image, 127)
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
    def __init__(self, _1, _2, _3, _4, _5):
        super().__init__()
        self._1 = _1
        self._2 = _2
        self._3 = _3
        self._4 = _4
        self._5 = _5
        self.image = self._1
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image, 127)
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
            self.mask = pygame.mask.from_surface(self.image, 127)
            self.rect.center = old_center
        if level == 3:
            self.image = self._3
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image, 127)
            self.rect.center = old_center
        if level == 4:
            self.image = self._4
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image, 127)
            self.rect.center = old_center
        if level >= 5:
            self.image = self._5
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image, 127)
            self.rect.center = old_center

class Enemy(pygame.sprite.Sprite):
    def __init__(self, _8):
        super().__init__()
        self._8 = _8
        self.image = self._8
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image, 127)
        self.rect.centerx = random.randint(0, WIDTH)
        self.rect.top = 30

    def update(self):
        self.rect.y += CFG['enemy_speed']
        if self.rect.y > HEIGHT:
            self.rect.centerx = random.randint(0, HEIGHT)
            self.rect.top = 30
        if isboss:
            self.kill()

class Enemy2(pygame.sprite.Sprite):
    def __init__(self, _9):
        super().__init__()
        self._9 = _9
        self.image = self._9
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image, 127)
        self.rect.centerx = random.randint(0, WIDTH)
        self.rect.top = 30

    def update(self):
        self.rect.y += CFG['enemy2_speed']
        if self.rect.y > HEIGHT:
            self.rect.centerx = random.randint(0, HEIGHT)
            self.rect.top = 30
        if isboss:
            self.kill()

class Enemy2_Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill('black')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image, 127)
        self.rect.centerx = enemy2.rect.centerx
        self.rect.top = enemy2.rect.top
    def update(self):
        self.rect.y += CFG['enemy2_bullet_speed']
        if self.rect.top > HEIGHT:
            self.kill()

class Meteorite(pygame.sprite.Sprite):
    def __init__(self, _10):
        super().__init__()
        self._10 = _10
        self.image = self._10
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image, 127)
        self.rect.centerx = random.randint(0, WIDTH)
        self.rect.top = 30
    def update(self):
        self.rect.y += CFG['meteor_speed']
        if self.rect.y > HEIGHT:
            self.rect.centerx = random.randint(0, WIDTH)
            self.rect.top = 30
        if isboss:
            self.kill()

class Reward(pygame.sprite.Sprite):
    def __init__(self,_12):
        super().__init__()
        self._12 = _12
        self.image = self._12
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image, 127)
        self.rect.centerx = random.randint(0, WIDTH)
        self.rect.centery = 0
    def update(self):
        self.rect.y += 3
        if self.rect.y > HEIGHT:
            self.kill()
        if isboss:
            self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self, _11):
        super().__init__()
        self._11 = _11
        self.image = self._11
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image, 127)
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
    def __init__(self, _6):
        super().__init__()
        self._6 = _6
        self.image = self._6
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image, 127)
        self.rect.centerx = boss.rect.centerx
        self.rect.top = boss.rect.top
    def update(self):
        global win, STATE
        self.rect.y += CFG['boss_bullet_speed']
        if self.rect.top > HEIGHT:
            self.kill()
        if HP <= 0:
            self.kill()
            if win == False:
                QMessageBox.information(None, '游戏成功', '游戏成功')
                win = True
            STATE = 'MENU'

_1 = pygame.image.load(resource_path(os.path.join('images', '1.png'))).convert()
_2 = pygame.image.load(resource_path(os.path.join('images', '2.png'))).convert()
_3 = pygame.image.load(resource_path(os.path.join('images', '4.png'))).convert()
_4 = pygame.image.load(resource_path(os.path.join('images', '8.png'))).convert()
_5 = pygame.image.load(resource_path(os.path.join('images', '16.png'))).convert()
_6 = pygame.image.load(resource_path(os.path.join('images', 'boss bullet.png'))).convert()
_7 = pygame.image.load(resource_path(os.path.join('images', 'player.png'))).convert_alpha()
_8 = pygame.image.load(resource_path(os.path.join('images', 'enemy.png'))).convert_alpha()
_9 = pygame.image.load(resource_path(os.path.join('images', 'enemy2.png'))).convert_alpha()
_10 = pygame.image.load(resource_path(os.path.join('images', 'Meteorite.png'))).convert_alpha()
_11 = pygame.image.load(resource_path(os.path.join('images', 'boss.png'))).convert_alpha()
_12 = pygame.image.load(resource_path(os.path.join('images', 'reward.png'))).convert_alpha()

# 精灵组与对象（由 reset_game 重建）
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemys = pygame.sprite.Group()
enemy2s = pygame.sprite.Group()
enemy2_bullets = pygame.sprite.Group()
meteorites = pygame.sprite.Group()
rewards = pygame.sprite.Group()
boss_bullets = pygame.sprite.Group()
player = None
boss = None

def set_difficulty(d):
    global difficulty, CFG
    difficulty = d
    CFG = DIFFICULTY_CONFIG[d].copy()

def reset_game():
    """根据当前难度重置所有精灵与全局状态，支持重开游戏"""
    global kill_enemys, level, HP, kill, isboss, right, win, player, boss
    global all_sprites, bullets, enemys, enemy2s, enemy2_bullets, meteorites, rewards, boss_bullets
    kill_enemys = 0
    level = 1
    kill = True
    isboss = False
    right = True
    win = False
    HP = CFG['hp']

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemys = pygame.sprite.Group()
    enemy2s = pygame.sprite.Group()
    enemy2_bullets = pygame.sprite.Group()
    meteorites = pygame.sprite.Group()
    rewards = pygame.sprite.Group()
    boss_bullets = pygame.sprite.Group()

    player = Player(_7)
    boss = Boss(_11)
    all_sprites.add(player)
    for i in range(CFG['enemy_count']):
        enemy = Enemy(_8)
        all_sprites.add(enemy)
        enemys.add(enemy)
    for i in range(CFG['enemy2_count']):
        enemy2 = Enemy2(_9)
        all_sprites.add(enemy2)
        enemy2s.add(enemy2)
    for i in range(CFG['meteor_count']):
        meteorite = Meteorite(_10)
        all_sprites.add(meteorite)
        meteorites.add(meteorite)

# ---------- 界面按钮布局 ----------
start_btn = pygame.Rect(WIDTH//2 - 110, 330, 220, 62)
rules_btn = pygame.Rect(WIDTH//2 - 110, 412, 220, 52)
easy_btn = pygame.Rect(150, 222, 120, 46)
normal_btn = pygame.Rect(340, 222, 120, 46)
hard_btn = pygame.Rect(530, 222, 120, 46)
back_btn = pygame.Rect(WIDTH//2 - 100, 524, 200, 50)

def draw_button(text, rect, color=(70, 130, 180), selected=False):
    mouse = pygame.mouse.get_pos()
    hover = rect.collidepoint(mouse)
    if selected:
        base = (255, 180, 30)
    elif hover:
        base = tuple(min(c + 35, 255) for c in color)
    else:
        base = color
    pygame.draw.rect(screen, base, rect, border_radius=10)
    if selected:
        pygame.draw.rect(screen, (255, 255, 255), rect, width=3, border_radius=10)
    font = load_cn_font(26)
    text_color = (40, 40, 40) if selected else (255, 255, 255)
    surf = font.render(text, True, text_color)
    screen.blit(surf, surf.get_rect(center=rect.center))

def draw_menu():
    screen.fill((18, 28, 48))
    title = load_cn_font(58).render('飞 机 大 战', True, (255, 215, 0))
    screen.blit(title, title.get_rect(center=(WIDTH//2, 110)))

    diff_label = load_cn_font(26).render('选择难度：', True, (220, 220, 220))
    screen.blit(diff_label, (150, 178))
    draw_button('简单', easy_btn, color=(46, 120, 80), selected=(difficulty == 'easy'))
    draw_button('普通', normal_btn, color=(70, 130, 180), selected=(difficulty == 'normal'))
    draw_button('困难', hard_btn, color=(170, 60, 60), selected=(difficulty == 'hard'))

    cur = load_cn_font(22).render('当前难度：' + DIFFICULTY_LABEL[difficulty], True, (180, 220, 255))
    screen.blit(cur, cur.get_rect(center=(WIDTH//2, 290)))

    draw_button('开始游戏', start_btn, color=(46, 160, 67))
    draw_button('游戏规则', rules_btn, color=(70, 130, 180))

    tip = load_cn_font(18).render('提示：游戏中 ← → 移动，空格发射子弹', True, (150, 150, 150))
    screen.blit(tip, tip.get_rect(center=(WIDTH//2, 500)))

RULES_TEXT = [
    '【游戏目标】',
    '操控战机消灭敌机，累计击落 100 架后迎战 BOSS。',
    '',
    '【操作方式】',
    '← → 方向键 左右移动，空格键 发射子弹。',
    '',
    '【升级系统】',
    '拾取黄色奖励道具可升级子弹火力（共 5 级）。',
    '',
    '【难度说明】',
    '简单：敌人少而慢，战机血量更厚。',
    '普通：标准挑战。',
    '困难：敌群密集、移动快、血量薄弱。',
    '',
    '【失败条件】',
    '战机撞上 敌机 / 敌弹 / 陨石 即游戏结束。',
]

def draw_rules():
    screen.fill((18, 28, 48))
    title = load_cn_font(42).render('游戏规则', True, (255, 215, 0))
    screen.blit(title, title.get_rect(center=(WIDTH//2, 56)))
    y = 120
    for line in RULES_TEXT:
        surf = load_cn_font(22).render(line, True, (230, 230, 230))
        screen.blit(surf, (70, y))
        y += 34
    draw_button('返回', back_btn, color=(70, 130, 180))

# 先初始化一局（供菜单之前模块引用的完整性），真正开局由 reset_game 重建
reset_game()

ENEMY_SHOOT_EVENT = pygame.USEREVENT + 1
BB_SHOOT_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(ENEMY_SHOOT_EVENT, 500)
pygame.time.set_timer(BB_SHOOT_EVENT, 500)


while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if STATE == 'MENU':
                if start_btn.collidepoint(event.pos):
                    reset_game()
                    STATE = 'PLAYING'
                elif rules_btn.collidepoint(event.pos):
                    STATE = 'RULES'
                elif easy_btn.collidepoint(event.pos):
                    set_difficulty('easy')
                elif normal_btn.collidepoint(event.pos):
                    set_difficulty('normal')
                elif hard_btn.collidepoint(event.pos):
                    set_difficulty('hard')
            elif STATE == 'RULES':
                if back_btn.collidepoint(event.pos):
                    STATE = 'MENU'
        if event.type == pygame.KEYDOWN and STATE == 'PLAYING':
            if event.key == pygame.K_SPACE:
                bullet = Bullet(_1, _2, _3, _4, _5)
                all_sprites.add(bullet)
                bullets.add(bullet)
        if event.type == ENEMY_SHOOT_EVENT and STATE == 'PLAYING':
            for enemy2 in enemy2s.sprites():
                enemy2_bullet = Enemy2_Bullet()
                all_sprites.add(enemy2_bullet)
                enemy2_bullets.add(enemy2_bullet)
        if event.type == BB_SHOOT_EVENT and STATE == 'PLAYING' and isboss:
            boss_bullet = Boss_Bullet(_6)
            all_sprites.add(boss_bullet)
            boss_bullets.add(boss_bullet)

    if STATE == 'MENU':
        draw_menu()
    elif STATE == 'RULES':
        draw_rules()
    elif STATE == 'PLAYING':
        if kill_enemys >= 100 and isboss == False:
            QMessageBox.information(None, 'BOSS来袭', 'BOSS来袭')
            isboss = True
            all_sprites.add(boss)
            boss.rect.left = 0
            boss.rect.top = 0
        if kill_enemys % 10 == 0 and kill_enemys != 0 and kill:
            reward = Reward(_12)
            all_sprites.add(reward)
            rewards.add(reward)
            kill = False
        CM = pygame.sprite.collide_mask

        hits = pygame.sprite.spritecollide(player, enemys, False, CM)
        if hits:
            QMessageBox.information(None, '游戏结束', '游戏结束')
            STATE = 'MENU'

        hits2 = pygame.sprite.groupcollide(enemys, bullets, True, False, CM)
        if hits2:
            kill_enemys += 1
            kill = True
            enemy = Enemy(_8)
            all_sprites.add(enemy)
            enemys.add(enemy)

        hits3 = pygame.sprite.spritecollide(player, enemy2s, False, CM)
        if hits3:
            QMessageBox.information(None, '游戏结束', '游戏结束')
            STATE = 'MENU'

        hits4 = pygame.sprite.groupcollide(enemy2s, bullets, True, False, CM)
        if hits4:
            kill_enemys += 1
            kill = True
            enemy2 = Enemy2(_9)
            all_sprites.add(enemy2)
            enemy2s.add(enemy2)

        hits5 = pygame.sprite.spritecollide(player, enemy2_bullets, False, CM)
        if hits5:
            QMessageBox.information(None, '游戏结束', '游戏结束')
            STATE = 'MENU'

        hits6 = pygame.sprite.spritecollide(player, meteorites, False, CM)
        if hits6:
            QMessageBox.information(None, '游戏结束', '游戏结束')
            STATE = 'MENU'

        hits7 = pygame.sprite.spritecollide(player, rewards, True, CM)
        if hits7:
            level += 1

        hits8 = pygame.sprite.spritecollide(player, boss_bullets, True, CM)
        if hits8:
            QMessageBox.information(None, '游戏结束', '游戏结束')
            STATE = 'MENU'

        hits9 = pygame.sprite.spritecollide(boss, bullets, True, CM)
        if hits9:
            HP -= 5

        hits10 = pygame.sprite.groupcollide(bullets, rewards, False, True, CM)
        if hits10:
            level += 1

        all_sprites.update()
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
