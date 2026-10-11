import pytest
from snake.core import Cell, Factory, Turn, WorldState
from snake.core.game import Game
from snake.fakes import FixedFoodPlacer


class ScriptedPlayer:
    # Gives the given turns in order (ahead when out of turns); records what it was shown
    def __init__(self, *turns: Turn) -> None:
        self._turns = list(turns)
        self.states_seen: list[WorldState] = []

    def pick_turn(self, state: WorldState) -> Turn:
        self.states_seen.append(state)
        return self._turns.pop(0) if self._turns else Turn.ahead


class RecordingObserver:
    def __init__(self) -> None:
        self.started: list[WorldState] = []
        self.stepped: list[WorldState] = []

    def on_started(self, state: WorldState) -> None:
        self.started.append(state)

    def on_stepped(self, state: WorldState) -> None:
        self.stepped.append(state)


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


def test_start_gives_initial_state_to_every_observer():
    world = make_world()
    first, second = RecordingObserver(), RecordingObserver()
    make_game(observers=[first, second], world=world).start()
    assert first.started == [world.initial_state]
    assert second.started == [world.initial_state]
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


def test_player_sees_the_latest_state():
    world = make_world()
    player = ScriptedPlayer()
    sut = make_game(player=player, world=world)
    sut.start()
    first = sut.tick()
    sut.tick()
    assert player.states_seen == [world.initial_state, first]


def test_tick_gives_its_state_to_every_observer():
    observer = RecordingObserver()
    sut = make_game(observers=[observer])
    sut.start()
    state = sut.tick()
    assert observer.stepped == [state]


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
