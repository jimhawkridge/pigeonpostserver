from PIL import Image, ImageDraw, ImageFont

from .splittext import split_text
import thermalimage
from django.conf import settings

MAX_WIDTH = 300.0
MAX_HEIGHT = 400.0


def scale_and_dither(stream):
    im = Image.open(stream)

    sd = thermalimage.scale_and_dither(im, (MAX_WIDTH, MAX_HEIGHT))
    return thermalimage.image_as_stream(sd)


def build_image(stream, text):
    pic = Image.open(stream)

    new_image = Image.new('1', (600, 400), 1)
    new_image.paste(pic, (300, 0))
    draw = ImageDraw.Draw(new_image)

    f = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Verdana_Bold.ttf', 15)
    lines = split_text(text, f, 280)
    for i, line in enumerate(lines):
        draw.text((10, 10+i*20), line, font=f)

    return new_image


def to_thermal(im):
    return thermalimage.to_thermal(im, settings.MARGIN)
