from team import Team

class HumanTeam(Team):

    def __init__(self, name, skills, powerups, league):
        super().__init__(name, skills, powerups, league)

    def get_choice(self, options, command_string, num_to_choose=0):
        """
        Given options and a number that must be chosen
        Pesters the human until they give a choice
        Also allows the human to print out information
        """
        option_dict = dict(zip("abcdefghijklmnopqrstuvwxyz", options))
        while True:
            print(command_string)
            for key in option_dict:
                print(f"\t{key}. {option_dict[key].name}")
            choice = input()
            if choice.lower() == "history":
                self.display_history()
                continue
            elif choice.lower() == "table":
                self.league.display_table()
                continue
            elif all([letter in option_dict for letter in choice]):
                if (num_to_choose == 0 or
                    (len(choice) == num_to_choose
                    and len(set(choice)) == num_to_choose)):
                    return [option_dict[letter] for letter in choice]
            print("Invalid input, try again")
            continue

    def select_team(self):
        # Drop players
        if len(self.playing_team) > 0:
            dropees = self.get_choice(self.playing_team, "Drop players?", 0)
            for player in dropees:
                self.playing_team.remove(player)
        # Add new ones
        num_required = 6 - len(self.playing_team)
        if num_required > 0:
            options = [
                player for player in self.players.values()
                if player not in self.playing_team
            ]
            players_to_add = self.get_choice(
                options,
                f"Select {num_required}",
                num_required
            )
            for player in players_to_add:
                self.playing_team.append(player)

    def select_powerup(self):
        chosen_powerup = self.get_choice(
            sorted(self.powerups),
            "Choose power-up",
            1
        )[0]
        self.powerups.remove(chosen_powerup)
        return chosen_powerup
