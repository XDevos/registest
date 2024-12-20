#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

import numpy as np
import tifffile


def save_tiff(image, filename):
    tifffile.imwrite(filename, image, dtype=np.uint16)


def generate_psf(shape, voxel_size=(0.25, 0.1, 0.1), attenuation_factor=2.0):
    """
    Generate a 3D PSF (Point Spread Function).
    :param shape: 3D image shape (Z, X, Y).
    :param voxel_size: voxel shape (Z, X, Y) in microns.
    :return: a 3D image with a PSF in center.
    """
    z, x, y = shape
    voxel_z, voxel_x, voxel_y = voxel_size
    z_coords = np.linspace(-1, 1, z) * voxel_z / min(voxel_size)
    x_coords = np.linspace(-1, 1, x) * voxel_x / min(voxel_size)
    y_coords = np.linspace(-1, 1, y) * voxel_y / min(voxel_size)
    z_grid, x_grid, y_grid = np.meshgrid(z_coords, x_coords, y_coords, indexing="ij")

    # Gaussian
    psf = np.exp(-attenuation_factor * (z_grid**2 + x_grid**2 + y_grid**2))
    # Center PSF
    image = ((psf / psf.max()) * 65535).astype(np.uint16)  # uint16
    return image


def add_psf(image, psf, position=None):
    """
    Adds a PSF to a larger 3D image at the specified position, using sum, mean, or max.
    :param image: The larger image (numpy array) to which the PSF will be added.
    :param psf: The PSF (numpy array) to be added.
    :param position: Tuple (z, x, y) specifying the center position where the PSF will be added.
                     If None, the PSF is added at the center of the image.
    :return: Updated image with the PSF added.
    """
    z, x, y = image.shape
    psf_z, psf_x, psf_y = psf.shape

    # Default to the center of the image if no position is specified
    if position is None:
        position = (z // 2, x // 2, y // 2)

    # Calculate bounds for placement
    start_z = max(0, position[0] - psf_z // 2)
    end_z = min(z, position[0] + psf_z // 2)
    start_x = max(0, position[1] - psf_x // 2)
    end_x = min(x, position[1] + psf_x // 2)
    start_y = max(0, position[2] - psf_y // 2)
    end_y = min(y, position[2] + psf_y // 2)

    # Corresponding bounds in the PSF
    psf_start_z = max(0, psf_z // 2 - position[0])
    psf_end_z = psf_start_z + (end_z - start_z)
    psf_start_x = max(0, psf_x // 2 - position[1])
    psf_end_x = psf_start_x + (end_x - start_x)
    psf_start_y = max(0, psf_y // 2 - position[2])
    psf_end_y = psf_start_y + (end_y - start_y)

    # Intermediate computation with uint32 to prevent overflow
    combined = image.astype(np.uint32)
    # Combine PSF with the image
    combined[start_z:end_z, start_x:end_x, start_y:end_y] += psf[
        psf_start_z:psf_end_z, psf_start_x:psf_end_x, psf_start_y:psf_end_y
    ].astype(np.uint32)
    # Normalize to maintain proportions
    max_val = max(combined.max(), 65535)
    combined = (combined / max_val * 65535).astype(np.uint16)
    return combined


if __name__ == "__main__":
    # psf1 = generate_psf(
    #     shape=(60, 128, 128), voxel_size=(0.25, 0.1, 0.1), attenuation_factor=20
    # )
    # psf2 = generate_psf(
    #     shape=(60, 128, 128), voxel_size=(0.25, 0.1, 0.1), attenuation_factor=30
    # )
    # save_tiff(psf1, "psf1.tif")
    # save_tiff(psf2, "psf2.tif")
    # pos1 = (28, 100, 80)
    # pos2 = (30, 100, 100)
    # img_sum = np.ones((60, 256, 256), dtype=np.uint16)
    # img_sum = add_psf(img_sum, psf1, pos1)
    # img_sum = add_psf(img_sum, psf2, pos2)
    # save_tiff(img_sum, "img_sum.tif")
    n_spots = 100
    psf_list = [
        generate_psf(
            shape=(60, 128, 128),
            voxel_size=(0.25, 0.1, 0.1),
            attenuation_factor=random.randint(30, 70),
        )
        for _ in range(n_spots)
    ]
    psf_pos_list = [
        (
            random.randint(5, 55),
            random.randint(64, 256 - 64),
            random.randint(64, 256 - 64),
        )
        for _ in range(n_spots)
    ]
    pos_shifted = []
    for x, y, z in psf_pos_list:
        pos_shifted.append(
            (
                x + random.randint(-4, 4),
                y + random.randint(-4, 4),
                z + random.randint(-4, 4),
            )
        )
    img_ref = np.ones((60, 256, 256), dtype=np.uint16) * 10
    target = np.ones((60, 256, 256), dtype=np.uint16) * 10
    for i in range(n_spots):
        img_ref = add_psf(img_ref, psf_list[i], psf_pos_list[i])
        target = add_psf(target, psf_list[i], pos_shifted[i])

    save_tiff(img_ref, "img_ref.tif")
    save_tiff(target, "target.tif")
