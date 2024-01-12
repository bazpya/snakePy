from src.game.cell import CellType, Cell
from src.game.direction import Direction
from src.game_test.cell_ import Cell_


class Cell_neighbours_(Cell_):
    def test_neighbour_setter_sets(self):
        sut = Cell(None, None, CellType.snake)
        neighbour = Cell(None, None, CellType.food)
        sut.set_neighbour(Direction.right, neighbour)
        self.assertEqual(neighbour, sut.get_neighbour(Direction.right))
