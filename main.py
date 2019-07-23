import pygame
import vector
import sys
pygame.init()
pygame.mixer.set_num_channels(3)

class Object(object):
    pass

#Constants
GHOST_BASE=(14,13)
UP=(0,-1)
DOWN=(0,1)
RIGHT=(1,0)
LEFT=(-1,0)
X=0
Y=1
WIDTH=28
HEIGHT=31
SIZES=(WIDTH,HEIGHT)
WINDOW=vector.multiply_scalar(SIZES,20)
FPS=60
LPS=5
DELAY=FPS/LPS
UNIT=vector.divide(WINDOW,SIZES)
ANIMATION=1/DELAY
if UNIT[X]<UNIT[Y]:
    MIN=UNIT[X]
else:
    MIN=UNIT[Y]
DOT_RADIUS=MIN/4
PADDING=MIN/8
BLACK=(0,0,0)
YELLOW=(255,255,0)
PURPLE=(52,0,118)
PINK=(255,0,255)
RED=(255,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
DOT_COLOR=YELLOW
WALL_COLOR=PURPLE
RED_TARGET=(26,1)
GREEN_TARGET=(4,29)
PINK_TARGET=(1,1)
BLUE_TARGET=(23,29)
PACMAN_HOME=(14,23)

# Reads the map
level=[['' for y in range(0,HEIGHT)] for x in range(0,WIDTH)]
with open('level.txt') as f:
    for y in range(0,HEIGHT):
        for x in range(0,WIDTH):
            read=f.read(1)
            if read=='\n':
                read=f.read(1)
            level[x][y]=read

#Window initialization
surface=pygame.display.set_mode(WINDOW)
clock=pygame.time.Clock()

#Utils
def draw_level():
    surface.fill(BLACK)
    for y in range(0,HEIGHT):
        for x in range(0,WIDTH):
            for e in entities:
                if e.position==(x,y):
                    draw_entity(e)
                    break
            draw_point((x,y))
    pygame.display.flip()

def get(position):
    if 0<=position[X]<WIDTH and 0<=position[Y]<HEIGHT:
        return level[position[X]][position[Y]]
    return None

def draw_point(position):
    c=level[position[X]][position[Y]]
    position=vector.multiply(position,UNIT)
    if c=='.':
        pygame.draw.circle(surface,DOT_COLOR,vector.to_int(vector.add(position,vector.divide_scalar(UNIT,2))),int(DOT_RADIUS))
    elif c=='|':
        pygame.draw.rect(surface,WALL_COLOR,position+UNIT)

def draw_entity(entity):
    animation=vector.add_scalar(vector.multiply(entity.animation,UNIT),PADDING)
    position=animation+vector.subtract_scalar(UNIT,PADDING*2)
    pygame.draw.rect(surface,entity.color,position)

def animate(entity):
    x=0
    y=0
    difference=vector.subtract(entity.animation,entity.position)
    if vector.module(difference)>5:
        animate_restore(entity)
    if entity.animation[X]<entity.position[X]:
        x=ANIMATION
    elif entity.animation[X]>entity.position[X]:
        x=-ANIMATION
    if entity.animation[Y]<entity.position[Y]:
        y=ANIMATION
    elif entity.animation[Y]>entity.position[Y]:
        y=-ANIMATION
    entity.animation=vector.add(entity.animation,(x,y))

def animate_restore(entity):
    entity.animation=entity.position

def distance(position1,position2):
    return vector.module(vector.subtract(position1,position2))

def border(position):
    x=0
    y=0
    if position[X]<0:
        x=WIDTH
    elif position[X]>=WIDTH:
        x=-WIDTH
    if position[Y]<0:
        y=HEIGHT
    elif position[Y]>=HEIGHT:
        y=-HEIGHT
    return vector.add(position,(x,y))

#Elements definition
pacman=Object()
pacman.icon='C'
pacman.color=YELLOW
pacman.position=PACMAN_HOME
def pacman_loop():
    if level[pacman.position[X]][pacman.position[Y]]=='.':
        bite_sound.stop()
        bite_sound.play()
    level[pacman.position[X]][pacman.position[Y]]=' '
    position=vector.add(pacman.position,pacman.direction)
    position=border(position)
    if get(position)=='|':
        return
    pacman.position=position

pacman.loop=pacman_loop

red=Object()
red.icon='R'
red.color=RED
red.position=RED_TARGET
def red_loop():
    red.target=pacman.position
    ghost_loop(red)

red.loop=red_loop

blue=Object()
blue.icon='B'
blue.color=BLUE
blue.position=BLUE_TARGET
def blue_loop():
    blue.target=vector.add(pacman.position,vector.multiply_scalar(pacman.direction,2))
    difference=vector.subtract(blue.target,red.position)
    blue.target=vector.subtract(blue.target,difference)
    ghost_loop(blue)

blue.loop=blue_loop

green=Object()
green.icon='G'
green.color=GREEN
green.position=GREEN_TARGET
def green_loop():
    if distance(green.position,pacman.position)<8:
        green.target=GREEN_TARGET
    else:
        green.target=pacman.position
    ghost_loop(green)

green.loop=green_loop

pink=Object()
pink.icon='P'
pink.color=PINK
pink.position=PINK_TARGET
def pink_loop():
    pink.target=vector.add(pacman.position,vector.multiply_scalar(pacman.direction,4))
    ghost_loop(pink)

pink.loop=pink_loop

def ghost_loop(ghost):
    if ghost.position==pacman.position:
        dead_sound.play()
        pacman.position=PACMAN_HOME
    moves=[UP,DOWN,RIGHT,LEFT]
    opposite=vector.invert(ghost.direction)
    moves.remove(opposite)
    nearest=None
    nearest_direction=None
    for m in moves:
        move=vector.add(ghost.position,m)
        if get(move)!='|':
            if nearest is None or distance(move,ghost.target)<distance(nearest,ghost.target):
                nearest=move
                nearest_direction=m
    ghost.position=nearest
    ghost.position=border(ghost.position)
    ghost.direction=nearest_direction
    if ghost.position==pacman.position:
        dead_sound.play()
        pacman.position=PACMAN_HOME

entities=(pacman,red,blue,green,pink)
for entity in entities:
    entity.direction=(0,0)
    if entity!=pacman:
        #entity.position=[GHOST_BASE[X],GHOST_BASE[Y]]
        entity.target=(0,0)
        entity.direction=UP
    entity.animation=entity.position

#Game loop
delay=0
sound_delay=0
background_sound=pygame.mixer.Sound('background.ogg')
bite_sound=pygame.mixer.Sound('bite.ogg')
dead_sound=pygame.mixer.Sound('dead.ogg')
while True:
    delay+=1
    sound_delay+=1
    if sound_delay>background_sound.get_length()*FPS-10:
        sound_delay=0
        background_sound.stop()
        background_sound.play()
    if delay>=DELAY:
        delay=0
        for entity in entities:
            animate_restore(entity)
            entity.loop()
    for entity in entities:
        animate(entity)
    draw_level()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP or event.key==pygame.K_w:
                pacman.direction=UP
            elif event.key==pygame.K_LEFT or event.key==pygame.K_a:
                pacman.direction=LEFT
            elif event.key==pygame.K_DOWN or event.key==pygame.K_s:
                pacman.direction=DOWN
            elif event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                pacman.direction=RIGHT


