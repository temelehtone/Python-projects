import pygame
import os
import random
pygame.font.init()

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy bird")

FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BIRD_HIT = pygame.USEREVENT + 1

END_FONT = pygame.font.SysFont('comicsans', 100)
SCORE_FONT = pygame.font.SysFont('comicsans', 30)

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Flappy_bird', 'Flappy_bird.png')), (WIDTH, HEIGHT))
FLAPPY_PHOTO = pygame.transform.scale(pygame.image.load(os.path.join('Flappy_bird', 'flappy.png')), (80, 70))
DOWN_PIPE_IMAGE = pygame.image.load(os.path.join('Flappy_bird', 'pipe.png'))
DOWN_PIPE = pygame.transform.scale(DOWN_PIPE_IMAGE, (200, 400))
UP_PIPE = pygame.transform.rotate(pygame.transform.scale(DOWN_PIPE_IMAGE, (200, 400)), 180)


def window(bird, up_pipe, down_pipe, down_pipe1, up_pipe1, up_pipe2, down_pipe2, score):
    WIN.blit(BACKGROUND, (0, 0))
    score_text = SCORE_FONT.render("Score: " + str(score), True, BLACK)

    WIN.blit(FLAPPY_PHOTO, (bird.x, bird.y))
    WIN.blit(DOWN_PIPE, (down_pipe.x, down_pipe.y))
    WIN.blit(UP_PIPE, (up_pipe.x, up_pipe.y))
    WIN.blit(DOWN_PIPE, (down_pipe1.x, down_pipe1.y))
    WIN.blit(UP_PIPE, (up_pipe1.x, up_pipe1.y))
    WIN.blit(DOWN_PIPE, (down_pipe2.x, down_pipe2.y))
    WIN.blit(UP_PIPE, (up_pipe2.x, up_pipe2.y))
    WIN.blit(score_text, (30, 30))
    pygame.display.update()


def pipe_move(alaputki, ylaputki, alaputki1, ylaputki1, ylaputki2, alaputki2, bird):
    ylaputki.x -= 15
    alaputki.x -= 15
    ylaputki1.x -= 15
    alaputki1.x -= 15
    ylaputki2.x -= 15
    alaputki2.x -= 15
    bird.y += 7


def osuma(bird, up_pipe, up_pipe1, up_pipe2, down_pipe, down_pipe1, down_pipe2):

    if bird.colliderect(up_pipe) or bird.colliderect(up_pipe1) or bird.colliderect(up_pipe2) or\
        bird.colliderect(down_pipe) or bird.colliderect(down_pipe1) or bird.colliderect(down_pipe2) or\
            bird.y < 0 or bird.y > HEIGHT - bird.height:
        pygame.event.post(pygame.event.Event(BIRD_HIT))


def end(score):
    end_text = END_FONT.render("Game over!", True, BLACK)
    score_text = END_FONT.render("Your score: " + str(score), True, BLACK)
    WIN.blit(score_text, (WIDTH / 2 - score_text.get_width()/2, HEIGHT / 2))
    WIN.blit(end_text, (WIDTH / 2 - end_text.get_width() / 2, HEIGHT / 2 - end_text.get_height() - 50))
    pygame.display.update()
    pygame.time.delay(4000)


def main():
    bird = pygame.Rect(300, 400, 80, 70)
    down_pipe = pygame.Rect(WIDTH + 200, HEIGHT - random.randint(200, 400), 200, 400)
    down_pipe1 = pygame.Rect(WIDTH + 800, HEIGHT - random.randint(200, 400), 200, 400)
    down_pipe2 = pygame.Rect(WIDTH + 1400, HEIGHT - random.randint(200, 400), 200, 400)
    score = 0
    up_pipe = pygame.Rect(WIDTH + 200, down_pipe.y - 700, 200, 400)
    up_pipe1 = pygame.Rect(WIDTH + 800, down_pipe1.y - 700, 200, 400)
    up_pipe2 = pygame.Rect(WIDTH + 1400, down_pipe2.y - 700, 200, 400)

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.y -= 150


            if event.type == BIRD_HIT:
                end(score)
                main()

        if up_pipe.x < -200:
            down_pipe = pygame.Rect(WIDTH + 400, HEIGHT - random.randint(200, 400), 200, 400)
            up_pipe = pygame.Rect(WIDTH + 400, down_pipe.y - 700, 200, 400)
        if up_pipe1.x < -200 and down_pipe1.x < - 200:
            down_pipe1 = pygame.Rect(WIDTH + 400, HEIGHT - random.randint(200, 400), 200, 400)
            up_pipe1 = pygame.Rect(WIDTH + 400, down_pipe1.y - 700, 200, 400)
        if up_pipe2.x < -200 and down_pipe2.x < -200:
            down_pipe2 = pygame.Rect(WIDTH + 400, HEIGHT - random.randint(200, 400), 200, 400)
            up_pipe2 = pygame.Rect(WIDTH + 400, down_pipe2.y - 700, 200, 400)
        if bird.x == up_pipe.x + 100 or bird.x == up_pipe2.x + 100 or bird.x == up_pipe1.x + 100:
            score += 1

        osuma(bird, up_pipe, up_pipe1, up_pipe2, down_pipe, down_pipe1, down_pipe2)
        window(bird, up_pipe, down_pipe, down_pipe1, up_pipe1, up_pipe2, down_pipe2, score)
        pipe_move(down_pipe, up_pipe, down_pipe1, up_pipe1, up_pipe2, down_pipe2, bird)

    main()

if __name__ == "__main__":
    main()