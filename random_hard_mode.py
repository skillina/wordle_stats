from player import Player
import random
from wordle_game import Presence

class BotPlayer(Player):
    def __init__(self, vocabulary):
        super().__init__(False)
        self.vocabulary = vocabulary
        self.known_presence = {}
        self.known_positions = {}

    def reset_memory(self):
        super().reset_memory()
        self.known_presence = {}
        self.known_positions = {}
    
    def random_vocab_word(self):
        index = random.randint(0, len(self.vocabulary)-1)
        return self.vocabulary[index]
    
    def give_feedback(self, guess, result):
        if len(guess) != len(result):
            raise RuntimeError("Guess length != Result length!")

        for index, char in enumerate(guess):
            if result[index] == Presence.CORRECT:
                self.known_presence[char] = Presence.PRESENT
                self.known_positions[index] = char
            else:
                self.known_presence[char] = result[index]

    # Determine if a word could still be the final result, based on the feedback given.
    def still_eligible(self, word):
        for index in self.known_positions.keys():
            if word[index] != self.known_positions[index]:
                return False

        for char in word:
            if (char in self.known_presence) and (self.known_presence[char] == Presence.NONE):
                return False
        
        return True

# Pick a random word, which passes the "hard mode" filter - use all clues.
class TrueChaoticPlayer(BotPlayer):
    def __init__(self, vocabulary):
        super().__init__(vocabulary)

    def guess_impl(self):
        return self.random_vocab_word()

# Pick a random word, which passes the "hard mode" filter - use all clues.
class RandomizedHardModePlayer(BotPlayer):
    def __init__(self, vocabulary):
        super().__init__(vocabulary)

    def guess_impl(self):
        while True:
            pick = self.random_vocab_word()
            if self.still_eligible(pick):
                return pick