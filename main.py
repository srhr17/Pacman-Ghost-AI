import pygame
import math
pygame.init()

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
WINDOW_WIDTH=310*2
WINDOW_HEIGHT=280*2
FPS=60
LPS=4
DELAY=FPS/LPS
UNIT_X=WINDOW_WIDTH/WIDTH
UNIT_Y=WINDOW_HEIGHT/HEIGHT
ANIMATION_X=1/DELAY
ANIMATION_Y=1/DELAY
if UNIT_X<UNIT_Y:
    MIN=UNIT_X
else:
    MIN=UNIT_Y
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
surface=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
clock=pygame.time.Clock()

#Utils
def draw_level():
    surface.fill(BLACK)
    for y in range(0,HEIGHT):
        for x in range(0,WIDTH):
            for e in entities:
                if e.position==[x,y]:
                    draw_entity(e)
                    break
            draw_point(x,y)
    pygame.display.flip()

def get(x,y):
    if 0<=x<WIDTH and 0<=y<=HEIGHT:
        return level[x][y]
    return None

def draw_point(x,y):
    c=level[x][y]
    x*=UNIT_X
    y*=UNIT_Y
    if c=='.':
        pygame.draw.circle(surface,DOT_COLOR,(int(x+UNIT_X/2),int(y+UNIT_Y/2)),int(DOT_RADIUS))
    elif c=='|':
        pygame.draw.rect(surface,WALL_COLOR,(x,y,UNIT_X,UNIT_Y))

def draw_entity(entity):
    x=entity.animation[X]*UNIT_X
    y=entity.animation[Y]*UNIT_Y
    position=(x+PADDING,y+PADDING,UNIT_X-PADDING*2,UNIT_Y-PADDING*2)
    pygame.draw.rect(surface,entity.color,position)

def animate(entity):
    if entity.animation[X]<entity.position[X]:
        entity.animation[X]+=ANIMATION_X
    elif entity.animation[X]>entity.position[X]:
        entity.animation[X]-=ANIMATION_X
    if entity.animation[Y]<entity.position[Y]:
        entity.animation[Y]+=ANIMATION_Y
    elif entity.animation[Y]>entity.position[Y]:
        entity.animation[Y]-=ANIMATION_Y

def animate_restore(entity):
    entity.animation[X]=entity.position[X]
    entity.animation[Y]=entity.position[Y]

def distance(position1,position2):
    difference=(position1[X]-position2[X],position1[Y]-position2[Y])
    return math.sqrt(math.pow(difference[X],2)+math.pow(difference[Y],2))

def border(position):
    if position[X]<0:
        position[X]=WIDTH+position[X]
    elif position[X]>=WIDTH:
        position[X]=position[X]-WIDTH
    if position[Y]<0:
        position[Y]=HEIGHT+position[Y]
    elif position[Y]>=HEIGHT:
        position[Y]=position[Y]-HEIGHT

#Elements definition
pacman=Object()
pacman.icon='C'
pacman.color=YELLOW
pacman.position=[14,23]
def pacman_loop():
    level[pacman.position[X]][pacman.position[Y]]=' '
    position=[pacman.position[X]+pacman.direction[X],pacman.position[Y]+pacman.direction[Y]]
    border(position)
    if get(position[X],position[Y])=='|':
        return
    pacman.position=position
pacman.loop=pacman_loop

red=Object()
red.icon='R'
red.color=RED
red.position=[RED_TARGET[X],RED_TARGET[Y]]
def red_loop():
    red.target[X]=pacman.position[X]
    red.target[Y]=pacman.position[Y]
    ghost_loop(red)

red.loop=red_loop

blue=Object()
blue.icon='B'
blue.color=BLUE
blue.position=[BLUE_TARGET[X],BLUE_TARGET[Y]]
def blue_loop():
    blue.target[X]=pacman.position[X]+pacman.direction[X]*2
    blue.target[Y]=pacman.position[Y]+pacman.direction[Y]*2
    difference=(blue.target[X]-red.position[X],blue.target[Y]-red.position[Y])
    blue.target[X]=blue.target[X]-difference[X]
    blue.target[Y]=blue.target[Y]-difference[Y]
    ghost_loop(blue)
blue.loop=blue_loop

green=Object()
green.icon='G'
green.color=GREEN
green.position=[GREEN_TARGET[X],GREEN_TARGET[Y]]
def green_loop():
    if distance(green.position,pacman.position)<8:
        green.target[X]=GREEN_TARGET[X]
        green.target[Y]=GREEN_TARGET[Y]
    else:
        green.target[X]=pacman.position[X]
        green.target[Y]=pacman.position[Y]
    ghost_loop(green)
green.loop=green_loop

pink=Object()
pink.icon='P'
pink.color=PINK
pink.position=[PINK_TARGET[X],PINK_TARGET[Y]]
def pink_loop():
    pink.target[X]=pacman.position[X]+pacman.direction[X]*4
    pink.target[Y]=pacman.position[Y]+pacman.direction[Y]*4
    ghost_loop(pink)
pink.loop=pink_loop

def ghost_loop(ghost):
    moves=[UP,DOWN,RIGHT,LEFT]
    opposite=(-ghost.direction[X],-ghost.direction[Y])
    moves.remove(opposite)
    nearest=None
    nearest_direction=None
    nearest_distance=1000000
    for m in moves:
        move=(ghost.position[X]+m[X],ghost.position[Y]+m[Y])
        if get(move[X],move[Y])!='|':
            difference=(move[X]-ghost.target[X],move[Y]-ghost.target[Y])
            distance=math.sqrt(math.pow(difference[X],2)+math.pow(difference[Y],2))
            if distance<nearest_distance:
                nearest=move
                nearest_distance=distance
                nearest_direction=m
    ghost.position[X]=nearest[X]
    ghost.position[Y]=nearest[Y]
    border(ghost.position)
    ghost.direction=nearest_direction

entities=[pacman,red,blue,green,pink]
for entity in entities:
    entity.direction=(0,0)
    if entity!=pacman:
        #entity.position=[GHOST_BASE[X],GHOST_BASE[Y]]
        entity.target=[0,0]
        entity.direction=UP
    entity.animation=[entity.position[X],entity.position[Y]]

#Game loop
delay=0
while True:
    delay+=1
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
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                pacman.direction=UP
            elif event.key==pygame.K_LEFT:
                pacman.direction=LEFT
            elif event.key==pygame.K_DOWN:
                pacman.direction=DOWN
            elif event.key==pygame.K_RIGHT:
                pacman.direction=RIGHT


