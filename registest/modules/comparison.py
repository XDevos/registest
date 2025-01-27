import os

import numpy as np
import pandas as pd
from skimage.metrics import structural_similarity as ssim

from registest.core.data_manager import ReferenceImg
from registest.core.run_args import parse_run_args
from registest.utils.io_utils import save_png
from registest.utils.metrics import timing_main
from registest.utils.visualization import visu_rgb_2d, visu_rgb_slice


def normalize_image(image):
    """
    Normalize the image to the range [0, 1].

    Parameters
    ----------
    image : ndarray
        The input image to normalize.

    Returns
    -------
    ndarray
        The normalized image.
    """
    return (image - np.min(image)) / (np.max(image) - np.min(image))


def calculate_normalized_mse(image1, image2):
    """
    Calculate normalized MSE between two images.

    Parameters
    ----------
    image1, image2 : ndarray
        Two input images to compare (must have the same shape).

    Returns
    -------
    float
        The normalized Mean Squared Error (MSE).
    """
    mse = np.mean((image1 - image2) ** 2)
    return mse


class Compare:
    def __init__(self) -> None:
        pass

    def execute(self, reference_3d, target):
        # Calculate Normalized MSE and SSIM
        nmse_value = calculate_normalized_mse(reference_3d, target)
        ssim_value = ssim(reference_3d, target, data_range=1.0)
        return {
            "method": "method_name",
            "target": "target_name",
            "NMSE": round(nmse_value, 6),
            "SSIM": round(ssim_value, 6),
        }


@timing_main
def main():
    run_args = parse_run_args()
    ref_img = ReferenceImg(run_args.reference)
    target_img = ReferenceImg(run_args.target)
    # Normalize the reference and target images
    ref_img.data = normalize_image(ref_img.data)
    target_img.data = normalize_image(target_img.data)
    out_csv = os.path.join(run_args.folder, "similarity.csv")
    comp_mod = Compare()
    report = comp_mod.execute(ref_img.data, target_img.data)
    report["method"] = "unknown"
    report["target"] = run_args.target
    # Save report to CSV
    report_df = pd.DataFrame([report])
    report_df.to_csv(out_csv, index=False)
    print(f"Similarity report saved to {out_csv}")
    # Plotting
    visu_rgb_slice(
        ref_img.data,
        target_img.data,
        path_to_save=os.path.join(run_args.folder, target_img.basename),
    )
    project = visu_rgb_2d(ref_img.data, target_img.data)
    # overlay_uint8 = (project * 255).astype(np.uint8)
    save_png(project, os.path.join(run_args.folder, f"{target_img.basename}_2d.png"))


if __name__ == "__main__":
    main()
