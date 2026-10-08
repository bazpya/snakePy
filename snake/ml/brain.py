import torch
from torch import nn
from snake.ml.brain_concept import BrainConcept
from snake.ml.turn_scores import TurnScores


class Brain(BrainConcept):
    # A small neural network: state in, a score (Q-value) for each turn out
    _hidden_count = 64

    def __init__(self, input_count: int) -> None:
        self._input_count = input_count
        self._model = nn.Sequential(
            nn.Linear(input_count, self._hidden_count),
            nn.ReLU(),
            nn.Linear(self._hidden_count, 3),  # left, ahead, right
        )

    def score(self, state: list[float]) -> TurnScores:
        if len(state) != self._input_count:
            raise ValueError(f"Expected {self._input_count} inputs, got {len(state)}")
        with torch.no_grad():  # scoring only; no learning here
            left, ahead, right = self._model(torch.tensor(state, dtype=torch.float32)).tolist()
        return TurnScores(left=left, ahead=ahead, right=right)
