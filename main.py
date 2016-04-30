# Enable importing modules from graph-problems folder
import sys
import os
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, current_dir + '/graph-problems')

from wordgrid import WordSearchGrid
from bitset import iterate, subtract

grid = WordSearchGrid.from_string(
"""
eiit
rhst
ecen
atcs
"""
)

from plot import plot

plot(grid, vertex_names=grid.vertices_to_letters)


def recurse(word: str, graph: WordSearchGrid, last_vertex, forbidden):
    if not word:
        return True

    letter = word[0]

    if letter not in graph.letters_to_vertices:
        return False

    candidates = subtract(graph.letters_to_vertices[letter] &
                          graph.neighborhoods[last_vertex], forbidden)
    if not candidates:
        return False

    return any(recurse(word[1:], graph, v, forbidden | v) for v in iterate(candidates))


def is_word_in_graph(word: str, graph: WordSearchGrid):
    letter = word[0]
    # print(graph.letters_to_vertices)
    candidates = (graph.letters_to_vertices[letter]
                  if letter in graph.letters_to_vertices else 0)
    # print(locals())
    if not candidates:
        return False

    return any(recurse(word[1:], graph, v, v) for v in iterate(candidates))


found_words = []

with open('./google-10000-english/google-10000-english.txt') as f:
    words = f.readlines()
    for word in words:
    # for word in ['stake']:
        # Strip \n and make upper
        word = word.upper()[:-1]
        # print('Trying {}'.format(repr(word)))
        if is_word_in_graph(word, grid):
            found_words.append(word)

print(found_words)
found_words.sort(key=lambda s: len(s))
for word in found_words:
    print(word)