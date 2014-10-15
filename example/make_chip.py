#!/usr/bin/env python


#
# set up functions to draw structures that will be
# parameterized
#
# fucntions should accept parameters as arguments and
# return a gdspy cell.
#

from gdspy import *
from layouter import uid

ANCHOR_W = ANCHOR_H = 10
pi = 3.1515926535

def minI_device(layer=0, R=10, paddle_w=2, paddle_h=.2,
        torsion_w=.13, torsion_h=5, gap=.13, lhang=1.):
    """
    draws a simple disc resonator and torsional device.
    returns a gds cell approximately centered with device things.
    """
    pw, ph = paddle_w / 2., paddle_h / 2.
    tw, th = torsion_w / 2., torsion_h / 2.

    disc = Round((-R, 0), R, layer=layer)

    # rectangles are made by specifying the bottom left and top right
    # corners.  I compute those first to make it easier to read.
    v1 = (gap, -ph)
    v2 = (gap + paddle_w, ph)
    paddle = Rectangle(v1, v2, layer=layer)

    v1 = (gap + pw - tw, -th)
    v2 = (gap + pw + tw, th)
    torsion = Rectangle(v1, v2, layer=layer)

    a1 = (v1[0] - lhang, th)
    a2 = (v1[0] + ANCHOR_W - lhang, th + ANCHOR_H)
    anchor1 = Rectangle(a1, a2, layer=layer)

    b1 = (a1[0], -th - ANCHOR_H)
    b2 = (a2[0], -th)
    anchor2 = Rectangle(b1, b2, layer=layer)

    c = Cell(uid('minI'), exclude_from_global=True)
    c.add([disc, paddle, torsion, anchor1, anchor2])

    return c



#
# Import layouter and generate layout
#


from layouter import Layout
l = Layout(2500, 6300)

# sweep paddle_w and torsion_h
l.make_devices(minI_device, {
    'R': [5],
    'paddle_w': range(2, 7),
    'paddle_h': [.13, .3, 1.],
    'gap': [0.105, .13],
    'torsion_h': range(5, 20, 2),
}, padding=[12, 20, 12, 20])

# sweep R
l.make_devices(minI_device, {
    'R': [2.5 + i * 2. for i in range(10)],
    'paddle_w': 5,
    'paddle_h': .5,
    'gap': .13,
    'torsion_h': [5, 8, 11],
}, padding=[12, 20, 12, 20])


if __name__ == "__main__":
    l.view()
