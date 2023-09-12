from os import system
from random import shuffle
from scipy.stats import rankdata
from tabulate import tabulate

with open("prompts.txt") as file:
    prompts = file.readlines()
shuffle(prompts)

players = []


class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self._guess_score = 0
        self._answer_score = 0
        self._total_score = 0

    @classmethod
    def get(cls, p):
        id = p + 1
        while True:
            name = input(f"Name of {id}. player: ")
            if name and name not in [player.name for player in players]:
                break
            else:
                print("Please type a unique name.")
                pass
        return cls(id, name)

    # Order of answer to be given
    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, order):
        self._order = order

    # Given answer to prompt
    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, answer):
        self._answer = answer

    # Points from correctly guessing orders
    @property
    def guess_score(self):
        return self._guess_score

    @guess_score.setter
    def guess_score(self, guess_score):
        self._guess_score = guess_score
        self.get_total()

    def get_guess(self):
        self.guess_score += 1

    # Points from others correctly guessing player's order
    @property
    def answer_score(self):
        return self._answer_score

    @answer_score.setter
    def answer_score(self, answer_score):
        self._answer_score = answer_score
        self.get_total()

    def get_answer(self):
        self.answer_score += 1

    # Total score (sum of guess scores and answer scores)
    @property
    def total_score(self):
        return self._total_score

    @total_score.setter
    def total_score(self, total_score=0):
        self._total_score = total_score

    def get_total(self):
        self.total_score = self.guess_score + self.answer_score

    # Rank of player based on total score
    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, rank=0):
        self._rank = rank


def main():
    system("clear")
    input(
        "WELCOME TO TOP10!\n\nThe program imitates the well known tabletop game of the same name in which players are given a prompt and a position in ranking, having to give an answer to the prompt, thus creating a ranked list from best to worst answer.\nPlayers then have to guess which answer is at which position of the list. Players get point for correct guesses as well as if someone else correctly guesses their answer's rank.\n\nPress Enter to start the game."
    )
    system("clear")
    players_no = get_players()
    rounds_no = get_rounds()

    players = set_players(players_no)
    print("Players:")
    for id in range(len(players)):
        print(f"* {players[id].name}")
    print()
    input(f"Press Enter to start the game for {players[0].name}.")
    system("clear")

    for r in range(rounds_no):
        prompt = game(r, rounds_no)

        solutions(prompt)
        print("\n")

        if r < rounds_no - 1:
            input(f"End of Round {r + 1}. Press Enter to start Round {r + 2}.")
        else:
            input("End of game. Press Enter to see the results.")
        system("clear")

    results()


def get_players():
    while True:
        try:
            players_no = int(input("Number of players (3-10): "))
        except ValueError:
            pass
        else:
            if 3 <= players_no <= 10:
                return players_no
            else:
                pass


def get_rounds():
    while True:
        try:
            rounds_no = int(input(f"Rounds to play (1-{len(prompts)}): "))
        except ValueError:
            pass
        else:
            if 1 <= rounds_no <= len(prompts):
                system("clear")
                return rounds_no
            else:
                pass


def set_players(players_no):
    for p in range(players_no):
        player = Player.get(p)
        players.append(player)
    system("clear")
    return players


def game(r, rounds_no):
    prompt = prompts[r].strip()

    orders = [player.id for player in players]
    shuffle(orders)

    # Answering part
    for player, order in zip(players, orders):
        print(f"Round {r + 1}. of {rounds_no}")
        print(f"The prompt is: {prompt}\n")
        print(
            f"{player.name}, your rank is {order} (out of {len(orders)}, with 1 being the best and {len(orders)} being the worst). Reply to the prompt with an answer that should fit the rank."
        )

        while True:
            answer = input("Type your answer here and press Enter: ")
            if answer:
                player.order = order
                player.answer = answer
                system("clear")
                break
            else:
                pass

        if player.id < len(players):
            input("Press Enter for the next player.")
            system("clear")

    answers(prompt)
    input(f"Press Enter to start guessing for {players[0].name}.")

    system("clear")

    # Guessing part
    for player in players:
        print(f"{player.name} is guessing\n")
        answers(prompt)
        print(f"\nGuess the actual order of each answer below and press Enter.")
        for p in players:
            if player.id != p.id:
                print(f"The answer is: {p.answer}")
                while True:
                    try:
                        guess = int(input("The order is: "))
                    except ValueError:
                        pass
                    else:
                        if p.order == guess:
                            player.get_guess()
                            p.get_answer()
                        break
        system("clear")
    return prompt

def answers(prompt):
    print(f"The prompt is: {prompt}")
    print("The answers are, in order of players:")
    for player in players:
        print(f"* {player.answer}")
    print()

def solutions(prompt):
    print(f"The prompt is: {prompt}")

    solutions = sorted(players, key=lambda player: player.order)

    print("The correct answers are:")
    for solution in solutions:
        print(f"{solution.order}. -> {solution.answer} (by {solution.name})")
    print()

def results():
    ranks = rankdata([player.total_score for player in players], method="max")

    for i in range(len(ranks)):
        players[i].rank = len(ranks) - ranks[i] + 1

    results = sorted(
        sorted(players, key=lambda player: player.guess_score, reverse=True),
        key=lambda player: player.rank,
    )

    final = [
        {
            "Rank": player.rank,
            "Name": player.name,
            "Total score": player.total_score,
            "Guess score": player.guess_score,
            "Answer score": player.answer_score,
        }
        for player in results
    ]

    print(
        tabulate(
            final, headers="keys", tablefmt="grid", numalign="center", stralign="center"
        ) + "\n"
    )
    print("Congratulations!\n")


if __name__ == "__main__":
    main()
