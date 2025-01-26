# -*- coding: utf-8 -*-
import os
import shutil

from registest.utils.io_utils import load_json


class Parameters:
    def __init__(self, path: str):
        self.path = path
        self.dict = self.load_parameters()
        self.transform = self.dict["transform"]
        self.register = self.dict["register"]

    def load_parameters(self):
        # Check if the file exists
        if not os.path.exists(self.path):
            dest_path = save_parameters_template(os.path.dirname(self.path))
            raise FileNotFoundError(
                f"'parameters.json' file not found: {self.path}\nAn example is saved to help you: {dest_path}"
            )
        return load_json(self.path)


def save_parameters_template(input_dir):
    template_filepath = os.path.join(input_dir, "parameters_template.json")
    module_dir = os.path.dirname(__file__)
    source_filepath = os.path.join(module_dir, "default_params.json")
    return shutil.copyfile(source_filepath, template_filepath)
