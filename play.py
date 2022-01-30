#!/usr/bin/python3
import argparse
from generate_vocab import generate_vocabulary
from wordle_game import WordleEngine, Presence, GameError
from interactive_player import InteractivePlayer
from pretty_output import *

# Maybe I didn't need another layer of abstraction here, but we have it anyway.
class Game():
    def  __init__(self, args):
        self.args = args
        self.vocabulary = self.load_vocabulary()
        self.player = self.player_select()
        self.engine = WordleEngine(self.vocabulary)
        self.output = PrettyOutput(self.args.guesses, self.args.displaymode)

    def player_select(self):
        if self.args.strategy == "interactive":
            return InteractivePlayer()

    def load_vocabulary(self):
        if self.args.vocabulary is None:
            print("No vocabulary file given... Generating from dictionary!\n")
            return generate_vocabulary(self.args.dictionary, self.args.length, "/dev/null")

        vocab = []
        with open(self.args.vocabulary, 'r') as vocabfile:
            for line in vocabfile:
                vocab.append(line.strip().upper())
        return vocab

    def win_condition(self, result):
        return result == [Presence.CORRECT] * self.args.length

    def play(self):
        for loop_iteration in range(0, self.args.gamelimit):
            self.engine.new_game(self.args.forceword.strip().upper(), self.args.guesses)
            self.player.reset_memory()
            win = False
            while self.engine.guesses() < self.args.guesses:
                try:
                    guess = self.player.guess()
                    result = self.engine.guess(guess)

                    self.output.report_guess(guess, result)
                    self.player.give_feedback(guess, result)
                    win = self.win_condition(result)
                    if  win:
                        break
                except GameError as e:
                    print(e)
                    print("\n")

            self.output.end_game(win)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play Wordle!')
    parser.add_argument("--strategy", default="interactive", help="Strategy to apply")
    parser.add_argument("--vocabulary", default=None, help="Path to a pre-generated vocabulary. If none, it will be generated.")
    parser.add_argument("--dictionary", default="/usr/share/dict/words", help="Path to a raw word list, which may not be the right size or may contain invalid characters.")
    parser.add_argument("--length", default=5, type=int, help="Word length")
    parser.add_argument("--guesses", default=6, type=int, help="Number of guesses per game")
    parser.add_argument("--forceword", default=None, help="Force a word for the game")
    parser.add_argument("--gamelimit", default=100, help="Number of games to play")
    parser.add_argument("--displaymode", default="full", help="Display mode. Options: none, results, noshare, pretty, full")
    args = parser.parse_args()

    game = Game(args)
    game.play()