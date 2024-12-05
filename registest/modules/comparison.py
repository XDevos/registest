from skimage.metrics import mean_squared_error, structural_similarity


class Compare:
    @staticmethod
    def execute(image1, image2, metric):
        if metric == "mse":
            return mean_squared_error(image1, image2)
        elif metric == "ssim":
            return structural_similarity(image1, image2, multichannel=False)
