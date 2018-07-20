import pygame as pg
from collisions import detect_collisions
from random import randint, choice


def play():
    global drops
    global powerups
    drops = []
    powerups = []
    is_playing = True
    timer_limit = 50
    times = 0
    score = 0
    move_dir = ''
    heart = pg.transform.scale(pg.image.load('Heart.png'), (50, 50))
    shield = pg.transform.scale(pg.image.load('Shield.png'), (player.size, player.size // 3))
    shield2 = pg.transform.scale(pg.image.load('Shield.png'), (int(player.size * 1.5), player.size // 2))
    shield3 = pg.transform.scale(pg.image.load('Shield.png'), (player.size * 2, player.size))
    timer = 0
    while player.lives > 0:
        screen.blit(bg, (0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    move_dir = 'l'
                elif event.key == pg.K_RIGHT:
                    move_dir = 'r'
                elif event.key == pg.K_DOWN:
                    move_dir = ''
                elif event.key == pg.K_UP:
                    player.jump(15)
                elif event.key == pg.K_SPACE:
                    is_playing = not is_playing
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
            player.draw()
            screen.blit(heart, (10, 10))
            screen.blit(font.render(' X ' + str(player.lives), False, (0, 0, 0)), (60, 20))
            screen.blit(font.render('score:' + str(score), False, (0, 0, 0)), (10, 100))
            if player.shields > 0:
                screen.blit(shield, (player.x, player.y))
            if player.shields > 1:
                screen.blit(shield2, (player.x - player.size // 4, player.y - player.size // 10))
            if player.shields > 2:
                screen.blit(shield3, (player.x - player.size // 2, player.y - player.size // 5))
            player.move(move_dir, 8)
            for i in drops:
                if i.anim_prog > 9:
                    i.move()
                    if i.check_for_floor():
                        score += int(60 - timer_limit)
                    if i.check_for_collisions(player):
                        if player.shields:
                            player.shields -= 1
                            score += 60 - int(timer_limit)
                            player.lives += 1
                    i.draw()
                else:
                    i.animation()
            for i in powerups:
                i.move()
                i.check_for_floor()
                i.check_for_collisions(player)
                i.draw()
            pg.display.flip()
            clk.tick(FPS)
            timer += 1
    print(score)


class PowerUp:
    def __init__(self, x, y, size, type):
        if type == 'life':
            self.pic = pg.transform.scale(pg.image.load('PowerUp(life+).png'), (size, size))
        elif type == 'shield':
            self.pic = pg.transform.scale(pg.image.load('PowerUp(shield).png'), (size, size))
        self.rect = self.pic.get_rect()
        self.x = x
        self.y = y
        self.type = type

    def draw(self):
        screen.blit(self.pic, (self.x, self.y))

    def delete(self):
        powerups.remove(self)
        powerups.sort()

    def check_for_floor(self):
        if self.y >= field_size[1]:
            self.delete()

    def check_for_collisions(self, other):
        if detect_collisions(self.x, self.y, self.rect[2], self.rect[3], other.x, other.y, other.rect[2],
                             other.rect[3]):
            if self.type == 'life':
                other.lives += 1
            elif self.type == 'shield' and other.shields < 3:
                other.shields += 1
            self.delete()

    def move(self):
        self.y += 3


class Drop:
    def __init__(self, x, y, size):
        self.raw_anim = pg.image.load('animation.png')
        self.anim = []
        self.pic = pg.transform.scale(pg.image.load('Drop.png'), (size, int(size * 2.5)))
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
        drops.sort()

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
    def __init__(self, x, y, size):
        self.pics = []
        self.size = size
        self.x = x
        self.y = y
        self.raw = pg.image.load('Player.png')
        self.look_dir = 0
        self.lives = 3
        self.shields = 3
        self.vel = 0
        for i in range(3):
            surf = pg.Surface((92, 98))
            surf.fill((200, 200, 50))
            surf.set_colorkey((200, 200, 50))
            surf.blit(self.raw, (-i * 92, 0))
            surf = pg.transform.scale(surf, (size, size))
            self.pics.append(surf)
        self.rect = self.pics[0].get_rect()
        self.jumppower = 0

    def draw(self):
        screen.blit(self.pics[self.look_dir], (self.x, self.y))

    def jump(self, power):
        self.vel = power
        self.jumppower = power

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
        if self.vel < self.jumppower:
            self.y -= self.vel
            self.vel -= 1


pg.init()

bg = pg.image.load('bg.png')
field_size = bg.get_rect()[2:]
screen = pg.display.set_mode(field_size)
clk = pg.time.Clock()
font = pg.font.SysFont('Quicksand-Bold.otf', 50, False, False)
FPS = 50

move_dir = ''
plr_s = 100
y_speed = 0

player = Player(bg.get_rect()[3] // 2 - plr_s // 2, bg.get_rect()[3] - plr_s, plr_s)
ptypes = ['shield', 'life']

play()
