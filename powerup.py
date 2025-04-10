import numpy as np
import random
from player import Player

class PowerUp:

    def __init__(self, operation, selection, num_players, constant):
        self.operation = operation
        self.selection = selection
        self.num_players = num_players
        self.constant = constant
        self.name = str(self)

    def __lt__(self, other):
        """ Just used for sorting them when displayed to human player """
        return self.operation < other.operation

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        selec = {
            "first_batters": "First",
            "random": "Random",
            "lowest_score": "Lowest scoring",
            "highest_score": "Highest scoring"
        }[self.selection]
        players = f"{self.num_players} get"
        if self.num_players == 1:
            players += "s" # Gotta pluralise!
        s = f"{selec} {players}"
        if self.operation == "plus_constant":
            return f"{s} {self.constant} bonus runs"
        elif self.operation == "plus_percent":
            return f"{s} extra {self.constant}% runs"
        elif self.operation == "multi_wickets":
            return f"{s} {self.constant} wickets each"
        elif self.operation == "individual_reroll":
            return f"{s} individual best score of {self.constant} attempts"
        elif self.operation == "group_reroll":
            return f"{s} collective best score of {self.constant} attempts"
        elif self.operation == "mult_or_divide":
            num = 1 + self.constant / 10
            return f"{s} score randomly multiplied or divided by {num:.1f}"
        elif self.operation == "square_runs":
            return f"{s} score squared"
        elif self.operation == "st_petersburg":
            return f"{s} a St Petersburg score"
        elif self.operation == "openers_all_plus":
            return f"Openers get all runs plus {self.constant} each"
        elif self.operation == "permute_plus":
            stump = "Scores are randomly permuted"
            return f"{stump}, all players get {self.constant} bonus runs"
        else:
            print("Operation not recognised")
            assert False

    def select_players(self, scores):
        if self.selection == "first_batters":
            return list(scores.keys())[:self.num_players]
        elif self.selection == "random":
            return random.sample(list(scores.keys()), self.num_players)
        elif self.selection == "lowest_score":
            return sorted(
                list(scores.keys()), key=scores.get
            )[:self.num_players]
        elif self.selection == "highest_score":
            return sorted(
                list(scores.keys()), key=scores.get
            )[-self.num_players:]
        else:
            print("Selection not recognised")
            assert False

    def apply_operation(self, scores, modified_players, modifier):
        """ Maps normally generates scores to modified scores """
        cd = scores.copy() # i.e., copy_dict
        if self.operation == "plus_constant":
            for player in modified_players:
                cd[player] += self.constant
        elif self.operation == "plus_percent":
            for player in modified_players:
                cd[player] = int(cd[player] * (1 + self.constant / 100))
        elif self.operation == "multi_wickets":
            for player in modified_players:
                cd[player] = sum([
                    player.get_score(modifier=modifier)
                    for _ in range(self.constant)
                ])
        elif self.operation == "individual_reroll":
            for player in modified_players:
                cd[player] = max([
                    player.get_score(modifier=modifier)
                    for _ in range(self.constant)
                ])
        elif self.operation == "group_reroll":
            for i in range(self.constant):
                old_sum = sum([cd[player] for player in modified_players])
                new_scores = {
                    player: player.get_score()
                    for player in modified_players
                }
                if sum(new_scores.values()) > old_sum:
                    for player in modified_players:
                        cd[player] = new_scores[player]
        elif self.operation == "mult_or_divide":
            for player in modified_players:
                if random.random() > 0.5:
                    cd[player] = int(cd[player] * (1 + self.constant / 10))
                else:
                    cd[player] = int(cd[player] / (1 + self.constant / 10))
        elif self.operation == "square_runs":
            for player in modified_players:
                cd[player] = cd[player] ** 2
        elif self.operation == "st_petersburg":
            for player in modified_players:
                cd[player] = 1
                while random.random() > 0.5:
                    cd[player] *= 2
        elif self.operation == "openers_all_plus":
            total = sum(scores.values())
            new_scores = [
                int(np.ceil(total / 2)) + self.constant,
                int(np.floor(total / 2)) + self.constant,
                0, 0, 0, 0
            ]
            for key, new_score in zip(scores.keys(), new_scores):
                cd[key] = new_score
        elif self.operation == "permute_plus":
            score_list = list(scores.values())
            random.shuffle(score_list)
            for player, score in zip(cd, score_list):
                cd[player] = score + self.constant
        else:
            print("Operation not recognised")
            assert False
        return cd

    def map(self, scores, modifier):
        modified_players = self.select_players(scores)
        new_scores = self.apply_operation(scores, modified_players, modifier)
        return new_scores
