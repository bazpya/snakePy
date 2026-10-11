import dataclasses
import pytest
from snake.config import Config, GridConfig, TrainingConfig


# ====================  Structure  ====================


def test_settings_are_grouped_by_aspect():
    sut = Config()
    assert sut.grid.row_count > 0
    assert sut.display.cell_size > 0
    assert sut.training.game_count > 0
    assert sut.paths.brain_path.name == "brain.pt"


def test_brain_is_saved_in_the_models_folder_at_the_project_root():
    sut = Config()
    assert sut.paths.brain_path.parent.name == "models"
    assert (sut.paths.brain_path.parent.parent / "snake").is_dir()


def test_config_is_immutable():
    sut = Config()
    with pytest.raises(dataclasses.FrozenInstanceError):
        sut.grid.row_count = 5


def test_one_group_can_change_while_the_others_keep_their_defaults():
    sut = Config(grid=GridConfig(row_count=5, col_count=6))
    assert sut.grid.row_count == 5
    assert sut.training == TrainingConfig()


# ====================  Validation  ====================


def test_defaults_are_valid():
    Config()  # would raise if any default broke a rule


def test_discount_outside_zero_to_one_is_rejected():
    with pytest.raises(ValueError):
        TrainingConfig(discount=1.5)


def test_epsilon_out_of_order_is_rejected():
    # The minimum must not exceed the start, and the start must not exceed 1
    with pytest.raises(ValueError):
        TrainingConfig(start_epsilon=0.1, min_epsilon=0.5)
    with pytest.raises(ValueError):
        TrainingConfig(start_epsilon=1.5)


def test_decay_factor_outside_zero_to_one_is_rejected():
    with pytest.raises(ValueError):
        TrainingConfig(epsilon_decay_factor=1.2)


def test_starvation_factor_must_be_positive():
    with pytest.raises(ValueError):
        GridConfig(starvation_factor=0)
