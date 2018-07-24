import pygame as pg
from buttons import Button
from collisions import detect_collisions
from random import randint, choice


def safe_quit():
    tmp = open('highscore', 'w')
    tmp.write(str(highscore))
    tmp.close()
    tmp = open('UpgradeInfo', 'w')
    tmp.write(str(coins) + '\n')
    tmp.write(str(speed) + '\n')
    tmp.write(str(shields) + '\n')
    tmp.write(str(life) + '\n')
    tmp.close()
    quit()


def draw_pause():
    pg.draw.rect(screen, (255, 255, 255), [10, 10, 10, 20])
    pg.draw.rect(screen, (255, 255, 255), [30, 10, 10, 20])


def play(multiplayer=False):
    global highscore
    global drops
    global powerups
    global score
    player1.x = field_centerx - player1.size // 2
    player2 = Player(field_size[0] - plr_s, field_size[1] - plr_s, plr_s, 2)
    if multiplayer:
        player1.x = 0
    player1.lives = 3
    player1.shields = 1
    drops = []
    powerups = []
    is_playing = True
    timer_limit = 50
    times = 0
    score = 0
    move_dir1 = ''
    move_dir2 = ''
    fire = pg.transform.scale(pg.image.load('resources/fire.png'), (15, 15))
    sfire = pg.transform.scale(pg.image.load('resources/shield_fire.png'), (15, 15))
    bg_front = pg.image.load('resources/bg front.png')
    timer = 0
    multiplayer = multiplayer
    bgs[0].rect.y = -bgs[0].rect.height // 2
    while player1.lives > 0 and player2.lives > 0:
        for i in bgs:
            i.move()
            i.draw()
        screen.blit(bg_front, (0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                safe_quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    move_dir1 = 'l'
                elif event.key == pg.K_RIGHT:
                    move_dir1 = 'r'
                elif event.key == pg.K_DOWN:
                    move_dir1 = ''
                elif event.key == pg.K_SPACE:
                    is_playing = not is_playing

                if multiplayer:
                    if event.key == pg.K_a:
                        move_dir2 = 'l'
                    elif event.key == pg.K_d:
                        move_dir2 = 'r'
                    elif event.key == pg.K_s:
                        move_dir2 = ''
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if quit_button.is_touching_mouse():
                        player1.lives = 0
        if timer > int(timer_limit):
            timer = 0
            drops.append(Drop(randint(0, field_size[0] - 50), 0, 50))
            times += 1
            if timer_limit > 10:
                timer_limit -= 0.1
        if times == 5:
            times = 0
            powerups.append(PowerUp(randint(0, field_size[0] - 25), -25, 25, choice(ptypes)))
        if is_playing:
            player1.draw()
            for i in range(player1.shields):
                shield = pg.transform.scale(pg.image.load('resources/Shield.png'),
                                            (player1.size + i * 2, player1.size + i * 2))
                shield_rect = shield.get_rect()
                shield_rect.centerx = player1.x + player1.size // 2
                shield_rect.centery = player1.y + player1.size // 2
                screen.blit(shield, shield_rect)
            if multiplayer:
                player2.draw()
                for i in range(player2.shields):
                    shield = pg.transform.scale(pg.image.load('resources/Shield.png'),
                                                (player2.size + i * 6, player2.size + i * 6))
                    shield_rect = shield.get_rect()
                    shield_rect.centerx = player2.x + player2.size // 2
                    shield_rect.centery = player2.y + player2.size // 2
                    screen.blit(shield, shield_rect)
            player1.move(move_dir1, 6 + speed)
            if multiplayer:
                player2.move(move_dir2, 6 + speed)
            for i in drops:
                if i.anim_prog > 9:
                    i.move()
                    if i.check_for_floor():
                        score += int(60 - timer_limit) * (int(multiplayer) + 1)
                    if i.check_for_collisions(player1):
                        if player1.shields:
                            player1.shields -= 1
                            score += (60 - int(timer_limit)) * 2 * (int(multiplayer) + 1)
                            player1.lives += 1
                    elif multiplayer:
                        if i.check_for_collisions(player2):
                            if player2.shields:
                                player2.shields -= 1
                                score += (60 - int(timer_limit)) * 2 * (int(multiplayer) + 1)
                                player2.lives += 1
                    i.draw()
                else:
                    i.animation()
            for i in powerups:
                i.move()
                i.check_for_floor()
                i.check_for_collisions(player1)
                if multiplayer:
                    i.check_for_collisions(player2)
                i.draw()
            x_pos = 5
            for i in range(player1.lives):
                screen.blit(fire, (x_pos, field_size[1] - 20))
                x_pos += 17
            x_pos = 5
            for i in range(player1.shields):
                screen.blit(sfire, (x_pos, field_size[1] - 45))
                x_pos += 17
            if multiplayer:
                x_pos = field_size[0] - 20
                for i in range(player2.lives):
                    screen.blit(fire, (x_pos, field_size[1] - 20))
                    x_pos -= 17
                x_pos = field_size[0] - 20
                for i in range(player2.shields):
                    screen.blit(sfire, (x_pos, field_size[1] - 45))
                    x_pos -= 17
            score_rect = font.render(str(score), True, (255, 255, 255)).get_rect()
            score_rect.centerx = field_size[0] // 2
            score_rect.y = 10
            screen.blit(font.render(str(score), True, (255, 255, 255)),
                        score_rect)
            pg.display.flip()
            clk.tick(FPS)
            timer += 1
            if score > highscore:
                highscore = score
        if not is_playing:
            screen.fill((0, 0, 0))
            if quit_button.is_touching_mouse():
                quit_button.draw(randint(field_centerx - 5, field_centerx + 5),
                                 randint(field_centery - 5, field_centery + 5), (255, 0, 0))
            else:
                quit_button.draw(randint(field_centerx - 1, field_centerx + 1),
                                 randint(field_centery - 1, field_centery + 1), (255, 255, 255))
            draw_pause()
            pg.display.flip()


class Background:
    def __init__(self):
        self.pic = pg.image.load('resources/bg back.png')
        self.rect = self.pic.get_rect()
        self.rect.y = -self.rect.height

    def draw(self):
        screen.blit(self.pic, self.rect)

    def move(self):
        self.rect.y += 1
        if self.rect.y == 0:
            bgs.append(Background())
        if self.rect.y == field_size[1]:
            bgs.remove(self)


class PowerUp:
    def __init__(self, x, y, size, type):
        if type == 'life':
            self.pic = pg.transform.scale(pg.image.load('resources/PowerUp(life+).png'), (size, size))
        elif type == 'shield':
            self.pic = pg.transform.scale(pg.image.load('resources/PowerUp(shield).png'), (size, size))
        self.rect = self.pic.get_rect()
        self.x = x
        self.y = y
        self.type = type

    def draw(self):
        screen.blit(self.pic, (self.x, self.y))

    def delete(self):
        if self in powerups:
            powerups.remove(self)

    def check_for_floor(self):
        if self.y >= field_size[1]:
            self.delete()

    def check_for_collisions(self, other):
        global score
        global life
        global shields
        if detect_collisions(self.x, self.y, self.rect[2], self.rect[3], other.x, other.y, other.rect[2],
                             other.rect[3]):
            if self.type == 'life':
                if other.lives < 10 + life:
                    other.lives += 1
                else:
                    if other.shields < 3 + shields:
                        other.shields += 1
                    else:
                        score += 150
            elif self.type == 'shield':
                if other.shields < 3 + shields:
                    other.shields += 1
                else:
                    score += 250
            self.delete()

    def move(self):
        self.y += 3


class Drop:
    def __init__(self, x, y, size):
        self.raw_anim = pg.image.load('resources/animation.png')
        self.anim = []
        self.pic = pg.transform.scale(pg.image.load('resources/Drop.png'), (size, int(size * 2.5)))
        self.rect = self.pic.get_rect()
        self.x = x
        self.y = y
        self.vel = 5
        self.anim_prog = 0
        for i in range(4):
            surf = pg.Surface((100, 250))
            surf.fill((0, 0, 255))
            surf.set_colorkey((0, 0, 255))
            surf.blit(self.raw_anim, (-i * 100, 0))
            self.anim.append(surf)

    def draw(self):
        screen.blit(self.pic, (self.x, self.y))

    def animation(self):
        screen.blit(self.anim[self.anim_prog // 3], (self.x - 25, self.y))
        self.anim_prog += 1

    def delete(self):
        drops.remove(self)

    def check_for_floor(self):
        if self.y >= field_size[1]:
            self.delete()
            return True

    def check_for_collisions(self, other):
        if detect_collisions(self.x, self.y, self.rect[2], self.rect[3], other.x, other.y, other.rect[2],
                             other.rect[3]):
            other.lives -= 1
            self.delete()
            return True

    def move(self):
        self.y += self.vel
        self.vel += 1


class Player:
    def __init__(self, x, y, size, pic):
        self.pics = []
        self.size = size
        self.x = x
        self.y = y
        self.raw = pg.image.load('resources/Player1.png') if pic == 1 else pg.image.load('resources/Player2.png')
        self.look_dir = 0
        self.lives = 3
        self.shields = 1
        self.vel = 0
        for i in range(3):
            surf = pg.Surface((92, 98))
            surf.fill((200, 200, 50))
            surf.set_colorkey((200, 200, 50))
            surf.blit(self.raw, (-i * 92, 0))
            surf = pg.transform.scale(surf, (size, size))
            self.pics.append(surf)
        self.rect = self.pics[0].get_rect()

    def draw(self):
        screen.blit(self.pics[self.look_dir], (self.x, self.y))

    def move(self, dir, speed):
        if dir == 'r':
            if self.x < field_size[0] - self.size:
                self.x += speed
            if self.look_dir == 1:
                self.look_dir = 0
            else:
                self.look_dir = 2
        elif dir == 'l':
            if self.x > 0:
                self.x -= speed
            if self.look_dir == 2:
                self.look_dir = 0
            else:
                self.look_dir = 1
        else:
            self.look_dir = 0


pg.init()

heart = pg.image.load('resources/Heart.png')
bg = pg.image.load('resources/bg.png')
upgrades_bg = pg.image.load('resources/upgrades bg.png')
crown = pg.image.load('resources/crown.png')
coin = pg.transform.scale(pg.image.load('resources/coin.png'), (25, 37))
screenshots = [pg.image.load('screenshots/1.png'), pg.image.load('screenshots/2.png'),
               pg.image.load('screenshots/3.png'), pg.image.load('screenshots/4.png'),
               pg.image.load('screenshots/5.png'), pg.image.load('screenshots/6.png')]
bgs = [Background()]
screenshots_rect = screenshots[0].get_rect()
for i in range(len(screenshots)):
    screenshots.append(pg.transform.scale(screenshots[i], (150, 150)))
    del screenshots[0]
screenshots_rect = screenshots[0].get_rect()

field_size = bg.get_size()
field_centerx = field_size[0] // 2
field_centery = field_size[1] // 2
crown_rect = crown.get_rect()
crown_rect.centerx = field_centerx

screen = pg.display.set_mode(field_size)
pg.display.set_caption('Lava dodge')
pg.display.set_icon(heart)
clk = pg.time.Clock()
font = pg.font.SysFont('resources/Quicksand-Bold.otf', 80, True, False)
font2 = pg.font.SysFont('resources/Quicksand-Bold.otf', 30, False, False)

FPS = 50
plr_s = 100

tmp = open('highscore', 'r')
highscore = int(tmp.readline())
tmp.close()
tmp = open('UpgradeInfo', 'r')
coins = int(tmp.readline())
speed = int(tmp.readline())
shields = int(tmp.readline())
life = int(tmp.readline())
tmp.close()

quit_button = Button(screen, 'quit')
player1 = Player(bg.get_rect()[3] // 2 - plr_s // 2, bg.get_rect()[3] - plr_s, plr_s, 1)
ptypes = ['shield', 'life']
screenshots_rect.centerx = field_centerx
menu_buttons = [Button(screen, 'PLAY(single)'), Button(screen, 'PLAY(multi)'), Button(screen, 'UPGRADES'),
                Button(screen, 'QUIT')]
upgrade_menu_buttons = [Button(screen, '<back'), Button(screen, 'SPEED'), Button(screen, 'SHIELDS'),
                        Button(screen, 'LIFE')]
screenshots_rect.y = field_centery
current_screenshot = choice(screenshots)
curr_menu = 'main'

while True:
    if curr_menu == 'main':
        screen.blit(bg, (0, 0))
        y_pos = 20
        for i in menu_buttons:
            if i.is_touching_mouse():
                i.draw(randint(field_centerx - 3, field_centerx + 3), randint(y_pos - 3, y_pos + 3), (255, 255, 200))
            else:
                i.draw(randint(field_centerx - 1, field_centerx + 1), randint(y_pos - 1, y_pos + 1), (255, 255, 255))
            y_pos += 55

        y_pos -= 25
        crown_rect.y = y_pos
        screen.blit(crown, crown_rect)

        y_pos += 65
        txt = font.render(str(highscore), True, (255, 255, 255))
        txt_rect = txt.get_rect()
        txt_rect.centerx = field_centerx
        txt_rect.y = y_pos
        screen.blit(txt, txt_rect)

        y_pos += 50
        screenshots_rect.y = y_pos
        screen.blit(current_screenshot, screenshots_rect)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                safe_quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in menu_buttons:
                        if i.is_touching_mouse():
                            if i.text == 'QUIT':
                                safe_quit()
                            elif i.text == 'PLAY(single)':
                                play()
                                coins += score // 100
                                current_screenshot = choice(screenshots)
                            elif i.text == 'UPGRADES':
                                curr_menu = 'upgrades'
                            elif i.text == 'PLAY(multi)':
                                play(True)
                                coins += score // 100
                                current_screenshot = choice(screenshots)

        pg.display.flip()
    elif curr_menu == 'upgrades':
        screen.blit(upgrades_bg, (0, 0))
        screen.blit(coin, (10, 10))
        screen.blit(font2.render(str(coins), True, (0, 0, 0)), (40, 20))
        y_pos = 100
        for i in upgrade_menu_buttons:
            if i.is_touching_mouse():
                i.draw(randint(field_centerx - 3, field_centerx + 3), randint(y_pos - 3, y_pos + 3), (0, 255, 0))
                if i.text == 'SPEED':
                    pg.draw.rect(screen, (255, 0, 0), (field_size[0] - 5 * 20 // 2, 10, 10, 5 * 20))
                    pg.draw.rect(screen, (0, 255, 0),
                                 (field_size[0] - 5 * 20 // 2, 5 * 20 + 10, 10, -speed * 20))
                    if speed < 5:
                        screen.blit(font2.render(str((speed + 1) * 120), True,
                                                 (255, 0, 0) if coins < (speed + 1) * 120 else (0, 255, 0)),
                                    (40, 60))
                elif i.text == 'SHIELDS':
                    pg.draw.rect(screen, (255, 0, 0), (field_size[0] - 5 * 20 // 2, 10, 10, 5 * 20))
                    pg.draw.rect(screen, (0, 255, 0),
                                 (field_size[0] - 5 * 20 // 2, 5 * 20 + 10, 10, -shields * 20))
                    if shields < 5:
                        screen.blit(font2.render(str((shields + 1) * 250), True,
                                                 (255, 0, 0) if coins < (shields + 1) * 250 else (0, 255, 0)),
                                    (40, 60))
                elif i.text == 'LIFE':
                    pg.draw.rect(screen, (255, 0, 0), (field_size[0] - 5 * 20 // 2, 10, 10, 5 * 20))
                    pg.draw.rect(screen, (0, 255, 0),
                                 (field_size[0] - 5 * 20 // 2, 5 * 20 + 10, 10, -life * 20))
                    if life < 5:
                        screen.blit(font2.render(str((life + 1) * 150), True,
                                                 (255, 0, 0) if coins < (life + 1) * 150 else (0, 255, 0)), (40, 60))
            else:
                i.draw(randint(field_centerx - 1, field_centerx + 1), randint(y_pos - 1, y_pos + 1), (255, 255, 255))
            y_pos += 55

        for event in pg.event.get():
            if event.type == pg.QUIT:
                safe_quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in upgrade_menu_buttons:
                        if i.is_touching_mouse():
                            if i.text == '<back':
                                curr_menu = 'main'
                            elif i.text == 'SHIELDS':
                                if coins >= 250 * (shields + 1) and shields < 5:
                                    coins -= 250 * (shields + 1)
                                    shields += 1
                            elif i.text == 'SPEED':
                                if coins >= 120 * (speed + 1) and speed < 5:
                                    coins -= 120 * (speed + 1)
                                    speed += 1
                            elif i.text == 'LIFE':
                                if coins >= 150 * (life + 1) and life < 5:
                                    coins -= 150 * (life + 1)
                                    life += 1

        pg.display.flip()
