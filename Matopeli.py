import pygame
import random
import time



pygame.font.init()

FPS = 8
WIDTH = 900
HEIGHT = 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matopeli")

VEL = 30

GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BOTTOM_BORDER = pygame.Rect(0, HEIGHT - 30, WIDTH, HEIGHT - 30)
RIGHT_BORDER = pygame.Rect(WIDTH - 30, 0, 30, HEIGHT)
LEFT_BORDER = pygame.Rect(0, 0, 30, HEIGHT)
UP_BORDER = pygame.Rect(0, 0, WIDTH, 30)

END_FONT = pygame.font.SysFont('comicsans', 100)
SCORE_FONT = pygame.font.SysFont('comicsans', 20)

APPLE_EATEN = pygame.USEREVENT + 1


def draw_boxes(boxes):
    for x in range(30, WIDTH - 30, 30):
        for y in range(30, HEIGHT - 30, 30):
            boxes.append((x, y))
            rect = pygame.Rect(x, y, 30, 30)
            pygame.draw.rect(WIN, BLACK, rect, 2)
    return boxes


def draw_window(apple, score, boxes, aika, snake_body):
    WIN.fill(WHITE)
    score_text = SCORE_FONT.render("Score: " + str(score), True, WHITE)
    time_text = SCORE_FONT.render(f"Time: {aika: .0f}", True, WHITE)
    pygame.draw.rect(WIN, RED, apple)
    
    draw_snake(snake_body)
    draw_boxes(boxes)
    
    pygame.draw.rect(WIN, BLACK, BOTTOM_BORDER)
    pygame.draw.rect(WIN, BLACK, RIGHT_BORDER)
    pygame.draw.rect(WIN, BLACK, LEFT_BORDER)
    pygame.draw.rect(WIN, BLACK, UP_BORDER)

    WIN.blit(score_text, (30, 2))
    WIN.blit(time_text, (800, 2))
    
    pygame.display.update()


def end(end_text, score):
    draw_text = END_FONT.render(end_text, True, RED)
    end_score_text = END_FONT.render("Your score: " + str(score), True, BLACK)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height()))
    WIN.blit(end_score_text, (WIDTH / 2 - end_score_text.get_width() / 2, HEIGHT / 2 - 10))
    pygame.display.update()
    pygame.time.delay(1000)


def eat_apple(apple, snake_body):
    for body in snake_body:
        rect = pygame.Rect(body[0], body[1], 30, 30)
        if apple.colliderect(rect):
            pygame.event.post(pygame.event.Event(APPLE_EATEN))


def borders_coord():
    borders = []
    y = 0
    for x in range(0, WIDTH, 30):
        borders.append((x, y))
    x = 0
    for y in range(0, HEIGHT, 30):
        borders.append((x, y))
    return borders


def draw_snake(snake_body):
    for body in snake_body:
        rect = pygame.Rect(body[0], body[1], 30, 30)
        pygame.draw.rect(WIN, BLUE, rect)


def main():

    move = (0, 0)
    clock = pygame.time.Clock()
    score = 0
    boxes = []
    boxes = draw_boxes(boxes)
    boxesX, boxesY = random.choice(boxes)
    
    borders = borders_coord()
    snake_body = []
    length_of_snake = 1
    boxesX, boxesY = random.choice(boxes)
    apple = pygame.Rect(boxesX, boxesY, 30, 30)
    run = True
    start_time = time.time()
    end_text = ""
    x1, y1 = 90, 90

    while run:
        
        aika = time.time() - start_time
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_LEFT:
                    move = (-VEL, 0)

                if event.key == pygame.K_RIGHT:
                    move = (VEL, 0)
                if event.key == pygame.K_UP:
                    move = (0, -VEL)
                if event.key == pygame.K_DOWN:
                    move = (0, VEL)
            if event.type == APPLE_EATEN:
                boxesX, boxesY = random.choice(boxes)
                apple = pygame.Rect(boxesX, boxesY, 30, 30)
                score += 1
                length_of_snake += 1
        
        if x1 >= WIDTH - 30 or x1 < 30 or y1 >= HEIGHT - 30 or y1 < 30:        
            end_text = "You lost!"
        x1 += move[0]
        y1 += move[1]      

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_body.append(snake_head)


        if len(snake_body) > length_of_snake:
            del snake_body[0]
        
        for body in snake_body[:-1]:
            if body == snake_head:
                end_text = "You lost!"
                       
        if end_text != "":
            end(end_text, score)
            break
        
        draw_window(apple, score, boxes, aika, snake_body)
        eat_apple(apple, snake_body)
        
    main()


if __name__ == "__main__":
    main()
