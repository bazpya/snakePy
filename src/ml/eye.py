import tensorflow as tf
from src.ml.sight import Sight
from src.game.game import Game
from src.game.cell import Cell


class Eye:
    def __init__(self, game: Game, sight: Sight) -> None:
        self._game = game
        self._sight = sight

    def see(self):
        # inputTensor = tf.Tensor(range(0, 8), [1, self._inputSize])
        inputTensor = tf.constant(range(0, self._sight.size))
        return inputTensor

    # #getInput() {
    #     let result = [];
    #     const foodDiffHor = The.grid.food.col - this.#head.col;
    #     const foodDiffVer = The.grid.food.row - this.#head.row;
    #     const foodSignalHor = foodDiffHor === 0 ? 0 : 1 / foodDiffHor;
    #     result.push(foodSignalHor);
    #     const foodSignalVer = foodDiffVer === 0 ? 0 : 1 / foodDiffVer;
    #     result.push(foodSignalVer);

    #     let deathVector = this.#head.getDiff(c => c.isDeadly, Direction.up);
    #     const deathSignalUp = - 1 / BazMath.amplitude(deathVector);
    #     result.push(deathSignalUp);

    #     deathVector = this.#head.getDiff(c => c.isDeadly, Direction.up, Direction.right);
    #     const deathSignalUpRight = - 1 / BazMath.amplitude(deathVector);
    #     result.push(deathSignalUpRight);

    #     deathVector = this.#head.getDiff(c => c.isDeadly, Direction.right);
    #     const deathSignalRight = - 1 / BazMath.amplitude(deathVector);
    #     result.push(deathSignalRight);

    #     deathVector = this.#head.getDiff(c => c.isDeadly, Direction.right, Direction.down);
    #     const deathSignalDownRight = - 1 / BazMath.amplitude(deathVector);
    #     result.push(deathSignalDownRight);

    #     deathVector = this.#head.getDiff(c => c.isDeadly, Direction.down);
    #     const deathSignalDown = - 1 / BazMath.amplitude(deathVector);
    #     result.push(deathSignalDown);

    #     deathVector = this.#head.getDiff(c => c.isDeadly, Direction.down, Direction.left);
    #     const deathSignalDownLeft = - 1 / BazMath.amplitude(deathVector);
    #     result.push(deathSignalDownLeft);

    #     deathVector = this.#head.getDiff(c => c.isDeadly, Direction.left);
    #     const deathSignalLeft = - 1 / BazMath.amplitude(deathVector);
    #     result.push(deathSignalLeft);

    #     deathVector = this.#head.getDiff(c => c.isDeadly, Direction.left, Direction.up);
    #     const deathSignalUpLeft = - 1 / BazMath.amplitude(deathVector);
    #     result.push(deathSignalUpLeft);

    #     return result;
    # }
