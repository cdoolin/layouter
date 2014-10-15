import numpy as np
import gdspy

# taken from .svg files drawn with inkscape
W, H = 20., 30.
WGTEXT = 77

spaths = [
    "8,5 -3,2 -1,4 0,8 1,4 3,2 4,0 3,-2 1,-4 0,-8 -1,-4 -3,-2",
    "4,7 2,3 2,-1 0,13 -3,0 0,3 10,0 0,-3 -3,0 0,-17 -4,0",
    "4,7 2,3 2,-1 3,0 1,2 -1,3 -7,7 0,4 12,0 0,-4 -5,0 0,-1 5,-6 0,-5 -2,-4 -6,0",
    "5,7 2,-2 7,0 2,3 0,5 -1,2 1,2 0,5 -2,3 -7,0 -3,-3 2,-2 3,1 3,0 0,-4 -3,-1 0,-2 3,-1 1,-2 -1,-2 -3,0 -2,1",
    "4,5 1,11 7,0 0,9 4,0 0,-20 -4,0 0,8 -4,0 0,-8",
    "14,5 -9,0 0,11 5,0 1,1 1,1 -1,2 -2,1 -4,-2 -1,4 6,2 4,-1 2,-4 0,-4 -2,-3 -5,0 0,-4 7,1 0,-5",
    "15,6 -3,-2 -6,0 -2,4 0,16 3,2 6,0 3,-1 0,-4 -1,-3 -2,-1 -5,1 -1,-9 2,-2 4,2",
    "4,5 0,5 8,0 0,1 -2,4 -4,0 0,3 3,0 0,1 -2,4 0,2 4,0 2,-7 3,0 0,-3 -2,0 0,-1 2,-4 0,-5",
    "7,5 -2,2 0,6 3,1 0,1 -3,2 0,5 1,2 2,1 5,0 1,-1 1,-2 0,-5 -2,-2 0,-1 2,-2 0,-4 -1,-3",
    "6,5 -2,2 0,5 2,2 7,0 0,11 3,0 0,-18 -2,-2",
]


paths = []
for s in spaths:
    p = [np.array(v.split(','), dtype='f8') for v in s.split(' ')]
    p = [np.sum(p[:i + 1], 0) for i in range(len(p))]
    p = [np.array((v[0], H - v[1])) for v in p]
    paths.append(p)


invcells = []
for i, p in enumerate(paths):
    r = gdspy.Rectangle((0, 0), (W, H), layer=0)
    pol = gdspy.boolean([r, p], lambda r, p: r and not p, layer=WGTEXT)
    c = gdspy.Cell("ifont_%1d" % i, exclude_from_global=True)
    c.add(pol)
    invcells.append(c)


invtextid = 0
def invtext(text, height=12):
    global invtextid
    c = gdspy.Cell("invtext_%04d" % int(invtextid), exclude_from_global=True)
    invtextid += 1
    mag = float(height) / H
    for i, l in enumerate(text):
        if l not in "0123456789":
            raise TypeError("DONT KNOW HOW TO MAKE LETTERS \"%s\"." % l)
        c.add(gdspy.CellReference(
            invcells[int(l)],
            origin=(i * W * mag, 0),
            magnification=mag))
        #c.add(invpolys[int(l)])
    return c

cells = []
for i, p in enumerate(paths):
    p = gdspy.Polygon(layer=WGTEXT, points=p)
    c = gdspy.Cell("font_%1d" % i,  exclude_from_global=True)
    c.add(p)
    cells.append(c)

textid = 0
def text(text, height=12):
    global textid
    c = gdspy.Cell("text_%04d" % int(textid), exclude_from_global=True)
    textid += 1
    mag = float(height) / H
    for i, l in enumerate(text):
        if l not in "0123456789":
            raise TypeError("DONT KNOW HOW TO MAKE LETTERS \"%s\"." % l)
        c.add(gdspy.CellReference(
            cells[int(l)],
            origin=(i * W * mag, 0),
            magnification=mag))
        #c.add(invpolys[int(l)])
    return c

if __name__ == "__main__":
    gdspy.LayoutViewer(invtext(''.join([str(x) for x in range(len(spaths))])))
