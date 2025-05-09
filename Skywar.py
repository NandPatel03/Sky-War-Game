import pygame
import os
pygame.font.init()
pygame.mixer.init() #this function adds music to bullets and hitdetections

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SKY WAR GAME!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 3
SKYWAR_WIDTH, SKYWAR_HEIGHT = 55, 40

BLUE_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BLUE_SKYWAR_IMAGE = pygame.image.load(
    os.path.join('Supportfiles', 'skywar_blue.png'))
BLUE_SKYWAR = pygame.transform.rotate(pygame.transform.scale(
    BLUE_SKYWAR_IMAGE, (SKYWAR_WIDTH, SKYWAR_HEIGHT)), 270)

RED_SKYWAR_IMAGE = pygame.image.load(
    os.path.join('Supportfiles', 'skywar_red.png'))
RED_SKYWAR = pygame.transform.rotate(pygame.transform.scale(
    RED_SKYWAR_IMAGE, (SKYWAR_WIDTH, SKYWAR_HEIGHT)), 90)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Supportfiles', 'skywar.png')), (WIDTH, HEIGHT))


def draw_window(red, blue, red_bullets, blue_bullets, red_health, blue_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLUE, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health Count: " + str(red_health), 1, WHITE)
    blue_health_text = HEALTH_FONT.render(
        "Health Count: " + str(blue_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 13, 13))
    WIN.blit(blue_health_text, (13, 13))

    WIN.blit(BLUE_SKYWAR, (blue.x, blue.y))
    WIN.blit(RED_SKYWAR, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in blue_bullets:
        pygame.draw.rect(WIN, BLUE, bullet)

    pygame.display.update()


def blues_controles(keys_pressed, blue):
    if keys_pressed[pygame.K_a] and blue.x - VEL > 0:  # A Button moves the jet Left
        blue.x -= VEL
    if keys_pressed[pygame.K_d] and blue.x + VEL + blue.width < BORDER.x:  # D Button moves the jet Right
        blue.x += VEL
    if keys_pressed[pygame.K_w] and blue.y - VEL > 0:  # W Button moves the jet Up
        blue.y -= VEL
    if keys_pressed[pygame.K_s] and blue.y + VEL + blue.height < HEIGHT - 15:  # S Button moves the jet Down
        blue.y += VEL


def reds_controles(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # left Arrow moves the jet Left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # right Arrow moves the jet Right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # up Arrow moves the jet Up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # down Arrow moves the jet Down
        red.y += VEL


def bullets_for_jets(blue_bullets, red_bullets, blue, red):
    for bullet in blue_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            blue_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def winning_logic(text): # Whichever jet come to 0 health, they lose the game. 
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, SKYWAR_WIDTH, SKYWAR_HEIGHT)
    blue = pygame.Rect(100, 300, SKYWAR_WIDTH, SKYWAR_HEIGHT)

    red_bullets = []
    blue_bullets = []

    red_health = 13
    blue_health = 13

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(blue_bullets) < MAX_BULLETS:# Shoots Bullets for Blue
                    bullet = pygame.Rect(
                        blue.x + blue.width, blue.y + blue.height//2 - 2, 10, 5)
                    blue_bullets.append(bullet)
                    

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS: # Shoots Bullets for Red 
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    

            if event.type == RED_HIT:
                red_health -= 1
                

            if event.type == BLUE_HIT:
                blue_health -= 1
                

        winner_text = ""     # Will display message to whichever team that wins.
        if red_health <= 0:
            winner_text = "Blue Wins!"

        if blue_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            winning_logic(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        blues_controles(keys_pressed, blue)
        reds_controles(keys_pressed, red)

        bullets_for_jets(blue_bullets, red_bullets, blue, red)

        draw_window(red, blue, red_bullets, blue_bullets,
                    red_health, blue_health)
