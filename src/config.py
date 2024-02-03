import yaml
from src.tree import Tree


class Config:
    _dict = None

    @staticmethod
    def _get() -> any:
        if Config._dict is None:
            Config._dict = yaml.safe_load(open("config.yaml"))
        return Config._dict

    @staticmethod
    def get() -> any:
        obj = Config._get()
        return Tree(obj)

    @staticmethod
    def parse_ints(string: str) -> any:
        return [int(x) for x in string.split(",")]
