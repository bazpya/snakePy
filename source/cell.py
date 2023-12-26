from source.global_refs import CellType, Direction


class CellConcept:
    def set_type(self, type: CellType):
        self.__type__ = type

    def be_blank(self) -> None:
        self.set_type(CellType.blank)

    def be_wall(self) -> None:
        self.set_type(CellType.wall)

    def be_worm(self) -> None:
        self.set_type(CellType.worm)

    def be_food(self) -> None:
        self.set_type(CellType.food)

    def get_neighbour(self, direction: Direction) -> "Cell":
        pass


class Cell(CellConcept):
    def __init__(self, type: CellType = CellType.blank):
        self.__type__ = type
        self.__type__: CellType
        self.__neighbours__ = {
            Direction.up: None,
            Direction.right: None,
            Direction.down: None,
            Direction.left: None,
        }

    def get_type(self) -> CellType:
        return self.__type__

    def is_blank(self) -> bool:
        return self.get_type() == CellType.blank

    def is_wall(self) -> bool:
        return self.get_type() == CellType.wall

    def is_worm(self) -> bool:
        return self.get_type() == CellType.worm

    def is_food(self) -> bool:
        return self.get_type() == CellType.food

    def set_neighbour(self, direction: Direction, neighbour: "Cell") -> None:
        self.__neighbours__[direction] = neighbour

    def get_neighbour(self, direction: Direction) -> "Cell":
        return self.__neighbours__[direction]
