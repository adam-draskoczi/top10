from project import get_players, get_rounds, Player, set_players

def test_get_players(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 3)
    assert get_players() == 3
    monkeypatch.setattr("builtins.input", lambda _: 10)
    assert get_players() == 10

def test_get_rounds(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 3)
    assert get_rounds() == 3
    monkeypatch.setattr("builtins.input", lambda _: 1)
    assert get_rounds() == 1

def test_set_players():
    assert set_players(0) == []

player = Player(1, "Adam")

def test_get_answer():
    player.get_answer()
    assert player.answer_score == 1

def test_get_guess():
    player.get_guess()
    assert player.guess_score == 1
    player.get_guess()
    assert player.guess_score == 2

def test_get_total():
    player.get_total()
    assert player.total_score == 3