from math import ceil
from PIL import Image
from StringIO import StringIO


def scale_and_dither(im, size):
    max_width, max_height = size
    w, h = im.size

    if w > max_width or h > max_height:
        ratio = min(max_width/w, max_height/h)
        im.thumbnail((int(w*ratio), int(h*ratio)), Image.ANTIALIAS)
        w, h = im.size

    # Remove transparency
    im = im.convert('RGBA')
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bg.paste(im, mask=im.split()[3])

    im = bg.convert('1')
    return im


def image_as_stream(im):
    out_data = StringIO()
    im.save(out_data, format='PNG')

    return out_data


def to_thermal(im, margin=None):
    out = ''
    w, h = im.size

    if margin is not None:
        out += '\x1bl'
        out += chr(margin)

    out += '\x1b~G'
    line_len = chr(int(ceil(w/8.0)))
    for i in range(0, h):
        out += line_len
        for j in range(0, w, 8):
            b = ''
            for x in range(j, min(w, j+8)):
                b += str(int(im.getpixel((x, i)) == 0))
            out += chr(int(b.ljust(8, '0'), 2))
        out += '\x00'
    out += '\x80'

    return out
