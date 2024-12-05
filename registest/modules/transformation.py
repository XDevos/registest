import scipy.ndimage as ndi


class Transform:
    @staticmethod
    def execute(image, type, **params):
        if type == "rotate":
            angle = params.get("angle", 0)
            return ndi.rotate(image, angle, axes=(1, 2), reshape=False)
        elif type == "scale":
            scale = params.get("scale", 1)
            return ndi.zoom(image, scale)
        # Add more transformations as needed
