#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import tifffile
from skimage import exposure


def normalize_image(image):
    return (image - np.min(image)) / (np.max(image) - np.min(image))


def image_adjust(image, lower_threshold=0.3, higher_threshold=0.9999):
    """
    Adjust intensity levels:
        - rescales exposures
        - gets histogram of pixel intensities to define cutoffs
        - applies thresholds

    Parameters
    ----------
    image : numpy array
        input 3D image.
    lower_threshold : float, optional
        lower threshold for adjusting image levels. The default is 0.3.
    higher_threshold : float, optional
        higher threshold for adjusting image levels.. The default is 0.9999.

    Returns
    -------
    image1 : numpy array
        adjusted 3D image.

    """
    # rescales image to [0,1]
    image1 = exposure.rescale_intensity(image, out_range=(0, 1))
    # calculates histogram of intensities
    hist1_before = exposure.histogram(image1)

    hist_sum = np.zeros(len(hist1_before[0]))
    for i in range(len(hist1_before[0]) - 1):
        hist_sum[i + 1] = hist_sum[i] + hist1_before[0][i]

    sum_normalized = hist_sum / hist_sum.max()
    lower_cutoff = np.where(sum_normalized > lower_threshold)[0][0] / 255
    higher_cutoff = np.where(sum_normalized > higher_threshold)[0][0] / 255

    # adjusts image intensities from (lower_threshold,higher_threshold) --> [0,1]
    image1 = exposure.rescale_intensity(
        image1, in_range=(lower_cutoff, higher_cutoff), out_range=(0, 1)
    )

    return image1


def visu_slice(normalized_3d):
    fig = px.imshow(normalized_3d, color_continuous_scale="viridis", animation_frame=0)
    fig.update_layout(title="Visualisation 3D Interactive")
    # fig.show()
    fig.write_html("visualization_slice.html")


def visu_3d(normalized_image):
    # Créer une grille pour les coordonnées (x, y, z)
    z, y, x = np.mgrid[
        : normalized_image.shape[0],
        : normalized_image.shape[1],
        : normalized_image.shape[2],
    ]
    # Créer le rendu volumétrique avec Plotly
    fig = go.Figure(
        data=go.Volume(
            x=x.flatten(),
            y=y.flatten(),
            z=z.flatten(),
            value=normalized_image.flatten(),
            isomin=0.1,  # Valeur minimale pour le rendu
            isomax=0.8,  # Valeur maximale pour le rendu
            opacity=0.1,  # Opacité pour voir à travers les surfaces
            surface_count=20,  # Nombre de surfaces pour le rendu volumétrique
            colorscale="Viridis",  # Palette de couleurs
        )
    )

    # Afficher la visualisation
    fig.update_layout(title="Vol 3D", scene=dict(aspectmode="data"))
    # fig.show()
    fig.write_html("visualization_3d.html")


def overlay_3d_img(ref_img, shifted_img):
    sz = ref_img.shape
    img_1, img_2 = (
        ref_img / ref_img.max(),
        shifted_img / shifted_img.max(),
    )
    img_1 = image_adjust(img_1, lower_threshold=0.5, higher_threshold=0.9999)
    img_2 = image_adjust(img_2, lower_threshold=0.5, higher_threshold=0.9999)
    null_image = np.zeros(sz)
    rgb = np.dstack([img_1, img_2, null_image])
    return rgb


def visu_rgb(ref, target):
    fig = go.Figure()
    z, y, x = np.mgrid[
        : ref.shape[0],
        : ref.shape[1],
        : ref.shape[2],
    ]
    fig.add_trace(
        go.Volume(
            x=x.flatten(),
            y=y.flatten(),
            z=z.flatten(),
            value=ref.flatten(),
            isomin=0.1,
            isomax=1.0,
            opacity=0.1,
            surface_count=20,
            colorscale=[[0, "rgba(255,0,0,0)"], [1, "rgba(255,0,0,1)"]],
            name="Red (Reference Image)",
        )
    )
    fig.add_trace(
        go.Volume(
            x=x.flatten(),
            y=y.flatten(),
            z=z.flatten(),
            value=target.flatten(),
            isomin=0.1,
            isomax=1.0,
            opacity=0.1,
            surface_count=20,
            colorscale=[[0, "rgba(0,255,0,0)"], [1, "rgba(0,255,0,1)"]],
            name="Green (Shifted Image)",
        )
    )
    fig.update_layout(
        title="3D RGB Visualization (Red: Reference, Green: Shifted)",
        scene=dict(aspectmode="data"),
    )
    fig.show()


