from copy import copy
from gdspy import * # NOQA

import font
import sys

WGLFAREA = 76
NO_FILL = 93


def newdict(olddict, key, value):
    d = copy(olddict)
    d.update({key: value})
    return d


def expand(ds):
    """
    takes a dictionary with keys pointing to lists and converts it
    to a list of dictionaries, where each key points to a single number.
    """
    if hasattr(ds, 'keys'):
        ds = [ds]

    for d in ds:
        #print d
        for k, v in d.items():
            try:
                newd = [newdict(d, k, i) for i in v]
                newds = []
                for e in ds:
                    if e is d:
                        newds += newd
                    else:
                        newds.append(e)
                return expand(newds)
            except TypeError:
                pass
    return ds


class Layout:
    def __init__(self, w, h, texth=12., layer=75):
        self.w = w
        self.h = h
        self.texth = texth
        self.layer = layer

        self.params = []
        self.devices = []
        self.padding = []

    def make_devices(self, device_func, params, padding=(20, 20, 20, 20)):
        if len(padding) is not 4:
            raise TypeError(
                "expect padding to look like (left, up, right, down)")

        params = expand(params)
        # save params to make a map
        self.params += params
        # render cells
        self.devices += [device_func(**p) for p in params]
        self.padding += [padding] * len(params)

    def make_layout(self):
        c = Cell("ENTIRE THING")
        i = 0
        y0 = 0
        while i < len(self.devices):
            n, space, h = self.getrow(i)
            #print n, space, h
            self.drawrow(c, y0, i, n, space, h)
            y0 -= h
            i += n

        usage = -y0 / float(self.h)
        print("drew %d devices over ~%.0f%% of available space (%d x %d um)."
                % (len(self.devices), usage * 100.,
                self.w, self.h))

        return c

    def getrow(self, i):
        """
        measures out how many devices can fit in a row.
        returns row, space, h
        where:
          n is number of device cells to draw,
          space is extra padding between devices to spread out extra space
          h is height row should be (including room for label)
        """
        n = 0
        row_w = 0
        row_h = 0

        # loop until row full
        while True:
            if i >= len(self.devices):
                break

            v1, v2 = self.devices[i].get_bounding_box()
            w, h = v2 - v1

            ww = w + self.padding[i][0] + self.padding[i][2]
            if row_w + ww <= self.w:
                n += 1
                row_w += ww
            else:
                break

            hh = h + self.padding[i][1] + self.padding[i][3] + self.texth
            if hh > row_h:
                row_h = hh

            i += 1

        if n > 1 and i < len(self.devices):
            space = (self.w - row_w) / float(n - 1)
        else:
            space = 0

        return n, space, row_h

    def drawrow(self, c, y0, i0, n, space, rh):
        x = 0
        #b1 = (x, y0 - rh)

        for i in range(i0, i0 + n):
            d = self.devices[i]
            p = self.padding[i]
            v1, v2 = d.get_bounding_box()
            w, h = v2 - v1

            # add device
            vspace = (rh - self.texth - h - p[1] - p[3]) / 2.
            origin = (x + p[0] - v1[0], y0 - vspace - p[1] - v2[1])
            c.add(CellReference(d, origin=origin))

            # add device id
            if self.texth > 0:
                text = font.text("%04d" % i, self.texth)
                t1, t2 = text.get_bounding_box()
                tw, th = t2 - t1
                origin = (x + (p[0] + w + p[2] - tw) / 2.,
                          y0 - rh - t1[1] + (self.texth - th) / 2.)
                c.add(CellReference(text, origin=origin))
            x += p[0] + w + p[2] + space

        # add LightField Area Box over devices
        b1 = (0, y0 - rh + self.texth)
        b2 = (x - space, y0)
        c.add(Rectangle(b1, b2, layer=WGLFAREA))

        # add NO_FILL box over text
        if self.texth > 0:
            b1 = (0, y0 - rh)
            b2 = (x - space, b1[1] + self.texth)
            c.add(Rectangle(b1, b2, layer=NO_FILL))

    def view(self):
        c = self.make_layout()

        if len(sys.argv) > 1:
            name = sys.argv[1]
            if name[-4:] != ".gds":
                name += ".gds"

            gdspy.gds_print(name, cells=[c], name=name, precision=5.e-9)
        else:
            LayoutViewer(c)
