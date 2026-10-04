from snake.core import Cell, Direction, StepResult
from snake.ui.colour import Colour
from snake.ui.drawer import Drawer

# 3x3 board
CELL_ROWS = tuple(tuple(Cell(r, c) for c in range(3)) for r in range(3))


class FakeCanvas:
    # Records what the Drawer asked for, instead of drawing
    def __init__(self) -> None:
        self.colours: dict[Cell, str] = {}
        self.filled: list[Cell] = []
        self.messages: list[str] = []

    def fill(self, cell: Cell, colour: str) -> None:
        self.colours[cell] = colour
        self.filled.append(cell)

    def show_message(self, text: str) -> None:
        self.messages.append(text)


def make_result(snake_cells, head, food=Cell(0, 0), is_over=False) -> StepResult:
    return StepResult(
        is_over=is_over,
        cell_rows=CELL_ROWS,
        snake_cells=frozenset(snake_cells),
        head=head,
        direction=Direction.right,
        food=food,
    )


# Snake (1,0) -> head (1,1), food at (0,0)
START = make_result({Cell(1, 0), Cell(1, 1)}, head=Cell(1, 1))


def make_started_drawer() -> tuple[Drawer, FakeCanvas]:
    canvas = FakeCanvas()
    sut = Drawer(canvas)
    sut.on_started(START)
    canvas.filled.clear()
    return sut, canvas


# ====================  Start  ====================


def test_start_fills_every_cell():
    canvas = FakeCanvas()
    Drawer(canvas).on_started(START)
    assert set(canvas.colours) == {cell for row in CELL_ROWS for cell in row}


def test_start_colours_each_cell_by_what_is_on_it():
    canvas = FakeCanvas()
    Drawer(canvas).on_started(START)
    assert canvas.colours[Cell(1, 1)] == Colour.head
    assert canvas.colours[Cell(1, 0)] == Colour.body
    assert canvas.colours[Cell(0, 0)] == Colour.food
    assert canvas.colours[Cell(2, 2)] == Colour.empty


def test_start_shows_no_message():
    canvas = FakeCanvas()
    Drawer(canvas).on_started(START)
    assert canvas.messages == []


# ====================  Step  ====================


def test_step_recolours_only_cells_that_changed():
    sut, canvas = make_started_drawer()
    sut.on_stepped(make_result({Cell(1, 1), Cell(1, 2)}, head=Cell(1, 2)))
    assert set(canvas.filled) == {Cell(1, 0), Cell(1, 1), Cell(1, 2)}
    assert canvas.colours[Cell(1, 0)] == Colour.empty
    assert canvas.colours[Cell(1, 1)] == Colour.body
    assert canvas.colours[Cell(1, 2)] == Colour.head


def test_step_recolours_food_that_moved():
    canvas = FakeCanvas()
    sut = Drawer(canvas)
    # Head moves up onto the food at (0,1); new food appears at (2,2)
    sut.on_started(make_result({Cell(1, 1)}, head=Cell(1, 1), food=Cell(0, 1)))
    canvas.filled.clear()
    sut.on_stepped(make_result({Cell(1, 1), Cell(0, 1)}, head=Cell(0, 1), food=Cell(2, 2)))
    assert canvas.colours[Cell(0, 1)] == Colour.head
    assert canvas.colours[Cell(1, 1)] == Colour.body
    assert canvas.colours[Cell(2, 2)] == Colour.food


def test_step_without_change_recolours_nothing():
    sut, canvas = make_started_drawer()
    sut.on_stepped(make_result({Cell(1, 0), Cell(1, 1)}, head=Cell(1, 1), is_over=True))
    assert canvas.filled == []


def test_step_handles_missing_food():
    # e.g. the board is filled
    sut, canvas = make_started_drawer()
    sut.on_stepped(make_result({Cell(1, 0), Cell(1, 1)}, head=Cell(1, 1), food=None))
    assert canvas.colours[Cell(0, 0)] == Colour.empty


# ====================  Over  ====================


def test_shows_a_message_when_the_game_is_over():
    sut, canvas = make_started_drawer()
    sut.on_stepped(make_result({Cell(1, 0), Cell(1, 1)}, head=Cell(1, 1), is_over=True))
    assert len(canvas.messages) == 1


def test_shows_no_message_while_the_game_goes_on():
    sut, canvas = make_started_drawer()
    sut.on_stepped(make_result({Cell(1, 1), Cell(1, 2)}, head=Cell(1, 2)))
    assert canvas.messages == []
