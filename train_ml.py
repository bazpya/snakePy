# ML training: many headless games, no window; saves the brain's weights at the end
from snake.config import Config
from snake.core import Factory, Game, ObserverConcept, WorldState
from snake.ml import Brain, ExploringPlayer, Eye, MLPlayer, Recorder, ReplayMemory, Rewarder, Stats, Teacher


class LastState(ObserverConcept):
    # Keeps the latest state, to report how each game ended
    def __init__(self) -> None:
        self.state: WorldState | None = None

    def on_started(self, state: WorldState) -> None:
        self.state = state

    def on_stepped(self, state: WorldState) -> None:
        self.state = state


def main() -> None:
    config = Config()
    grid, training, brain_path = config.grid, config.training, config.paths.brain_path
    factory = Factory(grid.row_count, grid.col_count, starvation_factor=grid.starvation_factor)
    eye = Eye()
    brain = Brain(input_count=eye.output_count, learning_rate=training.learning_rate)
    memory = ReplayMemory(training.memory_capacity)
    recorder = Recorder(eye, Rewarder(), memory)
    stats = Stats()
    last_state = LastState()
    player = ExploringPlayer(
        MLPlayer(eye, brain), training.start_epsilon, training.min_epsilon, training.epsilon_decay_factor
    )
    teacher = Teacher(brain, memory, training.batch_size, training.discount)

    total_step_count = 0
    report_lengths: list[int] = []
    for game_number in range(1, training.game_count + 1):
        game = Game(factory.create(), player, observers=[recorder, stats, last_state])
        game.start()
        while not game.is_over():
            game.tick()
            teacher.teach()
            total_step_count += 1
            if total_step_count % training.sync_interval_steps == 0:
                teacher.sync_target()
        player.decay_epsilon()

        report_lengths.append(last_state.state.snake_length)
        if game_number % training.report_interval_games == 0:
            average_length = sum(report_lengths) / len(report_lengths)
            print(
                f"game {game_number}: average length {average_length:.1f}, "
                f"best {max(report_lengths)}, last steps {stats.taken_step_count}, "
                f"epsilon {player.epsilon:.3f}"
            )
            report_lengths.clear()

    brain_path.parent.mkdir(exist_ok=True)
    brain.save(brain_path)
    print(f"saved {brain_path}")


if __name__ == "__main__":
    main()
