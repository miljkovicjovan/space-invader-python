import pygame 
import random
import math
from pygame import mixer

#initialize pygame
pygame.init()

#created screen
screen = pygame.display.set_mode((700, 500))

#background
background = pygame.image.load('images/background.jpg')

#background sounds
mixer.music.load('sounds/background.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invaders - by Jovan Miljkovic")
icon = pygame.image.load('images/spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('images/spaceship.png')
playerX = 320
playerY = 400
playerX_change = 0
playerY_change = 0
#drawing player
def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy
enemyImg = []
enemyX = []
enemyY =[]
enemyX_change = []
enemyY_change = []
numOfEnemies = 6

for i in range(numOfEnemies):
    enemyImg.append(pygame.image.load('images/alien.png'))
    enemyX.append(random.randint(0, 640))
    enemyY.append(random.randint(20, 100))
    enemyX_change.append(0.6)
    enemyY_change.append(40)
#drawing player
def enemy(x, y):
    screen.blit(enemyImg[i], (x, y))

# Bullet
bulletImg = pygame.image.load('images/bullet.png')
bulletX = 0
bulletY = 400
bulletX_change = 0.3
bulletY_change = 1
bulletState = "ready"#you can't see the bullet on the screen and "fire" is that the bullet is moving
#drawing player
def fire_bullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

#collision
def isCollision(ax, ay, bx, by):
    distance = math.sqrt(math.pow(ax-bx, 2) + math.pow(ay - by, 2))
    if distance < 27:
        return True
    else:
        return False

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
def showScore(x,y):
    score = font.render("Score : " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

# game over text
overfont = pygame.font.Font('freesansbold.ttf', 64)
def gameover():
    overText = overfont.render("GAMEOVER", True, (255,255,255))
    screen.blit(overText, (160, 200))


# Game Loop
running = True
while running:
    # bg color
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether Left or Right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.6
            elif event.key == pygame.K_RIGHT:
                playerX_change = 0.6
            elif event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    bulletSound = mixer.Sound("sounds/laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            playerX_change = 0
            playerY_change = 0

    #player change direction
    playerX += playerX_change
    playerY += playerY_change
    #player boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 640:
        playerX = 640
    if playerY >= 467:
        playerY = 467

    #enemy movement when hitting boundaries 
    for i in range(numOfEnemies):

        #GAME OVER
        if enemyY[i] > 200:
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            gameover()
            break

        enemyX[i] += enemyX_change[i] 
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.6
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 640:
            enemyX_change[i] = -0.6
            enemyY[i] += enemyY_change[i]
            
        #colision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            collisionSound = mixer.Sound("sounds/explosion.wav")
            collisionSound.play()
            bulletY = 400
            bulletState = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 640)
            enemyY[i] = random.randint(20, 100)
        
        enemy(enemyX[i], enemyY[i])

    #bullet movement
    if bulletY <= -5:
        bulletY = 400
        bulletState = "ready"
    if bulletState is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    

    showScore(textX, textY)#showing score
    player(playerX, playerY)# drawing player
    pygame.display.update()#updates the game (basically runs the game)