class Sight:
    def __init__(
        self,
        reciprocate_distances: bool = False,
        food_squarewise: bool = False,
        food_diagonal: bool = False,
        death_squarewise: bool = False,
        death_diagonal: bool = False,
    ) -> None:
        self._reciprocate_distances = reciprocate_distances
        self._food_squarewise = food_squarewise
        self._food_diagonal = food_diagonal
        self._death_squarewise = death_squarewise
        self._death_diagonal = death_diagonal
        self.size = 0
        self.size += 2 if food_squarewise else 0
        self.size += 1 if food_diagonal else 0
        self.size += 4 if death_squarewise else 0
        self.size += 4 if death_diagonal else 0
