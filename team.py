import numpy as np
import pandas as pd
from player import Player
from powerup import PowerUp

class Team:

    def __init__(self, name, skills, powerups, league):
        """
        squad is list of Player objects
        players is dictionary of (name, Player) pairs
        playing_team is list of Player objects
        powerups is list of PowerUp objects
        history is list of (powerup played, results, score, opp score) tuples
        league is League
        """
        assert len(skills) == 11
        assert len(powerups) == 17
        self.name = name
        self.squad = [Player(skill) for skill in skills]
        self.players = {player.name: player for player in self.squad}
        self.playing_team = []
        self.powerups = [i for i in powerups]
        self.history = []
        self.league = league

    def display_history(self):
        """ Pulls up dataframe showing info about each game played """
        history_a = pd.DataFrame(
            {player.name: player.past_scores for player in self.squad}
        )
        history_b = pd.DataFrame(self.history, columns=
            ["powerups", "result", "own_score", "opp_score"]
        )
        display(pd.concat([history_a, history_b], axis=1))

    def select_team(self):
        """ Sets self.playing_team to a list of 6 players """
        raise NotImplementedError

    def select_powerup(self):
        """ Returns the powerup being played, deletes it from self.powerups """
        raise NotImplementedError

    def get_team_score(self, powerup, target, modifier=1, go_print=False):
        """
        Gets the selected players to record a score
        And return total score
        NOTE: target is the score to WIN, if 1 under target it's a TIE
        """
        def get_stacks(target, playing_team, scores):
            """
            Returns history of who scored what and at what end
            stack_a_players is players who were at one end of the wicket
            stack_b_players is players who were at the other end
            (i.e., all partnerships made of a stack A player and a
            stack B player). Scoring rate assumed constant.
            If a player never bats, they won't be in either stack
            """
            stack_a, stack_a_players = 0, []
            stack_b, stack_b_players = 0, []
            for player in playing_team:
                if stack_a <= stack_b:
                    stack_a += scores[player]
                    stack_a_players.append(player)
                else:
                    stack_b += scores[player]
                    stack_b_players.append(player)
                if (stack_a >= target / 2 and stack_b >= target / 2
                    and stack_a + stack_b >= target):
                    break
            return stack_a_players, stack_b_players

        def censor(sap, sbp, target, scores):
            """
            Won't see all the players' scores
            If they get bowled out, one will be left stranded
            And if they chase successfully, two are left not out
            while all batters behind them have no score
            (sap and sbp are stack_a_players and stack_b_players respectively)
            """
            stack_a = sum([scores[p] for p in sap])
            stack_b = sum([scores[p] for p in sbp])
            if (stack_a >= target / 2 and stack_b >= target / 2
                and stack_a + stack_b >= target): # Censor both chasing batters
                censored_scores = {
                    sap[-1]: (
                        np.ceil(target/2) - sum([scores[p] for p in sap[:-1]])
                    ),
                    sbp[-1]: (
                        np.floor(target/2) - sum([scores[p] for p in sbp[:-1]])
                    )
                }
                uncensored_scores = {p: scores[p] for p in sap[:-1] + sbp[:-1]}
            else: # Censor last batter standing
                diff = max(stack_a, stack_b) - min(stack_a, stack_b)
                if stack_a > stack_b:
                    censored_scores = {sap[-1]: scores[sap[-1]] - diff}
                    uncensored_scores = {p: scores[p] for p in sap[:-1] + sbp}
                else:
                    censored_scores = {sbp[-1]: scores[sbp[-1]] - diff}
                    uncensored_scores = {p: scores[p] for p in sap + sbp[:-1]}
            return censored_scores, uncensored_scores

        def assign_scores(self, censored_scores, uncensored_scores, go_print):
            """
            Saves scores for each player
            Prints them if necessary
            """
            final_scores = []
            team_total = 0
            for player in self.squad:
                if player in censored_scores:
                    score = f"{int(censored_scores[player])}*"
                    team_total += int(censored_scores[player])
                elif player in uncensored_scores:
                    score = f"{uncensored_scores[player]}"
                    team_total += int(uncensored_scores[player])
                else:
                    score = "-"
                final_scores.append(score)
                player.past_scores.append(score)
            if go_print:
                print(f"{self.name} results:")
                for player in self.playing_team:
                    print(f"{player.past_scores[-1]}:\t{player.name}")
                print(f"TOTAL: {team_total}\n")
            return team_total

        scores = {
            player: player.get_score(modifier=modifier)
            for player in self.playing_team
        }
        scores = powerup.map(scores, modifier)
        sap, sbp = get_stacks(target, self.playing_team, scores)
        censored_scores, uncensored_scores = censor(sap, sbp, target, scores)
        team_total = assign_scores(
            self,
            censored_scores,
            uncensored_scores,
            go_print
        )
        return team_total
