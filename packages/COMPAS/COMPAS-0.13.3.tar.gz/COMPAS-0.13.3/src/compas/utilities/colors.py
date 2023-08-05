from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import re

try:
    basestring
except NameError:
    basestring = str


__all__ = [
    'i_to_rgb',
    'i_to_red',
    'i_to_green',
    'i_to_blue',
    'i_to_white',
    'i_to_black',
    'rgb_to_hex',
    'hex_to_rgb',
    'color_to_colordict',
    'color_to_rgb',
    'rgb_to_rgb',
    'is_color_rgb',
    'is_color_hex',
    'is_color_light',

    'Colormap',

    'red',
    'green',
    'blue',
    'yellow',
    'cyan',
    'white',
    'black',
]


red = 255, 0, 0
orange = 255, 125, 0
yellow = 255, 255, 0
yellowish = 125, 255, 0
green = 0, 255, 0
greenish = 0, 255, 125
cyan = 0, 255, 255
cyanish = 0, 125, 255
blue = 0, 0, 255

white = 255, 255, 255
black = 0, 0, 0


BASE16 = '0123456789abcdef'


try:
    HEX_DEC = {v: int(v, base=16) for v in [x + y for x in BASE16 for y in BASE16]}
except Exception:
    HEX_DEC = {v: int(v, 16) for v in [x + y for x in BASE16 for y in BASE16]}


def i_to_rgb(i, normalize=False):
    i = max(i, 0.0)
    i = min(i, 1.0)
    if i == 0.0:
        r, g, b = 0, 0, 255
    elif 0.0 < i < 0.25:
        r, g, b = 0, int(255 * (4 * i)), 255
    elif i == 0.25:
        r, g, b = 0, 255, 255
    elif 0.25 < i < 0.5:
        r, g, b = 0, 255, int(255 - 255 * 4 * (i - 0.25))
    elif i == 0.5:
        r, g, b = 0, 255, 0
    elif 0.5 < i < 0.75:
        r, g, b = int(0 + 255 * 4 * (i - 0.5)), 255, 0
    elif i == 0.75:
        r, g, b = 255, 255, 0
    elif 0.75 < i < 1.0:
        r, g, b,  = 255, int(255 - 255 * 4 * (i - 0.75)), 0
    elif i == 1.0:
        r, g, b = 255, 0, 0
    else:
        r, g, b = 0, 0, 0
    if not normalize:
        return [r, g, b]
    else:
        return [r / 255.0, g / 255.0, b / 255.0]


def i_to_red(i):
    i = max(i, 0.0)
    i = min(i, 1.0)
    gb = min((1 - i) * 255, 255)
    return (255, int(gb), int(gb))


def i_to_green(i):
    i = max(i, 0.0)
    i = min(i, 1.0)
    rb = min((1 - i) * 255, 255)
    return (int(rb), 255, int(rb))


def i_to_blue(i):
    i = max(i, 0.0)
    i = min(i, 1.0)
    rg = min((1 - i) * 255, 255)
    return (int(rg), int(rg), 255)


def i_to_white(i):
    i = max(i, 0.0)
    i = min(i, 1.0)
    rgb = min((1 - i) * 255, 255)
    return (int(rgb), int(rgb), int(rgb))


def i_to_black(i):
    i = max(i, 0.0)
    i = min(i, 1.0)
    rgb = min(i * 255, 255)
    return (int(rgb), int(rgb), int(rgb))


class Colormap(object):

    colorfuncs = {
        'rgb': i_to_rgb,
        'red': i_to_red,
        'green': i_to_green,
        'blue': i_to_blue,
        'white': i_to_white,
        'black': i_to_black
    }

    def __init__(self, data, spec):
        self.data = data
        self.dmin = min(data)
        self.dmax = max(data)
        self.dspan = self.dmax - self.dmin
        self.colorfunc = Colormap.colorfuncs[spec]

    def __call__(self, value):
        i = (value - self.dmin) / (self.dspan)
        return self.colorfunc(i)


# see: http://stackoverflow.com/questions/4296249/how-do-i-convert-a-hex-triplet-to-an-rgb-tuple-and-back


def is_color_rgb(color):
    if isinstance(color, (tuple, list)):
        return len(color) == 3
    return False


def is_color_hex(color):
    if isinstance(color, basestring):
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)
        if match:
            return True
        return False
    return False


def rgb_to_rgb(rgb, g=None, b=None):
    if g is None and b is None:
        r, g, b = rgb
    else:
        r = rgb
    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))
    c = min((r, g, b))
    if isinstance(c, float) and c <= 1.0:
        r = r * 255.0
        g = g * 255.0
        b = b * 255.0
    return int(r), int(g), int(b)


def rgb_to_hex(rgb, g=None, b=None):
    r, g, b = rgb_to_rgb(rgb, g=g, b=b)
    # return format(r << 16 | g << 8 | b, '06x')
    return '#{0:02x}{1:02x}{2:02x}'.format(r, g, b)


def hex_to_rgb(value, normalize=False):
    value = value.lstrip('#').lower()
    r = HEX_DEC[value[0:2]]
    g = HEX_DEC[value[2:4]]
    b = HEX_DEC[value[4:6]]
    if normalize:
        return r / 255.0, g / 255.0, b / 255.0
    return r, g, b


def color_to_colordict(color, keys, default=None, colorformat='hex', normalize=False):
    color = color or default

    if color is None:
        return {key: None for key in keys}

    # if input is hex
    # and output should be rgb
    if isinstance(color, basestring):
        if colorformat == 'rgb':
            color = hex_to_rgb(color, normalize=normalize)
        return {key: color for key in keys}

    # if input is rgb
    # and output should be hex
    if isinstance(color, (tuple, list)) and len(color) == 3:
        if colorformat == 'hex':
            color = rgb_to_hex(color)
        return {key: color for key in keys}

    if isinstance(color, dict):
        for k, c in color.items():

            # if input is hex
            # and output should be rgb
            if isinstance(c, basestring):
                if colorformat == 'rgb':
                    color[k] = hex_to_rgb(c)

            # if input is rgb
            # and output should be hex
            if isinstance(c, (tuple, list)) and len(c) == 3:
                if colorformat == 'hex':
                    color[k] = rgb_to_hex(c)

        return {key: (default if key not in color else color[key]) for key in keys}

    raise Exception('This is not a valid color format: {0}'.format(type(color)))


def color_to_rgb(color, normalize=False):
    if isinstance(color, basestring):
        r, g, b = hex_to_rgb(color)
    elif isinstance(color, int):
        r, g, b = i_to_rgb(color)
    else:
        r, g, b = color
    if not normalize:
        return r, g, b
    if isinstance(r, float):
        return r, g, b
    return r / 255., g / 255., b / 255.


def is_color_light(color):
    if is_color_hex(color):
        rgb = hex_to_rgb(color)
    else:
        rgb = color
    r, g, b = rgb_to_rgb(rgb)
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0
    r = ((r + 0.055) / 1.055) ** 2.4
    g = ((g + 0.055) / 1.055) ** 2.4
    b = ((b + 0.055) / 1.055) ** 2.4
    L = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return L > 0.179


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest

    doctest.testmod(globs=globals())
