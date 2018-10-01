#! /anaconda3/envs/maga/bin/python
# это файл для порождения форм-кандидатов и чека их через майстем
from pymystem3 import Mystem
from itertools import chain
import fileinput
import re


def concat(*args):
    """reversed('th'), 'e' => 'hte'"""
    try:
        return ''.join(args)
    except TypeError:
        return ''.join(chain.from_iterable(args))


ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
CLOSEST = {
'а': 'оя',
'б': 'пью',
'в': 'ыа',
'г': 'кнш',
'д': 'тлж',
'е': 'ёиокн',
'ё': 'ео',
'ж': 'дэ',
'з': 'сщх',
'и': 'емт',
'й': 'яц',
'к': 'уе',
'л': 'од',
'м': 'си',
'н': 'ег',
'о': 'апр',
'п': 'ар',
'р': 'по',
'с': 'зчмщ',
'т': 'иьд',
'у': 'цк',
'ф': 'ы',
'х': 'зъ',
'ц': 'йу',
'ч': 'яс',
'ш': 'гщ',
'щ': 'шз',
'ъ': 'х',
'ы': 'иофв',
'ь': 'тб',
'э': 'же',
'ю': 'б',
'я': 'ач',
}
COMPLEX = {
'ё': ('йо'),
'щ': ('сч')
}


class Word(object):
    """container for word-based methods"""

    def __init__(self, word, corrections=[]):
        """
        Generate slices to assist with typo
        definitions.
        'the' => (('', 'the'), ('t', 'he'),
                  ('th', 'e'), ('the', ''))
        """
        word_ = word.lower()
        slice_range = range(len(word_) + 1)
        self.slices = tuple((word_[:i], word_[i:])
                            for i in slice_range)
        self.word = word
        self.corrections = corrections

    def _deletes(self):
        """th"""
        return {concat(a, b[1:]): [*self.corrections, 'del:{}'.format(b[0])]
                for a, b in self.slices[:-1]}

    def _transposes(self):
        """teh"""
        return {concat(a, reversed(b[:2]), b[2:]): [*self.corrections, 'trans:{},{}'.format(b[0], b[1])]
                for a, b in self.slices[:-2]}

    def _replaces(self):
        """tge"""
        return {concat(a, c, b[1:]): [*self.corrections, 'repl:{},{}'.format(c, b[0])]
                for a, b in self.slices[:-1]
                for c in ALPHABET}

    def _inserts(self):
        """thwe"""
        return {concat(a, c, b): [*self.corrections, 'insert:{}'.format(c)]
                for a, b in self.slices
                for c in ALPHABET}

    def _half_replaces(self):
        return {**{concat(a, c, b[1:]): [*self.corrections, 'repl:{},{}'.format(c, b[0])]
                for a, b in self.slices[:-1]
                for c in set(CLOSEST[b[0]])|{COMPLEX.get(b[0], b[0])}-{b[0]}},
                **{self.word.replace('сч', 'щ'): 'repl:щ,сч'}} #- {self.word: None}

    def _half_deletes(self):
        # print([(a, b[1:]) for a, b in self.slices[:-1]])
        return {concat(a, b[1:]): [*self.corrections, 'del:{}'.format(b[0])]
                for a, b in self.slices[:-1] if b[0]=='е'}

    def typos(self):
        """letter combinations one typo away from word"""
        return ({**self._deletes(), **self._transposes(),
                **self._replaces(), **self._inserts(), **self._half_replaces(),
                **{e2: cor for e1, corr in self._half_replaces().items() for e2, cor in Word(e1, corr)._half_replaces().items()}})

    def one_and_a_half_typos(self):
        """letter combinations two typos away from word"""
        return {e2: cor for e1, corr in self._half_replaces().items()
                for e2, cor in Word(e1, corr).typos().items()}

    def double_typos(self):
        """letter combinations two typos away from word"""
        return {e2: cor for e1, corr in self.typos().items()
                for e2, cor in Word(e1, corr).typos().items()}


def check(cand):
    '''checks if a candidate is a known word using mystem'''
    ch = m.analyze(cand)
    if ch:
        analysis = m.analyze(cand)[0]['analysis']
        if len(analysis) > 0 and not 'qual' in analysis[0] and not ',кр,' in analysis[0]['gr']:
            return analysis[0]['lex']
    return None


def known(words):
    """{'Gazpacho', 'gazzpacho'} => {'gazpacho'}"""
    res = {check(w): words[w] for w in words} #- {None}
    if None in res:
        del res[None]
    return res
    # return {w.lower() for w in words} & KNOWN_WORDS


def spell(word):
    """most likely correction for everything up to a double typo"""
    w = Word(word)
    candidates = (#common([word]) or exact([word]) or
                  known({word: None}) or known(w._half_replaces()) or
                  known(w._half_deletes()) or
                  known(w.typos()) or known(w.one_and_a_half_typos()) or
                  known(w.double_typos()) or
                  {word: None})
    # print(candidates)
    return candidates


def fix_repetition(word):
    word=word.lower()
    word=re.sub(r'(.)\1{2,}', r'\1', word)
    return word


m = Mystem()
# spell('превед')
# spell('женсчина')
# spell('пионэр')
# spell('песом')
# spell('гребаный')
# spell('раён')
# spell('серф')

for line in fileinput.input():
    wd = line.strip()
    res = spell(fix_repetition(wd))
    print(wd, '\t', list(res.keys()), '\t', list(res.values()))
