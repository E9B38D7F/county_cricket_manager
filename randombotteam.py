from team import Team
import random

class RandomBotTeam(Team):

    def __init__(self, name, skills, powerups, league):
        """
        This bot doesn't think too hard:
        given a choice, it chooses an option at random
        """
        super().__init__(name, skills, powerups, league)

    def select_team(self):
        self.playing_team = random.sample(self.squad, 6)

    def select_powerup(self):
        chosen_powerup = random.choice(self.powerups)
        self.powerups.remove(chosen_powerup)
        return chosen_powerup
