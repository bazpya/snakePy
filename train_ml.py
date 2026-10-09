# ML training: many headless games, no window; saves the brain's weights at the end
from pathlib import Path
from snake.core import Factory, Game, ObserverConcept, StepResult
from snake.ml import Brain, ExploringPlayer, Eye, MLPlayer, Recorder, ReplayMemory, Rewarder, Stats, Teacher

ROW_COUNT = 10
COL_COUNT = 10
STARVATION_FACTOR = 0.5  # starves after half the grid's cell count of steps without food
GAME_COUNT = 500
MEMORY_CAPACITY = 50_000
BATCH_SIZE = 64
DISCOUNT = 0.9
LEARNING_RATE = 0.001
START_EPSILON = 1.0  # all random at first
MIN_EPSILON = 0.01
EPSILON_DECAY_FACTOR = 0.99  # per game
SYNC_INTERVAL_STEPS = 500
REPORT_INTERVAL_GAMES = 25
BRAIN_PATH = Path(__file__).parent / "models" / "brain.pt"


class LastResult(ObserverConcept):
    # Keeps the latest result, to report how each game ended
    def __init__(self) -> None:
        self.result: StepResult | None = None

    def on_started(self, result: StepResult) -> None:
        self.result = result

    def on_stepped(self, result: StepResult) -> None:
        self.result = result


def main() -> None:
    factory = Factory(ROW_COUNT, COL_COUNT, starvation_factor=STARVATION_FACTOR)
    eye = Eye()
    brain = Brain(input_count=eye.output_count, learning_rate=LEARNING_RATE)
    memory = ReplayMemory(MEMORY_CAPACITY)
    recorder = Recorder(eye, Rewarder(), memory)
    stats = Stats()
    last_result = LastResult()
    player = ExploringPlayer(MLPlayer(eye, brain), START_EPSILON, MIN_EPSILON, EPSILON_DECAY_FACTOR)
    teacher = Teacher(brain, memory, BATCH_SIZE, DISCOUNT)

    total_step_count = 0
    report_lengths: list[int] = []
    for game_number in range(1, GAME_COUNT + 1):
        game = Game(factory.create(), player, observers=[recorder, stats, last_result])
        game.start()
        while not game.is_over():
            game.tick()
            teacher.teach()
            total_step_count += 1
            if total_step_count % SYNC_INTERVAL_STEPS == 0:
                teacher.sync_target()
        player.decay_epsilon()

        report_lengths.append(last_result.result.snake_length)
        if game_number % REPORT_INTERVAL_GAMES == 0:
            average_length = sum(report_lengths) / len(report_lengths)
            print(
                f"game {game_number}: average length {average_length:.1f}, "
                f"best {max(report_lengths)}, last steps {stats.taken_step_count}, "
                f"epsilon {player.epsilon:.3f}"
            )
            report_lengths.clear()

    BRAIN_PATH.parent.mkdir(exist_ok=True)
    brain.save(BRAIN_PATH)
    print(f"saved {BRAIN_PATH}")


if __name__ == "__main__":
    main()
