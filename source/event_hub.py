from source.event import Event


class EventHub:
    stepped: Event
    ate: Event
    died: Event

    def __init__(self) -> None:
        self.stepped = Event()
        self.ate = Event()
        self.died = Event()
