import yaml


class Config:
    _file_content = None

    @staticmethod
    def _get() -> any:
        if Config._file_content is None:
            Config._file_content = yaml.safe_load(open("config.yaml"))
        return Config._file_content

    @staticmethod
    def get(path: str) -> any:
        obj = Config._get()
        segments = path.split(".")
        for seg in segments:
            obj = obj[seg]
        return obj
