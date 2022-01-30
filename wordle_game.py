from enum import Enum
import random

import pdb

class Presence(Enum):
    NONE = 1
    PRESENT = 2
    CORRECT = 3

class GameError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class WordleGame:
    def __init__(self, word, max_guesses):
        self.word = word
        self.max_guesses = max_guesses
        self.guesses = 0
    
    def getguesses(self):
        return self.guesses

    def getword(self):
        return self.word

    def guess(self, word):
        if self.guesses == self.max_guesses:
            raise GameError("Game Over!")

        # This should never happen due to vocabulary screening, but check anyway
        if len(word) != len(self.word):
            raise GameError("Invalid word length!")

        result = []
        for ii in range(0, len(word)):
            if word[ii] == self.word[ii]:
                result.append(Presence.CORRECT)
            elif word[ii] in self.word:
                result.append(Presence.PRESENT)
            else:
                result.append(Presence.NONE)
        self.guesses += 1
        return result

# This is just a reusable wrapper around the game, so we don't move around the vocabulary more than we need to
class WordleEngine:
    def __init__(self, vocabulary):
        self.vocabulary = vocabulary
        self.game = None
        if len(vocabulary) == 0 or any(len(word) != len(vocabulary[0]) for word in vocabulary):
            raise ValueError("Invalid vocabulary!")

    def new_game(self, word=None, max_guesses=6):
        # If a word is not provided, get a random one
        if word is None:
            index = random.randint(0, len(self.vocabulary) - 1)
            word = self.vocabulary[index]

        word_formatted = word.strip().upper()
        self.game = WordleGame(word_formatted, max_guesses)

    def guess(self, word):
        if word not in self.vocabulary:
            raise GameError("Word not in vocabulary!")
        return None if (word not in self.vocabulary) else self.game.guess(word)

    def guesses(self):
        return self.game.getguesses()

    def word(self):
        return self.game.getword()
