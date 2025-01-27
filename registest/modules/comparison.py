import os
import shutil

import fitz  # PyMuPDF
import numpy as np
import pandas as pd
from PIL import Image
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


def add_page_pdf(
    img_2d_path, pdf_path, refpath, target_path, xyz_transfo, xyz_shifts, ssim, nmse
):

    # Sample dictionary with information
    info_dict = {
        "Reference Path": refpath,
        "Target Path": target_path,
        # "XYZ Transformation": xyz_transfo,
        # "XYZ Shifts": xyz_shifts,
        "SSIM": ssim,
        "NMSE": nmse,
    }

    # Ensure the image exists
    if not os.path.exists(img_2d_path):
        raise FileNotFoundError(f"Image not found: {img_2d_path}")

    # Check if the PDF exists
    if os.path.exists(pdf_path):
        doc = fitz.open(pdf_path)  # Open existing PDF
        print(f"Appending a new page to {pdf_path}")
    else:
        doc = fitz.open()  # Create a new empty PDF
        print(f"Creating a new PDF as {pdf_path}")

    # Create a new page (A4 size)
    new_page = doc.new_page(width=595, height=842)  # Standard A4 page in points

    # Add an image
    img = Image.open(img_2d_path)
    img_width, img_height = img.size
    max_width, max_height = 400, 300  # Max size in points
    scale = min(max_width / img_width, max_height / img_height)

    # Calculate position (centered)
    x_pos = (595 - (img_width * scale)) / 2
    y_pos = 500  # Place it near the top

    # Insert the image
    new_page.insert_image(
        (x_pos, y_pos, x_pos + img_width * scale, y_pos + img_height * scale),
        filename=img_2d_path,
    )

    # Insert text information below the image
    y_text = y_pos - 50  # Start above image
    x_text = 50  # Left margin

    for key, value in info_dict.items():
        new_page.insert_text((x_text, y_text), f"{key}: {value}", fontsize=12)
        y_text -= 20  # Move down for the next line

    temp_pdf = "temp_updated.pdf"  # Temporary file
    # Save the modified PDF
    doc.save(temp_pdf)
    doc.close()
    # Replace the original file with the updated version
    shutil.move(temp_pdf, pdf_path)


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
    # Append the new row to the existing CSV file without erasing data
    report_df.to_csv(
        out_csv, mode="a", header=not pd.io.common.file_exists(out_csv), index=False
    )
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
