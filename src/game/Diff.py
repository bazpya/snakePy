from src.game.cell import Cell


class SnakeDiff:
    def __init__(self) -> None:
        self.blanks: list[Cell] = []
        self.snakes: list[Cell] = []

    def add_blank(self, cell: Cell):
        self.blanks.append(cell)

    def add_snake(self, cell: Cell):
        self.snakes.append(cell)


class GameDiff:
    def __init__(self) -> None:
        self.blanks: list[Cell] = []
        self.snakes: list[Cell] = []
        self.foods: list[Cell] = []

    def add(self, snake_diff: SnakeDiff):
        self.blanks.extend(snake_diff.blanks)
        self.snakes.extend(snake_diff.snakes)

    def add_food(self, cell):
        self.foods.append(cell)

    def flatten(self) -> list[Cell]:
        return (self.blanks, self.snakes, self.foods)
