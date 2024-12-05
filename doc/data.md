# Dataset description

We want to work on TIFF image in 3D with the uint16 type.
Default pixel size (micron): Z=0.25, X=0.1, Y=0.1
Image shape: (60,2048,2048)
PSF size (pixel) : (30,64,64)
First basic image for pytest including just one PSF (size in pixel): (60,128,128) ~ 8MB in memory


input:
	3D tiff image
	commands:
		transform
		extract
		register
		shift
		extract
		compare
		visualize
		report
	parameters:
		how to transform
		registration method

def extract(img1, img2):
	"""extract a mask of common valid value
	return NaN(img1) OR NaN(img2)"""

def transform(img, zxy):
	"""shift img with specific output filename
	return shifted_img"""

def register(ref, target):
	"""apply a specific method to find the shifts between ref and target.
	return zxy_shift"""

def compare(ref, target):
	"""return MSE ou SSIM"""

