from pathlib import Path
import torch
from torch import nn
from snake.core import Turn
from snake.ml.brain_concept import BrainConcept
from snake.ml.learner_concept import LearnerConcept
from snake.ml.turn_estimates import TurnEstimates


class Brain(BrainConcept, LearnerConcept):
    # A small neural network: state in, an estimate (Q-value) for each turn out
    _hidden_count = 64

    def __init__(self, input_count: int, learning_rate: float = 0.001) -> None:
        self._input_count = input_count
        self._learning_rate = learning_rate
        self._model = nn.Sequential(
            nn.Linear(input_count, self._hidden_count),
            nn.ReLU(),
            nn.Linear(self._hidden_count, 3),  # left, ahead, right
        )
        self._optimizer = torch.optim.Adam(self._model.parameters(), lr=learning_rate)

    def estimate(self, state: list[float]) -> TurnEstimates:
        if len(state) != self._input_count:
            raise ValueError(f"Expected {self._input_count} inputs, got {len(state)}")
        with torch.no_grad():  # estimating only; no learning here
            left, ahead, right = self._model(torch.tensor(state, dtype=torch.float32)).tolist()
        return TurnEstimates(left=left, ahead=ahead, right=right)

    def learn(self, states: list[list[float]], turns: list[Turn], targets: list[float]) -> float:
        # One learning step: pulls each chosen turn's estimate towards its target; returns the loss
        if not len(states) == len(turns) == len(targets):
            raise ValueError("states, turns and targets must have the same length")
        estimates = self._model(torch.tensor(states, dtype=torch.float32))
        columns = torch.tensor([[_turn_columns[turn]] for turn in turns])
        chosen = estimates.gather(1, columns).squeeze(1)
        loss = nn.functional.mse_loss(chosen, torch.tensor(targets, dtype=torch.float32))
        self._optimizer.zero_grad()
        loss.backward()
        self._optimizer.step()
        return loss.item()

    def save(self, path: str | Path) -> None:
        # Weights only; the learning progress of the optimizer is not kept
        torch.save(self._model.state_dict(), path)

    def load(self, path: str | Path) -> None:
        try:
            self._model.load_state_dict(torch.load(path, weights_only=True))
        except RuntimeError as error:  # torch's way of saying the sizes don't match
            raise ValueError(f"{path} does not fit a brain with {self._input_count} inputs") from error

    def copy(self) -> "Brain":
        # Same weights, trained separately from now on
        brain = Brain(self._input_count, self._learning_rate)
        brain._model.load_state_dict(self._model.state_dict())
        return brain


_turn_columns = {Turn.left: 0, Turn.ahead: 1, Turn.right: 2}
