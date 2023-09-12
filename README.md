# TOP10
#### Video Demo:  https://youtu.be/jgyhaKveKww
#### Description:

The program imitates the well known tabletop game of the same name in which players are given a prompt and a position in ranking, having to give an answer to the prompt creating a ranked list from best to worts answer. Players then have to guess which answer is at which position of the list.

### project.py

This file contains the core of the program.
Necessary methods and functions are imported from their respective libraries on the top of the file. The prompts.txt file containing the possible prompts is also read into a list type variable called `prompts` and shuffled to ensure random order of unique prompts throughout the game.

Next a class is defined by the name Player. Each instance has an id, a name, a guess_score and an answer_score. The `get(cls, p)` method is used to get the necessary values for id and name when an instance object is created for a player. The function also validates the answers and re-prompts the user in case of missing or redundant names.

A handful of properties and functions are also defined: the order of the expected answer of the player in the current round of game, the answer given to the prompt, points from correctly guessing the order of others' answers as well as from others correctly guessing the order of the player's answer, total score (sum of previous two) and the final rank of the player, based on total points.

The `main()` function contains the course of the program, calling each function when necessary. Firstly the game rules are displayed, the program then commences.

The `get_players()` function, when called, prompts the user for the number of players to participate in the game. In case of an invalid answer (eg not a whole number or out of the acceptable range) the user is re-prompted. Otherwise the input is returned to the main function as integer.

The `get_rounds()` function similarly prompts the user for an other integer, this time for the number of rounds to play which is then returned. This is always limited between 1 and the length of the `prompts` list (aka the number of prompts, to avoid repetition).

The `set_players(players_no)` function takes the number of players as an input and iterates over each prospective player, calling the constructor with the class's `get(p)` function, with the ordinal of player as an argument. The recently created player object is then appended to a list of players, which is eventually returned by the function.

The main function then displays the name of each player (for a check) and then the game starts.

The `game(r, rounds_no)` function is called for each round via a for loop over the range of number of rounds (retrieved and returned by the `get_rounds()` function earlier), passing the iteration variable as the parameter r into the function. This r then used to pick the corresponding prompt from the list `prompts` which stays unchanged throughout the game to ensure there is no repetition of the unique prompts. A list of `orders` is also created and shuffled randomly that will be used to assign each player an order of which they have to give their answer. The function then iterates over the global list of players and local list of orders, pairing up each player with their order. A message and the prompt is printed, asking the user for their valid (not empty) input. Once given, the order and the answer are saved to the current player object's `player.order` and `player.answer` attributes. The terminal window is then cleared and shows a warning message before moving to the next player to ensure fair game.

Once all the answers are given, they are displayed along the prompt by calling the `answers(prompt)` function and printing an iteration over the answer property of each player object. After this, the game commences to guessing, player by player.

Each player is asked to guess the order of each answer other than theirs - this is ensured by comparing the id attribute of the current player with the id of the player whose answer is to be guessed. All answers are visible for the players convenience, as an iteration over the answer attribute of each object in the `players` list. The answers are also used one by one for prompting the player for their guess. In case of a succesful guess, the `get_guess()` and `get_answer()` methods are called for the objects of the player guessing player that gave the answer respectively, increasing their respective scores by one for each. These methods also call the `get_total()` method of their self objects, updating the value of total score. The window is again cleared after each player. After the last player within the round, the solutions are printed in correct order, by calling the `solutions(prompt)` function. This takes the returned prompt string from the game function and iterates over a sorted list of the player objects.

This repeats for each iteration over the number of rounds.

The results are then displayed via main calling the `results` function. Firstly the rankdata function from the scipy library is utilised to assign each player a rank based on their total scores, then this rank is assigned to each player's rank attribute. (More exactly: Since the rankdata ranks values in ascending order but the results should be in descending, the rank is corrigated.) The list of players is then re-sorted first by guess score and then by total score, therefore in case of a tie, players with higher guess score are displayed first. The attributes of the players are then saved into a list of dictionaries called `final` which in turn is used to display the results by feeding the list into the tabulate function of the tabulate library.

### prompts.txt

This file contains several possible prompts that can be used for the game. The file is read at the beginning of the program into a list, which is then shuffled. Prompts are picked in this order throughout the rounds.

### requirements.txt

This file lists the external, pip installable libraries and their version that have been used for the project.

### test_project.py

This test file is used to test functions as well as methods of the original project. As most of the files rely on user inputs within the file, monkeypatch is utilised to provide a mock input in such cases.