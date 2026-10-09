from snake.ml.experience_source_concept import ExperienceSourceConcept
from snake.ml.learner_concept import LearnerConcept


class Teacher:
    # Teaches the learner from a batch of past experiences; targets come from a frozen copy
    # of the learner, refreshed by sync_target, so they don't shift on every lesson

    def __init__(
        self,
        learner: LearnerConcept,
        memory: ExperienceSourceConcept,
        batch_size: int,
        discount: float,  # how much future reward counts, from 0 to 1
    ) -> None:
        self._learner = learner
        self._memory = memory
        self._batch_size = batch_size
        self._discount = discount
        self._target = learner.copy()

    def teach(self) -> float | None:
        # Returns the loss, or None when the memory holds too few experiences
        if self._memory.size < self._batch_size:
            return None
        batch = self._memory.sample(self._batch_size)
        targets = [
            experience.reward if experience.is_over
            else experience.reward + self._discount * self._target.estimate(experience.next_state).best_estimate
            for experience in batch
        ]
        return self._learner.learn(
            [experience.state for experience in batch],
            [experience.turn for experience in batch],
            targets,
        )

    def sync_target(self) -> None:
        self._target = self._learner.copy()
