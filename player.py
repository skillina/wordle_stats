# Defines the interface for our various player types.
class Player():
    def __init__(self, warn_on_repeat = False):
        self.past_guesses = set()
        self.warn_on_repeat = warn_on_repeat

    # Reset past guess list at the beginning of the game
    def reset_memory(self):
        self.past_guesses = set()

    # Generate a guess, which we have not guessed before
    def guess(self):
        while True:
            new_guess = self.guess_impl()
            if new_guess not in self.past_guesses:
                self.past_guesses.add(new_guess)
                return new_guess
            elif self.warn_on_repeat:
                print("Word already used!\n")
    
    def give_feedback(self, guess, result):
        pass

    # Override this in the derived classes to actually generate the guess
    def guess_impl(self):
        raise NotImplementedError()