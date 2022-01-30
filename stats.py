class Stats():
    def __init__(self, guesses):
        self.trials = 0
        self.maxguesses = guesses
        self.outcomes = {}
        self.outcomes[-1] = 0
        for ii in range(1, self.maxguesses+1):
            self.outcomes[ii] = 0

    def record(self, guesses, win):
        index = guesses if win else -1
        self.outcomes[index] += 1
        self.trials += 1

    def report(self):
        count = 0
        for ii in range(1, self.maxguesses+1):
            print("{}/{}: {}".format(ii, self.maxguesses, self.outcomes[ii]))
            count += self.outcomes[ii]
        print("X/{}: {}".format(self.maxguesses, self.outcomes[-1]))
        print()
        print("Trials: {}".format(self.trials))
        print("Win Rate: {}%".format((1.0 - (self.outcomes[-1] / self.trials))*100))
        print("Average guesses to win: {}".format(count * 1.0 / (self.trials-self.outcomes[-1])))
