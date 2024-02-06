import yaml
from src.tree import Tree


class Config:
    _dict = None
    _tree = None

    @staticmethod
    def get() -> Tree:
        if Config._tree is None:
            _dict = yaml.safe_load(open("config.yaml"))
            tree = Tree(_dict)
            Config._tree = tree
        return Config._tree

    @staticmethod
    def parse_ints(string: str) -> any:
        return [int(x) for x in string.split(",")]


config = Config.get()
