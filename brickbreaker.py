import pygame
from sys import exit

pygame.init()
prozor = pygame.display.set_mode((800, 600))
pygame.display.set_caption("breakout")
clock = pygame.time.Clock()
deltaTime = 0

isOver = False
gameOverSound = pygame.mixer.Sound("assets/audio/gameover.mp3")
hitSound = pygame.mixer.Sound("assets/audio/scoreup.mp3")



player_width = 76
player_height = 16
player_score = 0
player_x = 400 - player_width
player_y = 580 - player_height
player_speed = 350.0

ball_radius = 10
ball_diameter = ball_radius * 2
ball_x = player_x + player_width // 2 - ball_radius
ball_y = player_y - ball_diameter
ball_velocity = [300.0, -300.0]

brick_height = player_height
brick_width = player_width
brick_x = 100
brick_y = 100
brick_gap = 10
brick = pygame.Rect(brick_x,brick_y,brick_width,brick_height)

bricks = []

total_row_width = 9 * brick_width + (9 - 1) * brick_gap

start_x = (800 - total_row_width) // 2 
start_y = 50 

ball_color = (255, 255, 255)
white = (255, 255, 255)
black = (0,0,0)

font = pygame.font.Font("freesansbold.ttf",14)
font2 = pygame.font.Font("freesansbold.ttf",30)
text = font.render(f"{player_score}",True,white,(0,0,0))
textOver = font2.render("GAME OVER", True, (255,0,0),(128,128,128))
textRestart = font2.render("Press R to try again :)", True, (255,0,0),(128,128,128))
textPos = (25,25)
textOverPos = (300,250)
textRestartPos = (250,300)

def updateBall():
    global ball_x,ball_y,ball_velocity,isOver
    ball_x += ball_velocity[0] * deltaTime
    ball_y += ball_velocity[1] * deltaTime

    if ball_x < 0:
        ball_x = 0
        ball_velocity[0] *= -1

    if ball_x + ball_diameter > 800:
        ball_x = 800 - ball_diameter
        ball_velocity[0] *= -1

    if ball_y < 0:
        ball_y = 0
        ball_velocity[1] *= -1

    if ball_y + ball_diameter > 600:
        isOver = True
        pygame.mixer.Sound.play(gameOverSound)

def drawEntities():
    global prozor,text,textPos,bricks,player,white,ball_color,ball
    prozor.fill("black")
    prozor.blit(text,textPos)
    for i in bricks:
        pygame.draw.rect(prozor,white,i)

    pygame.draw.rect(prozor, white, player)
    pygame.draw.rect(prozor, ball_color, ball)
    pygame.display.flip()

def updateBricks():
    global isOver, ball_velocity, ball_x, ball_y, bricks, player_score
    for i in bricks:
        if ball.colliderect(i):
            bricks.remove(i)
            ball_velocity[1] *= -1
            player_score += 1
            pygame.mixer.Sound.play(hitSound)

def checkVictory():
    global bricks
    if len(bricks) == 0:
        isOver = True
    

def restartGame():
    global isOver, player_score, player_x, player_y, ball_x, ball_y
    isOver = False
    player_score = 0
    bricks.clear()
    loadBricks()
    player_x = 400 - player_width
    player_y = 580 - player_height
    ball_x = player_x + player_width // 2 - ball_radius
    ball_y = player_y - ball_diameter
    prozor.fill("black")
    pygame.display.flip()
    pygame.display.update()

def loadBricks():
    for i in range(10):
        for j in range(9):
            brick_x = start_x + j * (brick_width + brick_gap)
            brick_y = start_y + i * (brick_height + brick_gap)
            brick = pygame.Rect(brick_x,brick_y,brick_width,brick_height)
            bricks.append(brick)

def checkPlayerInput(keys):
    global player_x, player_speed, player_width
    if keys[pygame.K_a] and player_x > 0:
        player_x -= player_speed * deltaTime
    if keys[pygame.K_d] and player_x < 800 - player_width:
        player_x += player_speed * deltaTime

loadBricks()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if not isOver:
        keys = pygame.key.get_pressed()
        checkPlayerInput(keys)

        updateBall()

        player = pygame.Rect(player_x, player_y, player_width, player_height)
        ball = pygame.Rect(ball_x, ball_y, ball_diameter, ball_diameter)

        if player.colliderect(ball):
            ball_velocity[1] *= -1

        updateBricks()
        text = font.render(f"Score: {player_score}",True,white,(0,0,0))
        drawEntities()

        checkVictory()
        
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            restartGame()

        if len(bricks) == 0:
            textOver = font2.render("YOU WON", True, (255,0,0),(128,128,128))

        prozor.fill("grey")
        prozor.blit(textOver,textOverPos)
        prozor.blit(textRestart,textRestartPos)

        pygame.display.flip()
        pygame.display.update()
    
    deltaTime = clock.tick(60) / 1000