#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from tqdm import tqdm, trange

from registest.config.parameters import Parameters
from registest.core.data_manager import DataManager
from registest.modules.registration import phase_cross_correlation_wrapper
from registest.modules.transformation import Transform, shift_3d_array_subpixel
from registest.utils.io_utils import load_tiff, save_json


class Pipeline:
    def __init__(self, datam: DataManager, params: Parameters):
        self.datam = datam
        self.params = params
        self.ref = self.datam.ref.data
        self.target_nbr = self.get_target_nbr()

    def get_target_nbr(self):
        return len(self.params.prepare["shifts"])

    def run(self):
        print("[Preparation]")
        self.prepare()
        print("[Registration]")
        self.register()
        print("[Comparison]")
        self.compare()

    def prepare(self):
        transform_mod = Transform(self.params.prepare)
        for i in trange(self.target_nbr):
            transformed_img = transform_mod.execute(self.ref, i)
            self.datam.save_tif(
                data=transformed_img, folder="Preparation", name=f"target_{i}"
            )
        transform_mod.save_shifts_used(self.datam.out_folder.prepa)

    def register(self):
        shifts_found = {}
        target_paths = self.datam.get_prepa_img_paths()
        for targ_path in tqdm(target_paths):
            target = load_tiff(targ_path)
            shift_3d = list(phase_cross_correlation_wrapper(self.ref, target))
            basename = os.path.basename(targ_path)
            shifts_found[basename] = shift_3d
            shifted_target = shift_3d_array_subpixel(target, shift_3d)
            self.datam.save_tif(
                data=shifted_target, folder="Registration", name=f"shifted_{basename}"
            )

        path = os.path.join(self.datam.out_folder.regis, "shifts_found.json")
        save_json(shifts_found, path)

    def compare(self):
        pass
