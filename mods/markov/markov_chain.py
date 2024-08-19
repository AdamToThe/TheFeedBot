import markovify
from markovchain.text import MarkovText

from os import path, getcwd

import re

cwd = path.join('mods', 'markov')


class Markov:

    def __init__(self):
        self.other_mark = MarkovText()
        self.read_from_txt('other_mark.txt')
        self.data_type = markovify.NewlineText
        self.mark = self.data_type(self.data('messages.txt'))

    def data(self, name: str):
        with open(path.join(cwd, 'data', name)) as fp:
            return fp.read()

    def __call__(self, *a, **kw):
        return self.mark.make_sentence(tries=30, *a, **kw)

    def other(self, *a, **kw):
        return self.other_mark(*a, **kw)

    def clean_txt(self, name: str, new: str):
        f = open(path.join(cwd, 'data', name), 'r')
        with open(path.join(cwd, 'data', new), 'w') as fp:
            d = f.read()
            clean = re.sub(r'http\S+', '', d)
            clean = re.sub(r'<@.*>', '', clean)
            fp.write(clean)

    def read_from_txt(self, n: str):
        with open(path.join(cwd, 'data', n)) as fp:
            for n in fp:
                self.other_mark.data(n, part=True)

    def learn(self, txt, *a, **k):
        clean = txt  #re.sub(r'http\S+', '', txt)
        #self.data(clean, part=False, *a, **k)
        self.mark = markovify.combine([self.mark, self.data_type(clean)])
        self.write_to('messages.txt', clean)

    def write_to(self, name: str, text: str):
        with open(path.join(cwd, 'data', name), 'a+') as fp:
            fp.write(text)
            fp.write('\n')
