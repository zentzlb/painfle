import pygame
from painfle import engine


def findall(string: str, substring: str):
    """
    find index(s) of substring in string
    :param string: string to search
    :param substring: character to search for
    :return: indices of substring
    """
    find_list = [i for i in range(len(string)) if string[i] == substring]

    return find_list


def remove(g: str, ms: str, w: str):
    """
    removes redundant yellow letters from response
    :param g: guessed word
    :param ms: response
    :param w: actual word
    :return:
    """
    for i in range(len(ms)):
        if ms[i] == 'Y' and g.count(g[i]) > w.count(g[i]):  # letter appears more in the guess than the word
            num = w.count(g[i])  # number of times the letter appears in the word
            ind_list = findall(g, g[i])
            for j in ind_list:
                if ms[j] == 'G':
                    num -= 1
            for j in ind_list:
                if ms[j] == 'Y' and num == 0:
                    ms = ms[:j] + '-' + ms[j+1:]
                elif ms[j] == 'Y':
                    num -= 1
    return ms


def checker(guess: str, answer: str):
    """
    gives a response to a guess
    :param guess: guessed word
    :param answer: actual word
    :return: string of G, Y, and -
    """
    MyString = ''
    for i in range(len(guess)):
        if i < len(answer) and guess[i] == answer[i]:
            MyString += 'G'
        elif answer.find(guess[i]) != -1:  # add clause for multiple of same letter
            MyString += 'Y'
        else:
            MyString += '-'
    MyString = remove(guess, MyString, answer)
    return MyString


class engine:
    def __init__(self):
        file1 = open('words.txt', 'r')
        file2 = open('curated.txt', 'r')
        self.full_words = set(file1.read().split('\n'))
        self.used_words = file2.read().split('\n')
        self.text = ''
        self.n = 0
        self.max_guesses = 6
        self.word_len = 5
        self.guesses = []
        self.responses = []
        self.letters = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']
        self.colors = {}
        self.counter = 0


    def reset(self):
        file2 = open('curated.txt', 'r')
        self.used_words = file2.read().split('\n')
        self.text = ''
        self.n = 0
        self.guesses = []
        self.responses = []
        self.colors = {}
        self.counter = 0

    def update(self, guess: str, response: str):
        self.used_words = [word for word in self.used_words if checker(guess, word) == response]

    def tic(self):
        if self.counter > 0:
            self.counter -= 1

    def respond(self):
        d = {}
        for word in self.used_words:
            r = checker(self.text, word)
            if r in d:
                d[r].append(word)
            else:
                d[r] = [word]
            # print(d.values())
        for key in d.keys():
            print(f'{key}: {len(d[key])}')

        self.used_words = max(d.values(), key=len)
        response = checker(self.text, self.used_words[0])
        for i in range(len(response)):
            if self.text[i] not in self.colors or response[i] < self.colors[self.text[i]]:
                self.colors[self.text[i]] = response[i]

        self.n += 1
        self.responses.append(response)
        self.guesses.append(self.text)
        self.text = ''


def main():

    pygame.font.init()

    FPS = 60
    run = True
    clock = pygame.time.Clock()
    WIDTH, HEIGHT = 800, 800
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    FONT = pygame.font.SysFont('Agency FB', 40)
    TITLE = pygame.font.SysFont('Agency FB', 60)
    SUBTITLE = pygame.font.SysFont('Agency FB', 20)
    pygame.display.set_caption('PAINFLE')

    e = engine()

    while run:
        clock.tick(FPS)
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
                        print(e.used_words)
                    else:
                        e.counter = FPS
                elif event.unicode.isprintable() and len(e.text) < e.word_len:
                    e.text += event.unicode.lower()

        draw_window(WIN, WIDTH, HEIGHT, FONT, TITLE, SUBTITLE, e)


def draw_window(win, width, height, font, title, subtitle, e):
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    PURPLE = (255, 0, 255)
    WHITE = (255, 255, 255)
    GRAY = (100, 100, 100)
    win.fill(WHITE)

    rx = 50
    ry = 50
    sep = 10
    wrec = 3
    color_dict = {'G': GREEN, 'Y': YELLOW, '-': GRAY}
    width2 = e.word_len * (rx + sep)
    height2 = e.max_guesses * (ry + sep)

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
            text_surface = subtitle.render(f'Better luck next time! The word was "{e.used_words[0]}," press esc to play again.', True, BLACK)
            xt = width / 2 - text_surface.get_width() / 2
            yt = 80
            win.blit(text_surface, (xt, yt))

    for w in range(e.max_guesses):
        for c in range(e.word_len):

            x = width2 * c / e.word_len + (width - width2) / 2
            y = height2 * w / e.max_guesses + (height - height2) / 2

            if w < len(e.guesses):
                color = color_dict[e.responses[w][c]]
                pygame.draw.rect(win, color, (x, y, rx, ry))
                pygame.draw.rect(win, BLACK, (x, y, rx, ry), width=wrec)
                text_surface = font.render(e.guesses[w][c].upper(), True, BLACK)
                xt = x + rx / 2 - text_surface.get_width() / 2
                yt = y + ry / 2 - text_surface.get_height() / 2
                win.blit(text_surface, (xt, yt))
            elif w == len(e.guesses) and c < len(e.text):
                if e.counter > 0:
                    dx = 5 * ((e.counter // 5) % 2 - 0.5)
                else:
                    dx = 0
                pygame.draw.rect(win, BLACK, (x+dx, y, rx, ry), width=wrec)
                text_surface = font.render(e.text[c].upper(), True, BLACK)
                xt = x + rx / 2 - text_surface.get_width() / 2 + dx
                yt = y + ry / 2 - text_surface.get_height() / 2
                win.blit(text_surface, (xt, yt))
            else:
                pygame.draw.rect(win, BLACK, (x, y, rx, ry), width=wrec)


    height2 = len(e.letters) * (ry + sep)
    for i in range(len(e.letters)):
        line = e.letters[i]
        width2 = len(line) * (rx + sep)
        for j in range(len(line)):
            c = line[j]
            x = width2 * j / len(line) + (width - width2) / 2
            y = height2 * i / len(e.letters) + (height - height2) / 2 + 300
            if c in e.colors:
                color = color_dict[e.colors[c]]
                pygame.draw.rect(win, color, (x, y, rx, ry))
            pygame.draw.rect(win, BLACK, (x, y, rx, ry), width=wrec)
            text_surface = font.render(c.upper(), True, BLACK)
            xt = x + rx / 2 - text_surface.get_width() / 2
            yt = y + ry / 2 - text_surface.get_height() / 2
            win.blit(text_surface, (xt, yt))


    pygame.display.update()


if __name__ == '__main__':
    main()
    pygame.quit()

