from skimage.metrics import mean_squared_error, structural_similarity
import numpy as np

class Compare:
    @staticmethod
    def execute(image1, image2, metric):
        if metric == "mse":
            return mean_squared_error(image1, image2)
        elif metric == "ssim":
            return structural_similarity(image1, image2, multichannel=False)

def masked_mse(ref, target):
    mask = ~np.isnan(ref) & ~np.isnan(target)
    mse = np.mean((ref[mask] - target[mask]) ** 2)
    return mse

def masked_ssim(ref, target, neutral_val = 0):
    ref_valid = np.nan_to_num(ref, nan=neutral_val)
    target_valid = np.nan_to_num(target, nan=neutral_val)
    ssim_value = structural_similarity(ref_valid, target_valid)
    return ssim_value