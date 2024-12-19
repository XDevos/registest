#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from registest.config.parameters import Parameters
from registest.core.data_manager import DataManager
from registest.modules.transformation import Transform


class Pipeline:
    def __init__(self, datam: DataManager, params: Parameters):
        self.datam = datam
        self.params = params
        self.ref = self.datam.ref.data
        self.target_nbr = self.get_target_nbr()

    def get_target_nbr(self):
        return len(self.params.prepare["shifts"])

    def run(self):
        self.prepare()
        # self.register()
        # self.compare()

    def prepare(self):
        transform_mod = Transform(self.params.prepare)
        for i in range(self.target_nbr):
            transformed_img = transform_mod.execute(self.ref, i)
            self.datam.save_tif(
                data=transformed_img, folder="Preparation", name=f"target_{i}"
            )
