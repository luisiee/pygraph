"""
An extension to pygraph.artists for storing and keeping track of 3D visual 
data.

History
---
Jan 19th, 2023 - Louis Servaes
"""

# .................{ IMPORTS                                  }................
import numpy as np

from pygraph.artists import Artist, Line, Points, Text


# .................{ CLASSES                                  }................
class Artist3D(Artist):
    """Virtual base class for storing and keeping track of 3D visual data 
    under an identity. Inherits from the pygraph.artists.Artist class.
    """
    # ...............{ DUNDERS                                  }..............
    def __init__(
        self, 
        x, 
        y, 
        z, 
        name: str
    ):
        """Initializes the Artist.

        Parameters
        ---
        x : Iterable[int | float]
            The Artist `xdata`.

        y : Iterable[int | float]
            The Artist `ydata`.
            
        z : Iterable[int | float]
            The Artist `zdata`.

        name : str
            The Artist identity or `name`.
        """
        Artist.__init__(self, x, y, name)
        zdata = np.array(z, dtype=float).flatten()
        assert self._xdata.size == zdata.size, (
            'Tried to initialize Artist, but `x` and `z` don\'t have the '
            'same size.'
        )
        self._zdata = zdata

    # ...............{ PROPERTIES                               }..............
    def get_zdata(self):
        """Gets the Artist `zdata`."""
        return self._zdata
    

class Line3D(Artist3D, Line):
    """Artist subclass for storing and keeping track of 3D line-type visual 
    data under an identity.
    """
    # ...............{ DUNDERS                                  }..............
    def __init__(
        self, 
        x, 
        y, 
        z, 
        name: str, 
        c: str = 'k', 
        lw: int | float = 1.0, 
        ls: str = 'solid',
    ):
        """Initializes the Artist.

        Parameters
        ---
        x : Iterable[int | float]
            The Artist `xdata`.

        y : Iterable[int | float]
            The Artist `ydata`.

        z : Iterable[int | float]
            The Artist `zdata`.

        name : str
            The Artist identity or `name`.

        c : str (optional):
            The Artist `color`. Default is black.

        lw : int | float (optional)
            The Artist `linewidth`. Default is 1.0.

        ls : str (optional)
            The Artist `linestyle`. Default is solid.
        """
        Artist3D.__init__(self, x, y, z, name)
        self.set_color(c)
        self.set_linewidth(lw)
        self.set_linestyle(ls)
    

class Points3D(Artist3D, Points):
    """Artist subclass for storing and keeping track of 3D point-type visual 
    data under an identity.
    """
    # ...............{ DUNDERS                                  }..............
    def __init__(
        self, 
        x, 
        y, 
        z, 
        name: str, 
        c='k', 
        s=1.0,
    ):
        """Initializes the Artist.

        Parameters
        ---
        x : Iterable[int | float]
            The Artist `xdata`.

        y : Iterable[int | float]
            The Artist `ydata`.
            
        z : Iterable[int | float]
            The Artist `zdata`.

        name : str
            The Artist identity or `name`.

        c : str | Iterable[int | float] (optional)
            The Artist `color`. If an Iterable[int | float] is passed, the size
            must match the Artist `xdata`, `ydata` and `zdata` size. Default 
            is black.

        s : int | float | Iterable[int | float] (optional)
            The Artist `size`. If an Iterable[int | float] is passed, the size
            must match the Artist `xdata`, `ydata` and `zdata` size. Default 
            is 1.0.
        """
        Artist3D.__init__(self, x, y, z, name)           
        self.set_color(c)
        self.set_size(s)


class Text3D(Artist3D, Text):
    """Artist subclass for storing and keeping track of 3D text-type visual 
    data under an identity.
    """
    # ...............{ DUNDERS                                  }..............
    def __init__(
        self, 
        x: int | float, 
        y: int | float, 
        z: int | float,
        text: str,
        name: str,
        c: str = 'k',
        s: int | float = 10,
        coord_type: str = 'data',
        offset: tuple[int | float, int | float] = (0, 0)
    ):
        """Initializes the Artist.

        Parameters
        ---
        x : int | float
            The Artist `xdata`.

        y : int | float
            The Artist `ydata`.

        z : int | float
            The Artist `zdata`.

        text : str
            The Artist `text`.

        name : str
            The Artist identity or `name`.

        c : str (optional)
            The Artist `color`. Default is black.

        s : int | float (optional)
            The Artist `size`. Default is 10.

        coord_type : str (optional)
            The Artist `coord_type`. Valid options are \'data\' and 
            \'fraction\'. Default is \'data\'.

        offset : tuple[int | float, int | float] (optional)
            The Artist text `offset` in points. Default is (0, 0).
        """
        Artist3D.__init__(self, x, y, z, name)
        self.set_text(text)
        self.set_color(c)
        self.set_size(s)
        self.set_offset(offset)