import random
from tests.test_ import Test_
from src.game.cell import CellType
from src.game.direction import Direction
from tests.game.helper.cell_factory import CellFactory


class Cell_factory_(Test_):
    _map = {
        "b": CellType.blank,
        "f": CellType.food,
        "s": CellType.snake,
        "w": CellType.wall,
    }

    # ======================  Make List  ======================

    def test_make_list_gets_right_number_of_cells(self):
        res = CellFactory._make_list("bfsw")
        self.assertEqual(len(res), 4)

    def test_make_list_gets_right_type_of_cells(self):
        res = CellFactory._make_list("bfsw")
        self.assertEqual(res[0].type, CellType.blank)
        self.assertEqual(res[1].type, CellType.food)
        self.assertEqual(res[2].type, CellType.snake)
        self.assertEqual(res[3].type, CellType.wall)

    # ======================  Link  ======================

    def test_link_works(self):
        cells = CellFactory._make_list("bfswbfswbfsw")
        origin = CellFactory._link(cells)
        for i, cell in enumerate(cells[:-1]):
            next = cells[i + 1]
            self.assertEqual(cell.get_neighbour(Direction.any()), next)

    # ======================  Make Chain  ======================

    def test_make_chain_single_cells(self):
        for key, val in self._map.items():
            origin, *etc = CellFactory.make(key)
            self.assertEqual(origin.type, val)

    def test_make_chain_multi(self):
        pattern = "bfswbbfsw"
        types = [
            CellType.blank,
            CellType.food,
            CellType.snake,
            CellType.wall,
            CellType.blank,
            CellType.blank,
            CellType.food,
            CellType.snake,
            CellType.wall,
        ]
        runner, *etc = CellFactory.make(pattern)
        for type in types:
            self.assertEqual(runner.type, type)
            runner = runner.get_neighbour(random.choice(list(Direction)))

    def test_make_chain_makes_correct_length(self):
        pattern = "bfswbbfsw"
        runner, *etc = CellFactory.make(pattern)
        length = 1
        while runner.get_neighbour(random.choice(list(Direction))) is not None:
            length += 1
            runner = runner.get_neighbour(random.choice(list(Direction)))
        self.assertEqual(length, len(pattern))

    # ======================  Make Infinite Chain  ======================

    def test_make_infinite_chain_creates_blank_chain(self):
        runner = CellFactory.make_infinite_chain()
        for i in range(self.many):
            self.assertEqual(runner.type, CellType.blank)
            runner = runner.get_neighbour(Direction.any())

    def test_make_infinite_chain_makes_correct_cell_type(self):
        type = CellType.food
        runner = CellFactory.make_infinite_chain(type=type)
        for i in range(self.many):
            self.assertEqual(runner.type, type)
            runner = runner.get_neighbour(Direction.any())
