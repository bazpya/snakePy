import tensorflow as tf
from src.game.direction import Direction
from src.ml.sight import Sight
from src.game.cell import Cell


class Eye:
    def __init__(self, sight: Sight) -> None:
        self._sight = sight
        self._recip = sight._reciprocate_distances

    def see(self, head: Cell, food: Cell) -> tf:
        signals = []

        # Food

        (food_ver, food_hor, food_diag) = head.get_distance(self._recip, food)

        if self._sight._food_squarewise:
            signals.extend(food_ver, food_hor)

        if self._sight._food_diagonal:
            signals.append(food_diag)

        # Death squarewise

        (*etc, death_up) = head.death_distance(self._recip, Direction.up)
        (*etc, death_down) = head.death_distance(self._recip, Direction.down)
        (*etc, death_left) = head.death_distance(self._recip, Direction.left)
        (*etc, death_right) = head.death_distance(self._recip, Direction.right)

        if self._sight._death_squarewise:
            signals.extend(death_up, death_down, death_left, death_right)

        # Death diagonal

        (*etc, death_up_right) = head.death_distance(
            self._recip, Direction.up, Direction.right
        )
        (*etc, death_up_left) = head.death_distance(
            self._recip, Direction.up, Direction.left
        )
        (*etc, death_down_right) = head.death_distance(
            self._recip, Direction.down, Direction.right
        )
        (*etc, death_down_left) = head.death_distance(
            self._recip, Direction.down, Direction.left
        )

        if self._sight._death_diagonal:
            signals.extend(
                [death_up_left, death_up_right, death_down_left, death_down_right]
            )

        res = tf.convert_to_tensor(signals)
        return res
