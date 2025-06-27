"""
More matplotlib 3D artists.

Usage
---
Call configure() to implement matplotlib 3D annotations and arrows.

Credit
---
This code is written by Wethat on Github.
URL: https://gist.github.com/WetHat/1d6cd0f7309535311a539b42cccca89c

History
---
Jan 19th, 2023 - Louis Servaes
"""

# .................{ IMPORTS                                  }................
import numpy as np
from matplotlib.patches import FancyArrowPatch
from matplotlib.text import Annotation
from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d.proj3d import proj_transform


# .................{ CLASSES                                  }................
class _MPLAnnotation3D(Annotation):

    def __init__(self, text, xyz, *args, **kwargs):
        super().__init__(text, xy=(0, 0), *args, **kwargs)
        self._xyz = xyz

    def draw(self, renderer):
        x2, y2, z2 = proj_transform(*self._xyz, self.axes.M)
        self.xy = (x2, y2)
        super().draw(renderer)


class _MPLArrow3D(FancyArrowPatch):

    def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._xyz = (x, y, z)
        self._dxdydz = (dx, dy, dz)

    def draw(self, renderer):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        super().draw(renderer)

    def do_3d_projection(self, renderer=None):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))

        return np.min(zs)
    

# .................{ FUNCTIONS                                }................
def _annotate3D(ax, text, xyz, *args, **kwargs):
    '''Add anotation `text` to an `Axes3d` instance.'''

    annotation = _MPLAnnotation3D(text, xyz, *args, **kwargs)
    ax.add_artist(annotation)
    return annotation


def _arrow3D(ax, x, y, z, dx, dy, dz, *args, **kwargs):
    '''Add a 3d arrow to an `Axes3D` instance.'''

    arrow = _MPLArrow3D(x, y, z, dx, dy, dz, *args, **kwargs)
    ax.add_artist(arrow)
    return arrow


def configure_3d_artists():
    setattr(Axes3D, 'annotate3D', _annotate3D)
    setattr(Axes3D, 'arrow3D', _arrow3D)