import pytest
from snake.core import Cell, Factory, StepResult, Turn
from snake.core.game import Game
from snake.fakes import FixedFoodPlacer


class ScriptedPlayer:
    # Gives the given turns in order (ahead when out of turns); records what it was shown
    def __init__(self, *turns: Turn) -> None:
        self._turns = list(turns)
        self.results_seen: list[StepResult] = []

    def pick_turn(self, result: StepResult) -> Turn:
        self.results_seen.append(result)
        return self._turns.pop(0) if self._turns else Turn.ahead


class RecordingObserver:
    def __init__(self) -> None:
        self.started: list[StepResult] = []
        self.stepped: list[StepResult] = []

    def on_started(self, result: StepResult) -> None:
        self.started.append(result)

    def on_stepped(self, result: StepResult) -> None:
        self.stepped.append(result)


def make_world(row_count: int = 5, col_count: int = 5):
    # Snake starts at the centre heading right; food far away in the corner
    factory = Factory(row_count, col_count, food_placer=FixedFoodPlacer(Cell(0, 0)))
    return factory.create()


def make_game(player=None, observers=(), world=None) -> Game:
    return Game(
        world or make_world(),
        player or ScriptedPlayer(),
        observers,
    )


# ====================  Start  ====================


def test_start_gives_initial_result_to_every_observer():
    world = make_world()
    first, second = RecordingObserver(), RecordingObserver()
    make_game(observers=[first, second], world=world).start()
    assert first.started == [world.initial_result]
    assert second.started == [world.initial_result]
    assert first.stepped == []


def test_start_twice_is_rejected():
    sut = make_game()
    sut.start()
    with pytest.raises(RuntimeError):
        sut.start()


def test_tick_before_start_is_rejected():
    with pytest.raises(RuntimeError):
        make_game().tick()


# ====================  Tick  ====================


def test_tick_steps_the_world_with_the_picked_turn():
    sut = make_game(player=ScriptedPlayer(Turn.left))
    sut.start()
    assert sut.tick().head == Cell(1, 2)  # centre (2,2), turned up


def test_player_sees_the_latest_result():
    world = make_world()
    player = ScriptedPlayer()
    sut = make_game(player=player, world=world)
    sut.start()
    first = sut.tick()
    sut.tick()
    assert player.results_seen == [world.initial_result, first]


def test_tick_gives_its_result_to_every_observer():
    observer = RecordingObserver()
    sut = make_game(observers=[observer])
    sut.start()
    result = sut.tick()
    assert observer.stepped == [result]


# ====================  Over  ====================


def test_is_not_over_before_or_after_start():
    sut = make_game()
    assert not sut.is_over()
    sut.start()
    assert not sut.is_over()


def test_is_over_when_the_world_is_over():
    # 1x3 grid: snake starts at (0,1) heading right; second step hits the wall
    sut = make_game(world=make_world(1, 3))
    sut.start()
    sut.tick()
    assert not sut.is_over()
    sut.tick()
    assert sut.is_over()


def test_tick_after_the_game_is_over_is_rejected():
    sut = make_game(world=make_world(1, 3))
    sut.start()
    sut.tick()
    sut.tick()
    with pytest.raises(RuntimeError):
        sut.tick()
