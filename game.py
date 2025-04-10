import numpy as np
from player import Player
from powerup import PowerUp
from team import Team
from humanteam import HumanTeam


class Game:

    def __init__(self, team_1, team_2):
        self.modifier = np.random.normal(1, 0.1)
        if np.random.normal() > 0:
            self.first_bat, self.second_bat = team_1, team_2
        else:
            self.first_bat, self.second_bat = team_2, team_1
        self.name = f"{self.first_bat.name} v {self.second_bat.name}"

    def run_game(self):
        # Teams choose players and powerups
        self.first_bat.select_team()
        self.second_bat.select_team()
        first_powerup = self.first_bat.select_powerup()
        second_powerup = self.second_bat.select_powerup()
        # Generate scores
        go_print = (
            isinstance(self.first_bat, HumanTeam)
            or isinstance(self.second_bat, HumanTeam)
        )
        first_score = self.first_bat.get_team_score(
            first_powerup,
            target=np.inf,
            modifier=self.modifier,
            go_print=go_print
        )
        second_score = self.second_bat.get_team_score(
            second_powerup,
            target=first_score + 1,
            modifier=self.modifier,
            go_print=go_print
        )
        # Get result and process it
        if first_score == second_score:
            results = ["TIE", "TIE", "TIE"]
        elif first_score > second_score:
            results = ["WIN", "LOSS", f"{self.first_bat.name} WINS"]
        else:
            results = ["LOSS", "WIN", f"{self.second_bat.name} WINS"]
        self.first_bat.history.append(
            [first_powerup, results[0], first_score, second_score]
        )
        self.second_bat.history.append(
            [second_powerup, results[1], second_score, first_score]
        )
        return results[2]
