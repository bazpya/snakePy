from src.config import Config


class View:
    def __init__(
        self,
        reciprocate_distances: bool = False,
        food_squarewise: bool = False,
        food_diagonal: bool = False,
        death_squarewise: bool = False,
        death_diagonal: bool = False,
    ) -> None:
        self._reciprocate_distances = reciprocate_distances
        self.size = 0
        self._food_squarewise = food_squarewise
        self.size += 2 if food_squarewise else 0
        self._food_diagonal = food_diagonal
        self.size += 1 if food_diagonal else 0
        self._death_squarewise = death_squarewise
        self.size += 4 if death_squarewise else 0
        self._death_diagonal = death_diagonal
        self.size += 4 if death_diagonal else 0

    def get():
        config = Config.get()
        return View(
            reciprocate_distances=config.ml.grid_view.reciprocate_distances,
            food_squarewise=config.ml.grid_view.food_squarewise,
            food_diagonal=config.ml.grid_view.food_diagonal,
            death_squarewise=config.ml.grid_view.death_squarewise,
            death_diagonal=config.ml.grid_view.death_diagonal,
        )
