import pygame as pg
from collisions import detect_collisions
from random import randint


def play():
    is_playing = True
    timer_limit = 50
    score = 0
    move_dir = ''
    heart = pg.transform.scale(pg.image.load('Heart.png'), (50, 50))
    shield = pg.transform.scale(pg.image.load('Shield.png'), (player.size, player.size // 3))
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
                elif event.key == pg.K_SPACE:
                    is_playing = not is_playing
        if timer > timer_limit:
            timer = 0
            drops.append(Drop(randint(0, field_size[0] - 50), 0, 50))
            if timer_limit > 20:
                timer_limit -= 1
        if is_playing:
            player.draw()
            screen.blit(heart, (10, 10))
            screen.blit(font.render(' X ' + str(player.lives), False, (0, 0, 0)), (60, 20))
            screen.blit(font.render('score:' + str(score), False, (0, 0, 0)), (10, 100))

            if player.has_shield:
                screen.blit(shield, (player.x, player.y))
            player.move(move_dir, 8)
            for i in drops:
                if i.anim_prog > 9:
                    i.move()
                    if i.check_for_floor():
                        score += 60 - timer_limit
                    if i.check_for_collisions(player):
                        if player.has_shield:
                            player.has_shield = False
                            score += 60 - timer_limit
                            player.lives += 1
                    i.draw()
                else:
                    i.animation()
            pg.display.flip()
            clk.tick(FPS)
            timer += 1
    print(score)


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
        self.has_shield = True
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
drops = []

play()
