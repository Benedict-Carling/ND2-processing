import argparse

from nd2reader import ND2Reader
import skimage
import matplotlib.pyplot as plt
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("inputPath", help="input nd2 file path to process", type=str)
parser.add_argument("outputFolder", help="folder to output images to", type=str)
parser.parse_args()

args = parser.parse_args()


def getBundleAxis(sizes):
    bundle_axes = ""
    if "x" in sizes:
        bundle_axes = "x" + bundle_axes
    if "y" in sizes:
        bundle_axes = "y" + bundle_axes
    if "t" in sizes:
        bundle_axes = "t" + bundle_axes
    if "z" in sizes:
        bundle_axes = "z" + bundle_axes
    if "v" in sizes:
        bundle_axes = "v" + bundle_axes
    return bundle_axes


with ND2Reader(args.inputPath) as images:
    images.bundle_axes = getBundleAxis(images.sizes)
    images.iter_axes = "c"
    for index, channel in enumerate(images):
        for indexFoV, FoV in enumerate(channel) if "f" in images.bundle_axes else enumerate([channel]):
            for indexZ, Z in enumerate(FoV) if "z" in images.bundle_axes else enumerate([FoV]):
                for indexTime, frame in enumerate(Z) if "z" in images.bundle_axes else enumerate([Z]):
                    title = f"{args.outputFolder}/channel{index}_fov{indexFoV}_Z{indexZ}_time{indexTime}"
                    rescaledImage = skimage.exposure.rescale_intensity(frame) * 255
                    plt.imsave(f"{title}.png", rescaledImage, cmap="Greys")
                    im = Image.open(f"{title}.png")
                    im.save(f"{title}.tif")

    # for index, channel in enumerate(images):
        
    #     if operator.contains(images.bundle_axes,"f"):
    #     for indexFoV, FoV in enumerate(channel) if "f" in :
    #         for indexTime, frame in enumerate(channel):
    #             title = f"{args.outputFolder}/channel{index}_fov{FoV}_time{indexTime}"
    #             rescaledImage = skimage.exposure.rescale_intensity(frame) * 255
    #             plt.imsave(f"{title}.png", rescaledImage, cmap="Greys")
    #             im = Image.open(f"pngImages/channel{index}_time{indexTime}.png")
    #             im.save(f"{title}.tif")
