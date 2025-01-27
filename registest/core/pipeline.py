#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import pandas as pd
from tqdm import tqdm

from registest.config.parameters import Parameters
from registest.core.data_manager import DataManager, get_target_paths, remove_ext
from registest.modules.comparison import Compare, normalize_image
from registest.modules.registration import Register
from registest.modules.transformation import Transform
from registest.utils.io_utils import load_tiff, save_png
from registest.utils.visualization import visu_rgb_2d, visu_rgb_slice


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
            for ref in self.datam.ref_list:
                self.ref = ref
                print(f"Reference image: {self.ref.path}")
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
                shifted_filepath = f"{base}_{reg_method}.tif"
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
        out_folder = self.datam.out_folder.similarity
        output_csv = os.path.join(out_folder, "similarity_report.csv")

        target_paths = get_target_paths(self.datam.out_folder.shifted, self.ref.path)
        self.ref.data = normalize_image(self.ref.data)

        for targ_path in tqdm(target_paths):
            target = load_tiff(targ_path)
            target = normalize_image(target)
            comp_mod = Compare()
            report = comp_mod.execute(self.ref.data, target)
            report["method"] = ""
            report["target"] = targ_path
            # Save report to CSV
            report_df = pd.DataFrame([report])
            report_df.to_csv(output_csv, index=False)
            print(f"Similarity report saved to {output_csv}")
            # Plotting
            visu_rgb_slice(
                self.ref.data,
                target,
                path_to_save=os.path.join(out_folder, os.path.basename(targ_path)),
            )
            project = visu_rgb_2d(self.ref.data, target)
            save_png(
                project,
                os.path.join(out_folder, f"{os.path.basename(targ_path)}_2d.png"),
            )

        # generate_similarity_report(
        #     self.ref.data, self.datam.out_folder.regis, output_csv
        # )
        # method_folder_names = self.params.register["method"]
        # self.datam.make_method_folders(self.datam.out_folder.comp, method_folder_names)
        # for fold_name in method_folder_names:
        #     shifted_target_paths = get_tif_filepaths(
        #         self.datam.out_folder.regis + os.sep + fold_name
        #     )
        #     for targ_path in shifted_target_paths:
        #         basename = os.path.basename(targ_path)
        #         print(f"Target: {fold_name}/{basename}")
        #         target = load_tiff(targ_path)
        #         comp_method_path = (
        #             self.datam.out_folder.comp + os.sep + fold_name + os.sep
        #         )
        #         visu_rgb_slice(
        #             self.ref.data, target, comp_method_path + "ref_VS_" + basename
        #         )
