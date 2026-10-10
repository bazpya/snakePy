import pytest
from snake.core._grid import Grid
from snake.core.direction import Direction
from snake.core.end_cause import EndCause
from snake.core.world import World
from snake.core.cell import Cell
from snake.core._snake import Snake
from snake.core.turn import Turn

START = Cell(2, 2)
FAR_FOOD = Cell(0, 0)


class ScriptedFoodPlacer:
    # Places food at the given cells in order; records what was free
    def __init__(self, *cells: Cell) -> None:
        self._cells = list(cells)
        self.free_given: list[list[Cell]] = []

    def place_food(self, free) -> Cell:
        self.free_given.append(list(free))
        return self._cells.pop(0)


def make_world(
    snake: Snake | None = None,
    food_placer: ScriptedFoodPlacer | None = None,
    grid: Grid | None = None,
    unfed_step_limit: int | None = None,
) -> World:
    return World(
        grid or Grid(5, 5),
        snake or Snake(START, Direction.right),
        food_placer or ScriptedFoodPlacer(FAR_FOOD),
        unfed_step_limit,
    )


def make_long_snake() -> Snake:
    # Body (tail -> head): (2,1) (2,2) (2,3) (3,3) (3,2), heading left
    snake = Snake(Cell(2, 1), Direction.right)
    snake.step(grow=True)
    snake.step(grow=True)
    snake.turn(Turn.right)
    snake.step(grow=True)
    snake.turn(Turn.right)
    snake.step(grow=True)
    return snake


def make_square_snake() -> Snake:
    # Body (tail -> head): (2,2) (2,3) (3,3) (3,2), heading left
    snake = Snake(START, Direction.right)
    snake.step(grow=True)
    snake.turn(Turn.right)
    snake.step(grow=True)
    snake.turn(Turn.right)
    snake.step(grow=True)
    return snake


# ====================  Start  ====================


def test_places_first_food_from_food_placer():
    sut = make_world(food_placer=ScriptedFoodPlacer(Cell(4, 4)))
    assert sut.initial_result.food == Cell(4, 4)


def test_first_food_is_chosen_from_free_cells_only():
    food_placer = ScriptedFoodPlacer(FAR_FOOD)
    make_world(food_placer=food_placer)
    free = food_placer.free_given[0]
    assert len(free) == 24
    assert START not in free


def test_initial_result_shows_starting_state():
    sut = make_world().initial_result
    assert sut.grid_cells == Grid(5, 5).get_cell_rows()
    assert sut.snake_cells == frozenset({START})
    assert sut.food == FAR_FOOD
    assert sut.head == START
    assert sut.tail == START
    assert sut.heading == Direction.right
    assert sut.last_turn == Turn.ahead
    assert not sut.just_ate
    assert not sut.is_over


def test_initial_result_does_not_change_after_a_step():
    sut = make_world()
    sut.step(Turn.ahead)
    assert sut.initial_result.head == START


# ====================  Step  ====================


def test_step_moves_the_snake():
    sut = make_world()
    result = sut.step(Turn.ahead)
    assert result.head == START + Direction.right
    assert result.snake_cells == frozenset({START + Direction.right})


def test_turn_changes_where_the_snake_goes():
    sut = make_world()
    result = sut.step(Turn.left)
    assert result.head == START + Direction.up
    assert result.heading == Direction.up
    assert result.last_turn == Turn.left


def test_result_reports_the_tail():
    sut = make_world(snake=make_long_snake())
    result = sut.step(Turn.left)  # down, away from the body
    assert result.tail == Cell(2, 2)


def test_head_may_move_into_cell_the_tail_leaves():
    sut = make_world(snake=make_square_snake())
    result = sut.step(Turn.right)  # up, into the tail's cell
    assert result.head == START


# ====================  Eat  ====================


