# PONG pygame
import sqlite3
import random
import pygame, sys
from pygame.locals import *
from time import sleep

pygame.init()
fps = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# globals
PLAYER = False
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 10
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [0, 0]
ball_vel = [0, 0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0
ai_score = 0
AI_LOOSE = False

PERM_SPEED = 8

# canvas declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Aged_pong')

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel  # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    horz = random.randrange(2, 4)
    vert = random.randrange(1, 3)

    if right == False:
        horz = - horz

    ball_vel = [horz, -vert]


# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, l_score, r_score  # these are floats
    global score1, score2, ai_score  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH - 1, HEIGHT / 2]
    paddle2_pos = [WIDTH + 1 - HALF_PAD_WIDTH, HEIGHT / 2]
    l_score = 0
    r_score = 0
    if random.randrange(0, 2) == 0:
        ball_init(True)
    else:
        ball_init(False)

#Shader Skript

def shader(canvas):
    for x in range(1, HEIGHT+1):
        pygame.draw.line(canvas, BLACK, [0, 4*x], [WIDTH, 4*x], 1)


# draw function of canvas
def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score
    global PLAYER, PERM_SPEED, AI_LOOSE

    canvas.fill(BLACK)
    pygame.draw.line(canvas, WHITE, [WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1)

    pygame.draw.rect(canvas, WHITE, ([WIDTH // 2 - 70, HEIGHT // 2 - 70], [140, 140]), 1)

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel

    if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[1] += paddle2_vel

    #AI check

    #if paddle2_pos[1] == HALF_PAD_HEIGHT or paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT:
    #    PERM_SPEED = - PERM_SPEED
    if paddle2_pos[1] < ball_pos[1]:
        PERM_SPEED = 8
    elif paddle2_pos[1] > ball_pos[1]:
        PERM_SPEED = -8
    else:
        PERM_SPEED = 0

    # update ball
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    # draw paddles and ball
    pygame.draw.rect(canvas, WHITE, ((ball_pos[0]-BALL_RADIUS, ball_pos[1]-BALL_RADIUS), (BALL_RADIUS*2, BALL_RADIUS*2)), 0)

    pygame.draw.polygon(canvas, WHITE, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT],
                                        [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT],
                                        [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT],
                                        [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(canvas, WHITE, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT],
                                        [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT],
                                        [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT],
                                        [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)

    # ball collision check on top and bottom walls
    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    # ball collison check on gutters or paddles
    if round(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and round(ball_pos[1]) in range(round(paddle1_pos[1] - HALF_PAD_HEIGHT), round(paddle1_pos[1] + HALF_PAD_HEIGHT), 1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        r_score += 1
        ball_init(True)
        AI_LOOSE = True


    if round(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and round(ball_pos[1]) in range(round(paddle2_pos[1] - HALF_PAD_HEIGHT), round(paddle2_pos[1] + HALF_PAD_HEIGHT), 1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
        l_score += 1
        ball_init(False)
        AI_LOOSE = True

    # update scores
    if PLAYER:
        myfont1 = pygame.font.Font("OldSchool.ttf", 20)
        label1 = myfont1.render("Score " + str(l_score), 1, (255, 255, 255))
        canvas.blit(label1, (55, 20))

        myfont2 = pygame.font.Font("OldSchool.ttf", 20)
        label2 = myfont2.render("Score " + str(r_score), 1, (255, 255, 255))
        canvas.blit(label2, (425, 20))
    else:
        myfont = pygame.font.Font("OldSchool.ttf", 20)
        ai_label = myfont.render("Score " + str(ai_score//10), 1, (255, 255, 255))
        canvas.blit(ai_label, (WIDTH/2-65, 30))

    shader(canvas)


# keydown handler
def keydown(event):
    global paddle1_vel, paddle2_vel
    global PLAYER
    if PLAYER:
        if event.key == K_UP:
            paddle2_vel = -8
        elif event.key == K_DOWN:
            paddle2_vel = 8
    if event.key == K_w:
        paddle1_vel = -8
    elif event.key == K_s:
        paddle1_vel = 8

def AI():
    global paddle2_vel, PERM_SPEED
    paddle2_vel = PERM_SPEED


# keyup handler
def keyup(event):
    global paddle1_vel, paddle2_vel

    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0

def newName(canvas, con, cur):
    global ai_score, WIDTH
    run = True
    name = [ord('A'), ord('A'), ord('A')]
    id = 0
    while run:
        canvas.fill(BLACK)
        myfont = pygame.font.Font("OldSchool.ttf", 20)
        ai_label = myfont.render("Score " + str(ai_score // 10), 1, (255, 255, 255))
        lable_name = myfont.render(''.join(map(chr, name)), 1, (255, 255, 255))
        canvas.blit(ai_label, (WIDTH / 2 - 65, 30))
        canvas.blit(lable_name, (WIDTH / 2 - 55, 60))
        pygame.draw.rect(canvas, WHITE, ((WIDTH / 2 - 55 + 22*id, 90), (20, 10)), 0)
        shader(canvas)
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    if id < 2:
                        id += 1
                if event.key == K_DOWN:
                    if id > 0:
                        id -= 1
                if event.key == K_w:
                    name[id] += 1
                if event.key == K_s:
                    name[id] -= 1
                if event.key == K_RETURN:
                    run = False

        pygame.display.update()
        fps.tick(60)
    print("INSERT INTO Leader VALUES ('"+''.join(map(chr, name))+"',"+str(ai_score)+")")
    cur.execute("INSERT INTO Leader VALUES ('"+''.join(map(chr, name))+"',"+str(ai_score)+")")
    con.commit()



def EndAI(canvas):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    newName(canvas, con, cur)
    canvas.fill(BLACK)
    run = True
    res = cur.execute('SELECT * FROM Leader ORDER BY score').fetchall()[::-1]
    x = 10
    if len(res) < 10:
        x=len(res)
    for x in range(x):
        font = pygame.font.Font("OldSchool.ttf", 20)
        alfa = font.render(res[x][0]+':'+str(res[x][1]), 1, WHITE)
        canvas.blit(alfa, (WIDTH/16, 30 + 30*x))
    shader(canvas)
    while run:
        pygame.display.update()
        fps.tick(60)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                run = False
            elif event.type == QUIT:
                run = False


def StartScreen(canvas):
    global PLAYER
    check = True
    run = True
    while run:
        canvas.fill(BLACK)
        fontC = pygame.font.Font("OldSchool.ttf", 20)
        labelO = fontC.render("One Player" + "*" * check, 1, WHITE)
        labelT = fontC.render("Two Players" + "*" * (not check), 1, WHITE)
        labelW = fontC.render('PONG', 1, WHITE)
        canvas.blit(labelO, (WIDTH / 2 - 100, HEIGHT / 2 - 30))
        canvas.blit(labelT, (WIDTH / 2 - 100, HEIGHT / 2 + 30))
        canvas.blit(labelW, (WIDTH/16, HEIGHT/4-30))
        shader(canvas)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_x:
                    pygame.quit()
                    sys.exit()
                if event.key == K_w:
                    check = True
                if event.key == K_s:
                    check = False
                if event.key == K_RETURN:
                    PLAYER = not check
                    run = False
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fps.tick(60)


StartScreen(window)

init()

# game loop
while True:

    draw(window)
    if not PLAYER:
        AI()
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_x:
                pygame.quit()
                sys.exit()
            else:
                keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
    if not PLAYER and AI_LOOSE:
        EndAI(window)
        pygame.quit()
        sys.exit()
    pygame.display.update()
    ai_score += 1
    fps.tick(60)