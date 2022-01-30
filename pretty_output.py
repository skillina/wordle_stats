from enum import Enum
from functools import total_ordering
from wordle_game import Presence

@total_ordering
class DisplayMode(Enum):
    NONE = 0
    RESULTS = 1
    PRETTY_NOSHARE = 2
    PRETTY = 3
    FULL = 4

    def __lt__(self, other):
        return self.value < other.value

class PrettyOutput():
    def __init__(self, guessmax, display_mode_string):
        modemap = {
            "none": DisplayMode.NONE,
            "results": DisplayMode.RESULTS,
            "noshare": DisplayMode.PRETTY_NOSHARE,
            "pretty": DisplayMode.PRETTY,
            "full": DisplayMode.FULL
        }

        self.guessmax = guessmax
        self.display_mode = modemap[display_mode_string]
        self.guess_history = []
        self.result_history = []
    
    def end_game(self, win):
        # Draw the grid of the guesses
        if self.display_mode >= DisplayMode.PRETTY:
            for result in self.result_history:
                self.report_guess(" " * len(result), result, True)

        if self.display_mode >= DisplayMode.RESULTS:
            numerator = len(self.result_history) if win else "X"
            print("Wordle custom: {}/{}".format(numerator, self.guessmax))
            print("\n\n")

        self.result_history = []

    def trigger_redraw(self):
        if len(self.guess_history) != len(self.result_history):
            raise RuntimeError("Guess history length doesn't match result history length")
        print()
        for ii in range(0, len(self.guess_history)):
            self.report_guess(self.guess_history[ii], self.result_history[ii], True)
        print()

    def report_guess(self, guess, result, redrawing=False):
        if not redrawing:
            self.guess_history.append(guess)
            self.result_history.append(result)

        if self.display_mode <= DisplayMode.RESULTS:
            return

        colormap = {Presence.NONE: '\033[100m',
                    Presence.PRESENT: '\033[43m',
                    Presence.CORRECT: '\033[42m'}

        if len(guess) != len(result):
            raise RuntimeError("Guess length doesn't match result length")
        
        frankenstring = ""
        for ii in range(0, len(guess)):
            frankenstring += colormap[result[ii]] + guess[ii]
        frankenstring += '\033[0m'
        print(frankenstring)

        if self.display_mode == DisplayMode.FULL and not redrawing:
            self.trigger_redraw()