def test_step_onto_food_grows_and_places_new_food():
    food = START + Direction.right
    food_placer = ScriptedFoodPlacer(food, FAR_FOOD)
    sut = make_world(food_placer=food_placer)
    result = sut.step(Turn.ahead)
    assert result.head == food
    assert len(result.snake_cells) == 2
    assert result.food == FAR_FOOD
    assert result.just_ate


def test_plain_step_does_not_eat():
    sut = make_world()
    assert not sut.step(Turn.ahead).just_ate


def test_new_food_is_chosen_from_free_cells_only():
    food = START + Direction.right
    food_placer = ScriptedFoodPlacer(food, FAR_FOOD)
    sut = make_world(food_placer=food_placer)
    sut.step(Turn.ahead)
    free = food_placer.free_given[1]
    assert len(free) == 23
    assert START not in free
    assert food not in free


# ====================  End  ====================


def test_hitting_the_wall_ends_the_game():
    sut = make_world(snake=Snake(Cell(2, 4), Direction.right))
    result = sut.step(Turn.ahead)
    assert result.end_cause == EndCause.crashed
    assert result.head == Cell(2, 4)


def test_hitting_the_body_ends_the_game():
    sut = make_world(snake=make_long_snake())
    result = sut.step(Turn.right)  # up, into (2,2)
    assert result.end_cause == EndCause.crashed


def test_crash_reports_the_turn_taken():
    sut = make_world(snake=make_long_snake())
    result = sut.step(Turn.right)  # up, into (2,2)
    assert result.last_turn == Turn.right
    assert result.heading == Direction.up
    assert not result.just_ate


def test_filling_the_grid_ends_the_game():
    food_placer = ScriptedFoodPlacer(Cell(0, 1), Cell(0, 2))
    sut = make_world(
        snake=Snake(Cell(0, 0), Direction.right),
        food_placer=food_placer,
        grid=Grid(1, 3),
    )
    assert not sut.step(Turn.ahead).is_over
    result = sut.step(Turn.ahead)
    assert result.end_cause == EndCause.won
    assert result.head == Cell(0, 2)
    assert result.food is None


def test_a_plain_step_has_no_end_cause():
    assert make_world().step(Turn.ahead).end_cause is None


def test_step_after_game_over_is_rejected():
    sut = make_world(snake=Snake(Cell(2, 4), Direction.right))
    sut.step(Turn.ahead)
    with pytest.raises(RuntimeError):
        sut.step(Turn.ahead)


# ====================  Length  ====================


def test_length_stays_the_same_without_food():
    sut = make_world()
    result = sut.step(Turn.ahead)
    assert result.snake_length == 1


def test_length_includes_the_final_step():
    food_placer = ScriptedFoodPlacer(Cell(0, 1), Cell(0, 2))
    sut = make_world(
        snake=Snake(Cell(0, 0), Direction.right),
        food_placer=food_placer,
        grid=Grid(1, 3),
    )
    sut.step(Turn.ahead)
    result = sut.step(Turn.ahead)  # eats the last free cell
    assert result.snake_length == 3


# ====================  Starve  ====================


def test_starves_on_reaching_the_unfed_step_limit():
    sut = make_world(unfed_step_limit=2)
    assert not sut.step(Turn.ahead).is_over
    assert sut.step(Turn.ahead).end_cause == EndCause.starved


def test_eating_resets_the_unfed_steps():
    food_placer = ScriptedFoodPlacer(Cell(2, 4), FAR_FOOD)
    sut = make_world(food_placer=food_placer, unfed_step_limit=2)
    sut.step(Turn.ahead)
    sut.step(Turn.ahead)  # eats at (2,4)
    assert not sut.step(Turn.left).is_over


def test_never_starves_without_a_limit():
    sut = make_world()
    for _ in range(8):  # circles in place
        assert not sut.step(Turn.left).is_over


def test_a_crash_wins_over_starving():
    sut = make_world(snake=Snake(Cell(2, 4), Direction.right), unfed_step_limit=1)
    assert sut.step(Turn.ahead).end_cause == EndCause.crashed
