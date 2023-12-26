from source.global_refs import CellType, Direction


class CellConcept:
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

    # ====================  Type Setters  ====================

    def set_type(self, type: CellType):
        self.__type__ = type

    def be_blank(self) -> None:
        self.__type__ = CellType.blank

    def be_wall(self) -> None:
        self.__type__ = CellType.wall

    def be_worm(self) -> None:
        self.__type__ = CellType.worm

    def be_food(self) -> None:
        self.__type__ = CellType.food

    # ====================  Type Getters  ====================

    def get_type(self) -> CellType:
        return self.__type__

    def is_blank(self) -> bool:
        return self.__type__ == CellType.blank

    def is_wall(self) -> bool:
        return self.__type__ == CellType.wall

    def is_worm(self) -> bool:
        return self.__type__ == CellType.worm

    def is_food(self) -> bool:
        return self.__type__ == CellType.food

    # ====================  Neighbours  ====================

    def set_neighbour(self, direction: Direction, neighbour: "Cell") -> None:
        self.__neighbours__[direction] = neighbour

    def get_neighbour(self, direction: Direction) -> "Cell":
        return self.__neighbours__[direction]
