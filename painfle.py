from functions import *


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

