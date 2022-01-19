import json


class Configuration:
    def __init__(self):
        self.config = dict()

    def read_config(self):
        with open('config.json') as json_file:
            self.config = json.load(json_file)

    def get_config(self):
        return self.config
