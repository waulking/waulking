#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      waulk-d
#
# Created:     11/11/2019
# Copyright:   (c) waulk-d 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame
import random
import math
import winsound

#Intialize pygame
pygame.init()

#Create the screen
screen = pygame.display.set_mode((800, 600))

#Background image
background = pygame.image.load('space.jpg')

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('fighter.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('fighter.png')
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append (random.randint(0, 735))
    enemyY.append  (random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

#Ready can't see bullet
#Fire bullet is moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 15
bullet_state = "ready"

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

#Game over text
over_font = pygame.font.Font('freesansbold.ttf',64)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text(x, y):
    over_text = over_font.render("GAME OVER", True, (255,000,000))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 20, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

#Game Loop
running = True

while running:
    #RGB Red, Green, Blue
    screen.fill((0, 0, 0))
    #Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #If keystroke is pressed check right or left
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change = -5

            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                bulletX = playerX
                fire_bullet(playerX,bulletY)
                winsound.PlaySound("pew", winsound.SND_ASYNC)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #Boundry checking forships
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >=736:
        playerX =736

    #Enemy movement

    for i in range(num_of_enemies):

        #Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(200, 250)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        #Collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            winsound.PlaySound("scream", winsound.SND_ASYNC)
        enemy(enemyX[i], enemyY[i], i)

    #Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()