def enhance_contrast(img, power=1):
    """
    Enhance contrast non-linearly by applying a power transformation.

    Parameters
    ----------
    img : ndarray
        Normalized image (values in [0, 1]).
    power : float
        The exponent for the power transformation. Higher values enhance differences more.

    Returns
    -------
    ndarray
        Contrast-enhanced image.
    """
    return normalize_image(np.power(img, power))


def visu_rgb_slice(ref_img, shifted_img, path_to_save):
    """
    Visualize two 3D images together using the RGB overlay technique.

    Parameters
    ----------
    ref_img : ndarray
        The reference image to be visualized in the red channel.
    shifted_img : ndarray
        The shifted image to be visualized in the green channel.
    """
    # Ensure both images have the same shape
    if ref_img.shape != shifted_img.shape:
        raise ValueError("Both images must have the same shape.")

    min_ch = np.minimum(ref_img, shifted_img)
    overlay = np.stack(
        [
            enhance_contrast(ref_img),
            enhance_contrast(shifted_img),
            enhance_contrast(min_ch),
        ],
        axis=-1,
    )

    # Visualize using Plotly
    fig = px.imshow(
        overlay,
        animation_frame=0,  # Frame corresponds to slices along Z-axis
        labels={"animation_frame": "Z Slice"},
    )
    fig.update_layout(
        title="Overlay Visualization (RED: Reference, GREEN: Shifted, WHITE: Relevant similarities)",
        coloraxis_showscale=False,  # Hide color scale for RGB visualization
    )

    # Save visualization as HTML
    fig.write_html(path_to_save + ".html")
    print("Visualization saved to " + path_to_save + ".html")

    return overlay


def visu_rgb_2d(ref_img, shifted_img):
    """
    Visualize two 2D images together using the RGB overlay technique.

    Parameters
    ----------
    ref_img : ndarray
        The reference image to be visualized in the red channel.
    shifted_img : ndarray
        The shifted image to be visualized in the green channel.
    """
    # Ensure both images have the same shape
    if ref_img.shape != shifted_img.shape:
        raise ValueError("Both images must have the same shape.")

    min_ch = np.minimum(ref_img, shifted_img)
    overlay = np.stack(
        [
            enhance_contrast(ref_img).max(axis=0),
            enhance_contrast(shifted_img).max(axis=0),
            enhance_contrast(min_ch).max(axis=0),
        ],
        axis=-1,
    )
    # Display the overlay
    # plt.figure(figsize=(6, 6))
    # plt.imshow(overlay)
    # plt.axis("off")  # Hide axis for better visualization
    # plt.title("RGB Overlay: Red (Reference), Green (Shifted), Blue (Overlap)")
    # plt.show()

    return (overlay * 255).astype(np.uint8)


if __name__ == "__main__":
    base = "/home/xdevos/Repositories/XDevos/pyhim-small-dataset/register_global/IN/global/"
    tar0 = base + "scan_001_RT26_005_ROI_converted_decon_ch00.tif"
    ref = base + "scan_001_RT27_005_ROI_converted_decon_ch00.tif"
    # base = "/home/xdevos/Documents/tempo2/"
    # tar0 = base + "Preparation/target_0.tif"
    # ref = base + "img_sum.tif"
    image_3d = tifffile.imread(ref)
    normalized_3d = normalize_image(image_3d)
    tar_3d = tifffile.imread(tar0)
    normalized_tar = normalize_image(tar_3d)
    visu_rgb_slice(normalized_3d, normalized_tar, "visualization_overlay")
