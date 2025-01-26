#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from tqdm import tqdm

from registest.config.parameters import Parameters
from registest.core.data_manager import (
    DataManager,
    get_target_paths,
    get_tif_filepaths,
    remove_ext,
)
from registest.modules.registration import Register
from registest.modules.reporting import generate_similarity_report
from registest.modules.transformation import Transform
from registest.utils.io_utils import load_tiff
from registest.utils.visualization import visu_rgb_slice


class Pipeline:
    def __init__(self, datam: DataManager, params: Parameters, raw_cmd_list: str):
        self.datam = datam
        self.params = params
        self.ref = self.datam.ref_list[0]
        self.default_cmds = ["transform", "register", "compare"]
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

    def run(self):

        if "transform" in self.commands:
            print("\n[Transformation]")
            for ref in self.datam.ref_list:
                self.ref = ref
                print(f"Reference image: {self.ref.path}")
                self.transform()
        if "register" in self.commands:
            print("\n[Registration]")
            for ref in self.datam.ref_list:
                self.ref = ref
                print(f"Reference image: {self.ref.path}")
                self.register()
        if "compare" in self.commands:
            print("\n[Comparison]")
            self.compare()

    def transform(self):
        for param in tqdm(self.params.transform):
            xyz = param["xyz"]
            transform_mod = Transform(xyz_shifts=xyz)
            transformed_img = transform_mod.execute(self.ref.data)
            target_name = f"{self.ref.basename}_{xyz[0]}_{xyz[1]}_{xyz[2]}.tif"
            self.datam.save_tif(
                data=transformed_img, folder="to_register", name=target_name
            )
            metadata = transform_mod.generate_metadata(target_name, self.ref.path)
            self.datam.save_metadata(metadata, "to_register")

    def register(self):
        target_paths = get_target_paths(
            self.datam.out_folder.to_register, self.ref.path
        )

        for targ_path in tqdm(target_paths):
            for param in self.params.register:
                reg_method = param["method"]
                reg_mod = Register(reg_method)
                target = load_tiff(targ_path)
                registered_img = reg_mod.execute(self.ref.data, target)
                base = remove_ext(os.path.basename(targ_path))
                shifted_filepath = f"{base}_{reg_method}"
                self.datam.save_tif(
                    data=registered_img,
                    folder="shifted",
                    name=shifted_filepath,
                )
                metad = reg_mod.generate_metadata(
                    shifted_filepath, ref_path=self.ref.path
                )
                self.datam.save_metadata(metad, "shifted")

    def compare(self):
        output_csv = os.path.join(self.datam.out_folder.comp, "similarity_report.csv")
        generate_similarity_report(
            self.ref.data, self.datam.out_folder.regis, output_csv
        )
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
                    self.ref.data, target, comp_method_path + "ref_VS_" + basename
                )
