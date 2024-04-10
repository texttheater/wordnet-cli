#!/usr/bin/env python3


"""Simple CLI for looking up word senses in WordNet."""


import sys


import nltk
from nltk.corpus import wordnet31


POS = ('n', 'v', 'a', 'r', 's')
POS_MAP = {
    'n': wordnet31.NOUN,
    'v': wordnet31.VERB,
    'a': wordnet31.ADJ,
    'r': wordnet31.ADV,
    's': wordnet31.ADJ_SAT,
}


def noncanonical_name(lemma, pos):
    synsets = wordnet31.synsets(lemma.name(), pos=pos)
    for i, s in enumerate(synsets, start=1):
        if s == lemma.synset():
            return f'{lemma.name()}.v.{i:02}'


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('USAGE: python3 wn.py LEMMA', file=sys.stderr)
        sys.exit(1)
    query = '_'.join(sys.argv[1:])
    try:
        synsets = wordnet31.synsets(query)
    except LookupError:
        nltk.download('wordnet')
        nltk.download('wordnet31')
        synsets = wordnet31.synsets(query)
    for synset in synsets:
        lemmas = synset.lemmas()
        names = [noncanonical_name(l, synset.pos()) for l in lemmas]
        title = ' '.join(names)
        print(title)
        print(synset.definition())
        for example in synset.examples():
            print(f"'{example}'")
        print()
