# -*- coding: utf-8 -*-
import os

from registest.utils.io_utils import load_json


class Parameters:
    def __init__(self, path: str):
        self.path = path
        self.dict = self.load_parameters()
        self.prepare = self.dict["prepare"]
        self.register = self.dict["register"]

    def load_parameters(self):
        # Check if the file exists
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"'parameters.json' file not found: {self.path}")
        return load_json(self.path)
