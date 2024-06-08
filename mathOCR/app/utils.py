from pix2tex.cli import LatexOCR
from PIL import Image


def get_latex_from_image(image_path):
    model = LatexOCR()
    image = Image.open(image_path)
    return model(image)