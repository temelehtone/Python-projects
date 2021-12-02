import pygame
import random

pygame.font.init()

FPS = 30
WIDTH = 900
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matopeli")

VEL = 7

GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

BOTTOM_BORDER = pygame.Rect(0, HEIGHT - 30, WIDTH, HEIGHT - 30)
RIGHT_BORDER = pygame.Rect(WIDTH - 30, 0, 30, HEIGHT)
LEFT_BORDER = pygame.Rect(0, 0, 30, HEIGHT)
UP_BORDER = pygame.Rect(0, 0, WIDTH, 30)

END_FONT = pygame.font.SysFont('comicsans', 100)
SCORE_FONT = pygame.font.SysFont('comicsans', 30)
APPLE_EATEN = pygame.USEREVENT + 1
ADD_SNAKE = pygame.USEREVENT + 2


def draw_window(mato, apple, score, snake_body, move):
    WIN.fill(LIGHT_GREEN)
    score_text = SCORE_FONT.render("Score: " + str(score), True, WHITE)
    WIN.blit(score_text, (30, 30))
    pygame.draw.rect(WIN, RED, apple)

    pygame.draw.rect(WIN, GREEN, BOTTOM_BORDER)
    pygame.draw.rect(WIN, GREEN, RIGHT_BORDER)
    pygame.draw.rect(WIN, GREEN, LEFT_BORDER)
    pygame.draw.rect(WIN, GREEN, UP_BORDER)
    pygame.draw.rect(WIN, BLUE, mato)
    draw_body(snake_body, move, mato)

    pygame.display.update()


def end(end_text, score):
    draw_text = END_FONT.render(end_text, True, RED)
    end_score_text = SCORE_FONT.render("Your score: " + str(score), True, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height()))
    WIN.blit(end_score_text, (WIDTH / 2 - end_score_text.get_width() / 2, HEIGHT / 2 + end_score_text.get_height() - 10))
    pygame.display.update()
    pygame.time.delay(5000)


def eat_apple(apple, mato):
    if apple.colliderect(mato):
        pygame.event.post(pygame.event.Event(APPLE_EATEN))


def draw_body(snake_body, move, mato):
    if len(snake_body) != 0:
        snake_body[0].x, snake_body[0].y = mato.x, mato.y
        pygame.draw.rect(WIN, WHITE, snake_body[0])
        for body in snake_body[1:]:
            body.x, body.y = snake_body[snake_body.index(body) - 1].x, snake_body[snake_body.index(body) - 1].y
            pygame.draw.rect(WIN, WHITE, body)


def add_body(snake_body, mato, move):

    if len(snake_body) == 0:
        if move[0] == -VEL:
            snake_body.append(pygame.Rect(mato.x + 42, mato.y, 40, 40))
        elif move[0] == VEL:
            snake_body.append(pygame.Rect(mato.x - 42, mato.y, 40, 40))
        elif move[1] == -VEL:
            snake_body.append(pygame.Rect(mato.x, mato.y + 42, 40, 40))
        elif move[1] == VEL:
            snake_body.append(pygame.Rect(mato.x, mato.y - 42, 40, 40))
    else:
        if move[0] == -VEL:
            snake_body.append(pygame.Rect(snake_body[-1].x + 42, snake_body[-1].y, 40, 40))
        elif move[0] == VEL:
            snake_body.append(pygame.Rect(snake_body[-1].x - 42, snake_body[-1].y, 40, 40))
        elif move[1] == -VEL:
            snake_body.append(pygame.Rect(snake_body[-1].x, snake_body[-1].y + 42, 40, 40))
        elif move[1] == VEL:
            snake_body.append(pygame.Rect(snake_body[-1].x, snake_body[-1].y - 42, 40, 40))

    return snake_body


def main():

    mato = pygame.Rect(100, 100, 40, 40)
    apple = pygame.Rect(200, 200, 40, 40)
    move = (0, 0)
    clock = pygame.time.Clock()
    score = 0
    snake_body = []

    run = True
    while run:
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
                apple = pygame.Rect(random.randint(40, WIDTH - 40 - apple.width), random.randint(40, HEIGHT - 40 - apple.height), 40, 40)
                score += 1
                add_body(snake_body, mato, move)

        end_text = ""
        if mato.x < 35 or mato.x > WIDTH - 35 - mato.width:
            end_text = "You lost!"
        if mato.y < 35 or mato.y > HEIGHT - 35 - mato.height:
            end_text = "You lost!"
        for body in snake_body:
            if mato.colliderect(body):
                end_text = ""
        if end_text != "":
            end(end_text, score)
            break
        mato = mato.move(move)
        draw_window(mato, apple, score, snake_body, move)
        eat_apple(apple, mato)

    main()


if __name__ == "__main__":
    main()
