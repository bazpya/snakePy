class Anonym:
    def __init__(self, **attributes) -> None:
        self.__dict__.update(attributes)


stuff = Anonym(prop1=1, prop2="two", prop3=[1, 2, 3], prop4=False)
