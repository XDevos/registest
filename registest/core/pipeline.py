#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from tqdm import tqdm, trange

from registest.config.parameters import Parameters
from registest.core.data_manager import DataManager, get_tif_filepaths
from registest.modules.registration import phase_cross_correlation_wrapper
from registest.modules.reporting import generate_similarity_report
from registest.modules.transformation import Transform, shift_3d_array_subpixel
from registest.utils.io_utils import load_tiff, save_json
from registest.utils.visualization import visu_rgb_slice


class Pipeline:
    def __init__(self, datam: DataManager, params: Parameters, raw_cmd_list: str):
        self.datam = datam
        self.params = params
        self.ref = self.datam.ref.data
        self.target_nbr = self.get_target_nbr()
        self.default_cmds = ["prepare", "register", "compare"]
        self.commands = self.decode_cmd_list(raw_cmd_list)

    def decode_cmd_list(self, raw_cmd_list: str):
        commands = raw_cmd_list.split(",")
        for cmd in commands:
            if cmd not in self.default_cmds:
                raise ValueError(
                    f"This command doesn't exist: {cmd}. See default list: {self.default_cmds }"
                )
        sorted_cmds = []
        for cmd in self.default_cmds:
            if cmd in commands:
                sorted_cmds.append(cmd)
        return sorted_cmds

    def get_target_nbr(self):
        return len(self.params.prepare["shifts"])

    def run(self):
        print(f"Reference image: {self.datam.ref.path}")
        if "prepare" in self.commands:
            print("[Preparation]")
            self.prepare()
        if "register" in self.commands:
            print("[Registration]")
            self.register()
        if "compare" in self.commands:
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
        target_paths = get_tif_filepaths(self.datam.out_folder.prepa)
        for targ_path in tqdm(target_paths):
            for reg_method in self.params.register["method"]:

                target = load_tiff(targ_path)
                shift_3d = list(phase_cross_correlation_wrapper(self.ref, target))
                basename = os.path.basename(targ_path)
                shifts_found[basename] = shift_3d
                shifted_target = shift_3d_array_subpixel(target, shift_3d)
                self.datam.save_tif(
                    data=shifted_target,
                    folder="Registration",
                    name=os.path.join(reg_method, f"shifted_{basename}"),
                )

        path = os.path.join(self.datam.out_folder.regis, "shifts_found.json")
        save_json(shifts_found, path)

    def compare(self):
        output_csv = os.path.join(self.datam.out_folder.comp, "similarity_report.csv")
        generate_similarity_report(self.ref, self.datam.out_folder.regis, output_csv)
        method_folder_names = self.params.register["method"]
        self.datam.make_method_folders(self.datam.out_folder.comp, method_folder_names)
        for fold_name in method_folder_names:
            shifted_target_paths = get_tif_filepaths(
                self.datam.out_folder.regis + os.sep + fold_name
            )
            for targ_path in shifted_target_paths:
                basename = os.path.basename(targ_path)
                print(f"Target: {fold_name}/{basename}")
                target = load_tiff(targ_path)
                comp_method_path = (
                    self.datam.out_folder.comp + os.sep + fold_name + os.sep
                )
                visu_rgb_slice(
                    self.ref, target, comp_method_path + "ref_VS_" + basename
                )
