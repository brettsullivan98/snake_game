import pygame
import time
import random
import sys

#difficulty settings
# easy aka youre trash -> 10
# medium aka youre a noob -> 25
# hard aka youre ok -> 50
# harder aka youre a pro-> 75
# impossible aka youre a god -> 100

difficulty = 25

frame_size_x = 720
frame_size_y = 480


#check for pygame errors
check_errors = pygame.init()
if check_errors[1] > 0:
    print("(!) Had {0} initializing errors, exiting...".format(check_errors[1]))
    sys.exit(-1)
else:
    print("(+) PyGame successfully initialized!")

#intialize pygame window
pygame.display.set_caption("Snake Game")
screen = pygame.display.set_mode((frame_size_x, frame_size_y))

#colors (R, G, B) pygame.color
white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)


#fps controller
fps_controller = pygame.time.Clock()


#game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

#food variables
food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

direction = "right"
change_to = direction

score = 0


#game over
def game_over():
    my_font = pygame.font.SysFont("monaco", 72)
    game_over_surface = my_font.render("Game Over", True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/2)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(5)
    pygame.quit()
    sys.exit()
    

#score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render("Score: " + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/2, 10)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y-10)
    screen.blit(score_surface, score_rect)
    pygame.display.flip()

#snake logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = "up"
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = "down"
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = "left"
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = "right"
            
#make sure snake cannot move opposite direction instantly
    if change_to == "right" and not direction == "left":
        direction = change_to
    if change_to == "left" and not direction == "right":
        direction = change_to
    elif change_to == "up" and not direction == "down":
        direction = change_to
    elif change_to == "down" and not direction == "up":
        direction = change_to

    #snake movement
    if direction == "right":
        snake_pos[0] += 10
    if direction == "left":
        snake_pos[0] -= 10
    if direction == "up":
        snake_pos[1] -= 10
    if direction == "down":
        snake_pos[1] += 10

    #snake growing
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        food_spawn = False
        score += 1
    else:
        snake_body.pop()

    #spawn food
    if not food_spawn:
        food_pos = [random.randrange(1, frame_size_x-1), random.randrange(1, frame_size_y-1)]
    food_spawn = True

    #gfx
    screen.fill(black)
    for pos in snake_body:
        pygame.draw.rect(screen, white, pygame.Rect(pos[0], pos[1], 10, 10))

    #snake food
    pygame.draw.rect(screen, green, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    #game over conditons
    #getting out of bounds
    if snake_pos[0] > frame_size_x or snake_pos[0] < 0:
        game_over()
    if snake_pos[1] > frame_size_y or snake_pos[1] < 0:
        game_over()
    #getting into body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()



    show_score(1, white, "monaco", 72)
    pygame.display.update()
    fps_controller.tick(difficulty)


