import numpy as np
import pandas as pd
import random
from player import Player
from powerup import PowerUp
from team import Team
from randombotteam import RandomBotTeam
from humanteam import HumanTeam
from game import Game

class League:

    def __init__(self):
        skills = abs(np.random.normal(25, 20, 11)).astype(int) + 1
        powerups = [self.generate_powerup() for _ in range(17)]
        self.teams = dict()
        team_names = list(pd.read_csv("teams.txt", header=None)[0])
        player_team = self.get_team(team_names)
        for name in team_names:
            np.random.shuffle(skills)
            if name == player_team:
                self.teams[name] = HumanTeam(name, skills, powerups, self)
            else:
                self.teams[name] = RandomBotTeam(name, skills, powerups, self)
        self.fixtures = self.generate_fixtures(self.teams)
        self.results = {team: [] for team in self.teams.keys()}

    def generate_powerup(self):
        powerup_list = [ # of form (name, min_const, mean_const, prob, weight)
            ("plus_constant", 2, 5, 0.5, 20),
            ("plus_percent", 5, 10, 0.4, 10),
            ("multi_wickets", 2, 2.5, 0.3, 8),
            ("individual_reroll", 2, 2.5, 0.2, 12),
            ("group_reroll", 2, 2.5, 0.4, 10),
            ("mult_or_divide", 5, 8, 0.6, 10),
            ("square_runs", 1, 1, 0.02, 4),
            ("st_petersburg", 1, 1, 0.02, 5),
            ("openers_all_plus", 5, 8, 0.00001, 8),
            ("permute_plus", 3, 5, 0.99999, 12)
        ]
        selection_list = [
            "first_batters",
            "random",
            "lowest_score",
            "highest_score"
        ]
        weights = [i[-1] for i in powerup_list]
        chosen_powerup = random.choices(powerup_list, weights=weights, k=1)[0]
        operation = chosen_powerup[0]
        selection = random.choices(selection_list, weights=[1,5,4,2], k=1)[0]
        num_players = 1 + np.random.binomial(5, chosen_powerup[3])
        constant = int(
            chosen_powerup[1]
            + np.random.exponential(chosen_powerup[2] - chosen_powerup[1])
        )
        powerup = PowerUp(operation, selection, num_players, constant)
        return powerup

    def get_team(self, team_names):
        print("Choose a team out of the following:")
        for name in team_names:
            print(f"\t{name}")
        while True:
            user_choice = input()
            if user_choice in team_names:
                return user_choice
            else:
                print("Invalid choice")

    def generate_fixtures(self, teams):
        """
        Create all n choose k games, and shuffle the order up
        """
        fixtures = []
        for team_1 in self.teams:
            for team_2 in self.teams:
                if team_1 <= team_2: # Can't play self, and avoid double ups
                    continue
                new_fixture = Game(self.teams[team_1], self.teams[team_2])
                fixtures.append(new_fixture)
        np.random.shuffle(fixtures)
        return fixtures

    def run_league(self):
        for game in self.fixtures:
            result = game.run_game()
            for team in [game.name.split(" ")[0], game.name.split(" ")[2]]:
                if result == "TIE":
                    self.results[team].append(0.5)
                else:
                    self.results[team].append(int(team in result))

    def display_table(self):
        """ Shows table of results for each team """
        column_results = {
            team: [i for i in self.results[team]]
            for team in self.teams
        }
        max_length = max([len(column_results[team]) for team in self.teams])
        for team in self.teams:
            try:
                wins = sum(column_results[team])
            except TypeError:
                print(column_results[team])
            column_results[team] += (
                ["."] * (max_length - len(column_results[team])) + [wins]
            )
        table = pd.DataFrame(
            column_results,
            index=[i for i in range(1, max_length + 1)] + ["total"]
        )
        display(table.T.sort_values(by="total", ascending=False))

    def get_best_batters(self):
        """ Shows two tables, of best batters by total and by average """
        batters = [
            batter for team in self.teams.values() for batter in team.squad
        ]
        team_names = [team for team in self.teams for _ in range(11)]
        names = [batter.name for batter in batters]
        totals = [batter.get_total_score() for batter in batters]
        averages = [batter.get_average() for batter in batters]
        innings = [
            len([s for s in batter.past_scores if s != "-"])
            for batter in batters
        ]
        df = pd.DataFrame({
            "team": team_names,
            "total": totals,
            "average": averages,
            "innings": innings
        }, index=names)
        print("Top ten batters by total:")
        display(df.sort_values(by="total", ascending=False).head(10))
        print("Top ten batters by average:")
        display(df.sort_values(by="average", ascending=False).head(10))
