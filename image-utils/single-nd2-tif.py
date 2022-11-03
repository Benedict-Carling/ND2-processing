import argparse

from nd2reader import ND2Reader
import skimage
import matplotlib.pyplot as plt
from PIL import Image
import os

parser = argparse.ArgumentParser()
parser.add_argument("inputPath", help="input nd2 file path to process", type=str)
parser.add_argument("outputFolder", help="folder to output images to", type=str)
parser.parse_args()

args = parser.parse_args()

os.mkdir(args.outputFolder)
os.mkdir(args.outputFolder + "/tif")
os.mkdir(args.outputFolder + "/png")


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
        for indexFoV, FoV in (
            enumerate(channel) if "f" in images.bundle_axes else enumerate([channel])
        ):
            for indexZ, Z in (
                enumerate(FoV) if "z" in images.bundle_axes else enumerate([FoV])
            ):
                for indexTime, frame in (
                    enumerate(Z) if "z" in images.bundle_axes else enumerate([Z])
                ):
                    titleTif = f"{args.outputFolder}/tif/channel{index}_fov{indexFoV}_Z{indexZ}_time{indexTime}"
                    titlePng = f"{args.outputFolder}/png/channel{index}_fov{indexFoV}_Z{indexZ}_time{indexTime}"
                    rescaledImage = skimage.exposure.rescale_intensity(frame) * 255
                    plt.imsave(f"{titlePng}.png", rescaledImage, cmap="Greys")
                    im = Image.open(f"{titlePng}.png")
                    im.save(f"{titleTif}.tif")
