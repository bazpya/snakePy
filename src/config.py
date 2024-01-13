import yaml


class Config:
    _instance = None

    @staticmethod
    def _get():
        if Config._instance is None:
            Config._instance = yaml.safe_load(open("config.yaml"))
        return Config._instance

    @staticmethod
    def get(path: str):
        obj = Config._get()
        segments = path.split(".")
        for seg in segments:
            obj = obj[seg]
        return obj
