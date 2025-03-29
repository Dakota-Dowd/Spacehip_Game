# Pygame in 90 Minutes - For Beginners (Tech With Tim)
# https://youtu.be/jO6qQDNa2UY?si=PkVhwQ9Z3J-6QK7J
# Time: 1:23:55

import pygame
import os
pygame.font.init()
pygame.mixer.init()

# Inititalizing Variables
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# Middle border, x/y/width/height
BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)


# Sounds
BULLET_HIT_SOUND = pygame.mixer.Sound("Assets/Grenade+1.mp3")
BULLET_FIRE_SOUND = pygame.mixer.Sound("Assets/Gun+Silencer.mp3")

HEALTH_FONT = pygame.font.SysFont("comicsnas", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# Create new event (Plus 1 & 2 just make it a unique ID)
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# IMAGES
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

# This function provides the color for the screen
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
        # Applying the Space image as background
        WIN.blit(SPACE, (0,0))
        pygame.draw.rect(WIN, BLACK, BORDER)
        
        # This displays the health
        # I don't remember what the "1" does in this statement
        red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
        yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
        WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
        WIN.blit(yellow_health_text, (10,10))

        # Use blit when you want to load a surface (image/text) on the screen
        WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
        WIN.blit(RED_SPACESHIP, (red.x, red.y))



        for bullet in red_bullets:
            pygame.draw.rect(WIN, RED, bullet)
        
        for bullet in yellow_bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)

        pygame.display.update()

# Handles movement for the yellow Spaceship
def handle_yellow_movement(keys_pressed, yellow):
        # The sections after "and" are the border control (and I don't know why VEL is important there)
        if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
            yellow.x -= VEL
        if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # RIGHT
            yellow.x += VEL
        # When you move up, you subtract from y becuase you are moving relative to the top left corner of the screen, which is y = 0
        if keys_pressed[pygame.K_w] and yellow.y - VEL > 0 : # UP
            yellow.y -= VEL
        if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 13: # DOWN
            yellow.y += VEL


# Handles movement for the red spaceship
def handle_red_movement(keys_pressed, red):
        if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # LEFT
            red.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # RIGHT
            red.x += VEL
        # When you move up, you subtract from y becuase you are moving relative to the top left corner of the screen, which is y = 0
        if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # UP
            red.y -= VEL
        if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 13: # DOWN
            red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    # Yellow Bullet Behavior
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        # colliderect() checks if two rectangles collide
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    # Red Bullet Behavior
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        # colliderect() checks if two rectangles collide
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()))
    pygame.display.update()
    pygame.time.delay(5000)
    

# This function runs the screen
def main():
    # Creating rectangles that allow us to move the spaceships
    # Rectangles: x, y, width, height
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # Activating Bullets with keys
                # Yellow Bullet
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                # Red Bullet
                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()


            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break 


        # This registeres when a key is being pressed
        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # Something to do with FPS
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)


    main()

# Don't worry about what this is
if __name__ == "__main__":
    main()




