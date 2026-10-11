# All settings in one place, grouped by aspect.
# Only the entry points read this; they pass plain values into constructors.
from dataclasses import dataclass, field
from pathlib import Path

_PROJECT_ROOT = Path(__file__).parent.parent


@dataclass(frozen=True)
class GridConfig:
    row_count: int = 10
    col_count: int = 10
    starvation_factor: float = 0.5  # ML games starve after this times the cell count of unfed steps

    def __post_init__(self) -> None:
        if self.starvation_factor <= 0:
            raise ValueError(f"starvation_factor must be positive, got {self.starvation_factor}")


@dataclass(frozen=True)
class DisplayConfig:
    cell_size: int = 24  # pixels
    tick_interval_ms: int = 120


@dataclass(frozen=True)
class TrainingConfig:
    game_count: int = 500
    memory_capacity: int = 50_000
    batch_size: int = 64
    discount: float = 0.9  # how much future reward counts
    learning_rate: float = 0.001
    start_epsilon: float = 1.0  # all random at first
    min_epsilon: float = 0.01
    epsilon_decay_factor: float = 0.99  # per game
    sync_interval_steps: int = 500
    report_interval_games: int = 25

    def __post_init__(self) -> None:
        if not 0 <= self.discount <= 1:
            raise ValueError(f"discount must be from 0 to 1, got {self.discount}")
        if not 0 <= self.min_epsilon <= self.start_epsilon <= 1:
            raise ValueError(
                f"epsilons must satisfy 0 <= min <= start <= 1, got min {self.min_epsilon}, start {self.start_epsilon}"
            )
        if not 0 < self.epsilon_decay_factor <= 1:
            raise ValueError(f"epsilon_decay_factor must be above 0 and at most 1, got {self.epsilon_decay_factor}")


@dataclass(frozen=True)
class PathConfig:
    brain_path: Path = _PROJECT_ROOT / "models" / "brain.pt"


@dataclass(frozen=True)
class Config:
    grid: GridConfig = field(default_factory=GridConfig)
    display: DisplayConfig = field(default_factory=DisplayConfig)
    training: TrainingConfig = field(default_factory=TrainingConfig)
    paths: PathConfig = field(default_factory=PathConfig)
