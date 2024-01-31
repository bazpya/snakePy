from src.game.cell import Cell


class SnakeDiff:
    def __init__(self) -> None:
        self.blank: Cell = None
        self.snake: Cell = None

    def set_blank(self, cell: Cell):
        if self.blank:
            raise ValueError("Diff already has a Blank cell")
        self.blank = cell

    def set_snake(self, cell: Cell):
        if self.snake:
            raise ValueError("Diff already has a Snake cell")
        self.snake = cell


class GameDiff(SnakeDiff):
    def __init__(self) -> None:
        self.blank: Cell = None
        self.snake: Cell = None
        self.food: Cell = None

    def add(self, snake_diff: SnakeDiff):
        self.set_blank(snake_diff.blank)
        self.set_snake(snake_diff.snake)

    def set_food(self, cell):
        if self.food:
            raise ValueError("Diff already has a Food cell")
        self.food = cell

    def flatten(self) -> list[Cell]:
        res = []
        if self.blank:
            res.append(self.blank)
        if self.snake:
            res.append(self.snake)
        if self.food:
            res.append(self.food)
        return res
