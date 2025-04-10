**Rules**

The County Championships is one of cricket's most prestigious trophies, and is a hotly-contested competition fought between 18 teams in front of crowds as large as fifteen. This year you have been chosen to manage one of those teams, and you have one task: win. 

Each team has a squad of 11 players, of which you get to choose 6 that play in a given game. Each player has a single hidden stat, which is their skill: a player with a skill of 20 will, all things equal, average 20 per game. However, they will score exactly 20 quite rarely, because their score for a given game is geometrically distributed. So it might take a while for low-skill players' deficits to become apparent: even the lowest skill players can score centuries. (For fairness, each team is given the same set of skills. So if you have a bunch of awful players, all the other teams are carrying the same burden.)

There are three further sources of noise to complicate the game of figuring out who is good and who is not. First, because games are not played until the final batter gets out, some scores are censored. There must always be two batters on the pitch, which means that when the second-last batter gets out, the final batter also must go back to the shed because they have no partner. So even if one player would have scored 1000, if everyone else on the team scores single digits they won't be able to realise that score because they will run out of teammates to bat with. So they are probably only going to get to, say, 30, and that score will be marked as not out with an asterisk (so the scoresheet will have them as "30*"). Furthermore, as soon as the second team's score overtakes the first team's, the game ends because the result is already determined. That means that the two batters who are in have their scores taken and marked as not out (again, even if they would have gone on to score many more runs), and if there are any players who never got in they will have their scores marked with a dash. 

Second, there is variation in conditions from day to day, which means that in some games it is easier to score a high total than others. This is implemented as there being a "modifier" parameter, which is selected from $N(1, 0.1)$, which each player's skill is multiplied by before calculating scores. For example, if the game modifier is 0.9, a player who normally averages 30 will be scoring as though they have an average of 27. 

Third, there are power-ups which teams play in each game. These could be thought of as novel game-specific strategies, or "enhanced meal plans", which for some reason can only be used once. These are applied after each batter has an initial score calculated, which the power-up then modifies to produce their final score. Each team starts with the same randomly-generated 17 and plays one per game over the season. They are: 
* $x$ bonus runs: the players specified get $x$ runs added to the number they score;
* Extra $x$%: the players specified have their score multiplied by $1 + \frac{x}{100}$;
* $x$ wickets each: the players specified get $x$ scores, and their score is the sum of those scores;
* Individual best score of $x$ attempts: the players specified get $x$ scores, and each player's score is the best of their scores. For example, for if two players get the best of two scores, and the first generates [10, 11] and the second generates [12, 3], the first player will get 11 and the second will get 12;
* Collective best score of $x$ attempts: scores are generated for the group of players specified $x$ times. Out of those $x$ attempts, the one that maximises the sum of batters' scores is chosen. So, for the previous example, the players will get 10 and 12 respectively, because $10 + 12 > 3 + 11$;
* Randomly multiply or divide by $x$: the players specified get their score either multiplied by $x$ or divided by $x$, with equal probaiblity;
* Score squared: the players specified get their scores squared;
* St Petersburg score: the [St Petersburg game](https://plato.stanford.edu/entries/paradox-stpetersburg/) is played for each player, and the outcome is their score;
* Openers get all runs plus $x$ each: runs are calculated for the whole team, which are then summed up and split equally between the first two players, who then each get $x$ runs on top of that;
* Scores are randomly permuted, all players get $x$ bonus runs: players' scores are generated, then randomly shuffled among all the players, and on top of that each gets $x$ more runs.

So, as a manager, you can't affect the skill of your players, and you also can't affect their in-game luck: even if you choose the best players, they can score dismally. However, you have two things in your control. First, you can choose the best players from your squad to play the games. And second, you can choose the best power-up for each occasion. 

**To play**

* Download the program files from [Google Drive](https://drive.google.com/file/d/1iEPInZ4yNjG3dCwLUWfaDiPYC-_4dU7Z/view?usp=sharing) and put them in the same directory as this notebook (if using Colab, upload them into the files folder in the sidebar).
* If playing on Colab run the cell below, otherwise open up play_game.ipynb and run the first cell.
* Type in the name of the team you want to play as.
* When offered a choice, put in just the letter of the option you want. If you want to submit multiple options, put in all those options concatenated, e.g., if you want to select players a-f, type in "abcdef". 
* To help making decisions, at any point you can type in "history" which pulls up records of your players' individual performances, or (less informatively) "table" which pulls up the league table. 
* After the game, you can run the cells in the following section to show the league table, the true skill levels of each player, and a summary of the best batters in the league.

Good luck - you'll probably need some!
