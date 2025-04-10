import pygame
import random as rnd
import numpy as np
import math
from painfle import Engine

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

RX = 50
RY = 50
SEP = 10
REC_WIDTH = 3
COLORS = {'G': GREEN, 'Y': YELLOW, '-': GRAY}


def main():
    pygame.font.init()

    fps = 60
    run = True
    clock = pygame.time.Clock()
    width, height = 800, 800
    win = pygame.display.set_mode((width, height))
    font = pygame.font.SysFont('Agency FB', 40)
    title = pygame.font.SysFont('Agency FB', 60)
    subtitle = pygame.font.SysFont('Agency FB', 20)
    pygame.display.set_caption('PAINFLE')

    e = Engine()

    while run:
        clock.tick(fps)
        e.tic()
        # fps = clock.get_fps()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quit if user quits
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    e.reset()
                elif event.key == pygame.K_BACKSPACE:
                    e.text = e.text[:-1]
                elif event.key == pygame.K_RETURN and len(e.text) == e.word_len:
                    if e.text in e.full_words and e.text not in e.guesses:
                        e.respond()
                    else:
                        e.counter = fps
                elif event.key == pygame.K_PRINT:
                    print(e.used_words)
                elif event.unicode.isprintable() and len(e.text) < e.word_len:
                    e.text += event.unicode.lower()

        draw_window(win, width, height, font, title, subtitle, e)


def draw_window(win, width, height, font, title, subtitle, e):
    win.fill(WHITE)
    width2 = e.word_len * (RX + SEP)
    height2 = e.max_guesses * (RY + SEP)

    text_surface = title.render('PAINFLE', True, BLACK)
    xt = width / 2 - text_surface.get_width() / 2
    yt = 10
    win.blit(text_surface, (xt, yt))

    if len(e.responses) > 1 and e.responses[-1] == 'GGGGG':
        text_surface = subtitle.render('press esc to play again', True, BLACK)
        xt = width / 2 - text_surface.get_width() / 2
        yt = 80
        win.blit(text_surface, (xt, yt))
    elif len(e.responses) == 6:
        text_surface = subtitle.render(f'Better luck next time! The word was "{e.used_words[0]}," '
                                       f'press esc to play again', True, BLACK)
        xt = width / 2 - text_surface.get_width() / 2
        yt = 80
        win.blit(text_surface, (xt, yt))

    for w in range(e.max_guesses):
        for c in range(e.word_len):
            x = width2 * c / e.word_len + (width - width2) / 2
            y = height2 * w / e.max_guesses + (height - height2) / 2

            if w < len(e.guesses):
                color = COLORS[e.responses[w][c]]
                pygame.draw.rect(win, color, (x, y, RX, RY))
                pygame.draw.rect(win, BLACK, (x, y, RX, RY), width=REC_WIDTH)
                text_surface = font.render(e.guesses[w][c].upper(), True, BLACK)
                xt = x + RX / 2 - text_surface.get_width() / 2
                yt = y + RY / 2 - text_surface.get_height() / 2
                win.blit(text_surface, (xt, yt))
            elif w == len(e.guesses) and c < len(e.text):
                if e.counter > 0:
                    dx = 5 * ((e.counter // 5) % 2 - 0.5)
                else:
                    dx = 0
                pygame.draw.rect(win, BLACK, (x + dx, y, RX, RY), width=REC_WIDTH)
                text_surface = font.render(e.text[c].upper(), True, BLACK)
                xt = x + RX / 2 - text_surface.get_width() / 2 + dx
                yt = y + RY / 2 - text_surface.get_height() / 2
                win.blit(text_surface, (xt, yt))
            else:
                pygame.draw.rect(win, BLACK, (x, y, RX, RY), width=REC_WIDTH)

    height2 = len(e.letters) * (RY + SEP)
    for i in range(len(e.letters)):
        line = e.letters[i]
        width2 = len(line) * (RX + SEP)
        for j in range(len(line)):
            c = line[j]
            x = width2 * j / len(line) + (width - width2) / 2
            y = height2 * i / len(e.letters) + (height - height2) / 2 + 300
            if c in e.colors:
                color = COLORS[e.colors[c]]
                pygame.draw.rect(win, color, (x, y, RX, RY))
            pygame.draw.rect(win, BLACK, (x, y, RX, RY), width=REC_WIDTH)
            text_surface = font.render(c.upper(), True, BLACK)
            xt = x + RX / 2 - text_surface.get_width() / 2
            yt = y + RY / 2 - text_surface.get_height() / 2
            win.blit(text_surface, (xt, yt))

    pygame.display.update()


if __name__ == '__main__':
    main()
    pygame.quit()
