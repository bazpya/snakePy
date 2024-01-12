from configparser import ConfigParser


class Config:
    filePath: str

    def __init__(self, filePath):
        self.filePath = filePath
        self.parser = ConfigParser()
        self.parser.read(filePath)

    def get_section(self, section):
        res = {}
        if self.parser.has_section(section):
            for param in self.parser.items(section):
                res[param[0]] = param[1]
        else:
            raise Exception(
                f'Section {section} not found in config file {self.filePath}')
        return res
