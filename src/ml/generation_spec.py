import math
from src.config import config
from src.ml.view import View


class GenerationSpec:
    def __init__(
        self,
        population: int,
        selection_count: int,
        row_count: int,
        col_count: int,
        max_steps: int,
        fake_player: bool,
        view: View,
        use_ui: bool,
        cell_size: int,
        interval: float,
    ) -> None:
        self.population = population
        self.selection_count = selection_count
        self.row_count = row_count
        self.col_count = col_count
        self.max_steps = max_steps
        self.fake_player = fake_player
        self.view = view
        self.use_ui = use_ui
        self.cell_size = cell_size
        self.interval = interval

    def get():
        population = config.ml.generation.population
        selection_ratio = config.ml.evolution.selection_ratio

        return GenerationSpec(
            population,
            math.floor(population * selection_ratio),
            config.game.row_count,
            config.game.col_count,
            config.ml.player.max_steps,
            config.ml.player.fake,
            View.get(),
            config.game.use_ui,
            config.game.cell_size,
            config.game.interval,
        )
