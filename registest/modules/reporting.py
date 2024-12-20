import os

import numpy as np
import pandas as pd
import tifffile
from skimage.metrics import structural_similarity as ssim


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


def generate_similarity_report(reference_3d, registered_dir, output_csv):
    """
    Generate a similarity report comparing registered images to a reference image.

    Parameters
    ----------
    reference_path : str
        Path to the reference image.
    registered_dir : str
        Path to the directory containing registered images organized by method.
    output_csv : str
        Path to save the generated CSV report.
    """

    if reference_3d.ndim != 3:
        raise ValueError("The reference image must be 3D.")

    # Normalize the reference image
    reference_3d = normalize_image(reference_3d)

    report_data = []

    # Iterate over registration methods
    for method_name in os.listdir(registered_dir):
        method_path = os.path.join(registered_dir, method_name)

        if not os.path.isdir(method_path):
            continue

        # Iterate over registered targets
        for target_name in os.listdir(method_path):
            if not target_name.endswith((".tif", ".tiff")):
                continue

            target_path = os.path.join(method_path, target_name)
            target = tifffile.imread(target_path)

            if target.shape != reference_3d.shape:
                raise ValueError(
                    f"Shape mismatch: {target_name} does not match the reference image."
                )

            # Normalize the target image
            target = normalize_image(target)

            # Calculate Normalized MSE and SSIM
            mse_value = calculate_normalized_mse(reference_3d, target)
            ssim_value = ssim(reference_3d, target, data_range=1.0)

            # Append results
            report_data.append(
                {
                    "Method": method_name,
                    "Target": target_name,
                    "Normalized MSE": round(mse_value, 6),
                    "SSIM": round(ssim_value, 6),
                }
            )

    # Save report to CSV
    report_df = pd.DataFrame(report_data)
    report_df.to_csv(output_csv, index=False)

    print(f"Similarity report saved to {output_csv}")


if __name__ == "__main__":
    # Input paths
    reference_path = "/home/xdevos/Documents/tempo2/img_sum.tif"
    registered_dir = "/home/xdevos/Documents/tempo2/Registration"
    output_csv = "similarity_report.csv"

    # Generate report
    generate_similarity_report(reference_path, registered_dir, output_csv)
