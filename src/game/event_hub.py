from src.game.event import Event


class EventHub:
    stepped: Event
    ate: Event
    died: Event
    ready_to_draw: Event

    def __init__(self) -> None:
        self.stepped = Event()
        self.ate = Event()
        self.died = Event()
        self.ready_to_draw = Event()
