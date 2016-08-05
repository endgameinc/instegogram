import subprocess
from PIL import Image
#requires ImageMagick
import array


QTABLEARRAY = {0: array.array('b', [6, 4, 5, 6, 5, 4, 6, 6, 5, 6, 7, 7, 6, 8, 10, 16, 10, 10, 9, 9, 10, 20, 14,
                                    15, 12, 16, 23, 20, 24, 24, 23, 20, 22, 22, 26, 29, 37, 31, 26, 27, 35, 28,
                                    22, 22, 32, 44, 32, 35, 38, 39, 41, 42, 41, 25, 31, 45, 48, 45, 40, 48, 37,
                                    40, 41, 40]),
               1: array.array('b', [7, 7, 7, 10, 8, 10, 19, 10, 10, 19, 40, 26, 22, 26, 40, 40, 40, 40, 40, 40,
                                    40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40,
                                    40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40,
                                    40, 40, 40, 40, 40, 40])}


def prep_img(filepath):
    """ Resizes an image to at max 1080x1080 square and re-quantizes with Instagram's quantization table"""
    target = filepath[:-4] + '_prepped' + '.jpg'

    with Image.open(filepath) as img:
        width, height = img.size

    min_dim = min(width, height)
    if min_dim < 1080:
        img_dim = str(min_dim) + 'x' + str(min_dim) + '!'
    else:
        img_dim = '1080x1080!'

    subprocess.call(['convert', '-resize', img_dim, filepath, target])

    with Image.open(target) as img:
        img.save(target, qtables=QTABLEARRAY, **img.info)

    return target
