# -*- coding: utf-8 -*-

import os

import SimpleITK as sitk
from skimage.registration import phase_cross_correlation

from registest.config.metadata import FileMetadata, MetadataManager
from registest.core.data_manager import OutImg, ReferenceImg
from registest.core.run_args import parse_run_args
from registest.modules.transformation import shift_3d_array_subpixel
from registest.utils.metrics import timing_main


def phase_cross_correlation_wrapper(ref_3d, target_3d):
    shift, _, _ = phase_cross_correlation(ref_3d, target_3d, upsample_factor=100)
    return shift


def affine_sitk(fixed_image, moving_image):
    # Convert NumPy arrays to SimpleITK images and cast to Float32
    fixed_sitk = sitk.GetImageFromArray(fixed_image)
    moving_sitk = sitk.GetImageFromArray(moving_image)
    fixed_sitk = sitk.Cast(fixed_sitk, sitk.sitkFloat32)  # Convert to float
    moving_sitk = sitk.Cast(moving_sitk, sitk.sitkFloat32)  # Convert to float
    registration = sitk.ImageRegistrationMethod()
    registration.SetMetricAsMeanSquares()
    # Optimization
    registration.SetOptimizerAsRegularStepGradientDescent(
        learningRate=1.0, minStep=1e-4, numberOfIterations=100
    )
    transform = sitk.CenteredTransformInitializer(
        fixed_sitk,
        moving_sitk,
        sitk.AffineTransform(3),
        sitk.CenteredTransformInitializerFilter.GEOMETRY,
    )
    registration.SetInitialTransform(transform, inPlace=False)
    final_transform = registration.Execute(fixed_sitk, moving_sitk)
    affine_transform = final_transform.GetBackTransform()  # Extracts the last transform
    shift_x, shift_y, shift_z = affine_transform.GetTranslation()
    return [shift_x, shift_y, shift_z]


class Register:
    def __init__(self, method="global_pyhim"):
        self.method: str = method
        self.zxy_shift = None
        self.xyz_shift = None

    def execute(self, ref_3d, target_3d):
        if self.method == "global_pyhim":
            self.zxy_shift, _, _ = phase_cross_correlation(
                ref_3d, target_3d, upsample_factor=100
            )
            self.xyz_shift = [
                float(self.zxy_shift[1]),
                float(self.zxy_shift[2]),
                float(self.zxy_shift[0]),
            ]
            return self.apply(target_3d)
        elif self.method == "global_sitk":
            self.xyz_shift = affine_sitk(ref_3d, target_3d)
            self.zxy_shift = [
                float(self.xyz_shift[2]),
                float(self.xyz_shift[0]),
                float(self.xyz_shift[1]),
            ]
            return self.apply(target_3d)
        else:
            raise NotImplementedError(
                f"The method '{self.method}' is not implemented. Please use a supported method such as 'global_pyhim' or `global_sitk`."
            )

    def apply(self, target_3d):
        if self.zxy_shift is None:
            raise ValueError
        return shift_3d_array_subpixel(target_3d, self.zxy_shift)

    def generate_metadata(self, key_path: str, ref_path):
        metad = FileMetadata(key_path, ref_path)
        metad.registration = {"done": True, "method": self.method}
        metad.shift = {"done": True, "xyz_values": self.xyz_shift}
        return metad


@timing_main
def main():
    run_args = parse_run_args()
    ref_img = ReferenceImg(run_args.reference)
    target_img = ReferenceImg(run_args.target)
    out_path = os.path.join(run_args.folder, os.path.basename(run_args.target))
    out_img = OutImg(out_path)
    method = run_args.method
    registration = Register(method)
    registered_img = registration.execute(ref_img.data, target_img.data)
    out_img.save(registered_img)
    metad = registration.generate_metadata(out_img.path, ref_path=ref_img.path)
    meta_datam = MetadataManager(folder=out_img.dirname)
    meta_datam.add_file_metadata(metad)


if __name__ == "__main__":
    main()
