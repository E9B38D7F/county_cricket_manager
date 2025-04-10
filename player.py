import numpy as np
import pandas as pd

class Player:

    def __init__(self, skill):
        """ Skill is their batting average """
        self.skill = skill
        self.name = self.get_name()
        self.past_scores = []

    def get_name(self):
        fn = pd.read_csv("first_names.txt", header=None)[0].sample(1).item()
        sn = pd.read_csv("surnames.txt", header=None)[0].sample(1).item()
        return f"{fn} {sn}"

    def get_score(self, modifier=1):
        """ Higher modifier is higher score """
        lambd = modifier / (self.skill + 1)
        score = np.random.geometric(lambd) - 1
        return score

    def get_total_score(self):
        not_outs = [int(s[:-1]) for s in self.past_scores if "*" in s]
        outs = [int(s) for s in self.past_scores if s != "-" and "*" not in s]
        return sum(not_outs) + sum(outs)

    def get_average(self):
        not_outs = [int(s[:-1]) for s in self.past_scores if "*" in s]
        outs = [int(s) for s in self.past_scores if s != "-" and "*" not in s]
        try:
            return (sum(outs) + sum(not_outs)) / len(outs)
        except ZeroDivisionError:
            return np.nan
