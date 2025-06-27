"""
A collection of classes for storing and keeping track of 2D visual data. All 
classes that are implemented in pygraph inherit from a virtual base class 
`Artist`, of which in theory no instance needs to be created (unless you want 
a 2D data container, in which case it is recommended to implement your own 
container).

History
---
Dec 31th, 2023 - Louis Servaes
"""

# .................{ IMPORTS                                  }................
import matplotlib as mpl
import matplotlib.colors as mcolors
import numpy as np

import pygraph.errors as e


# .................{ CLASSES                                  }................
class Artist:
    """Virtual base class for storing and keeping track of 2D visual data 
    under an identity.
    """
    # ...............{ CLASS VARIABLES                          }..............
    # dictionary containing all valid colors (str) (from matplotlib.colors)
    COLOR_OPTIONS = (
        mcolors.BASE_COLORS | mcolors.TABLEAU_COLORS | mcolors.CSS4_COLORS
    )

    # ...............{ DUNDERS                                  }..............
    def __init__(
        self, 
        x, 
        y, 
        name: str
    ):
        """Initializes the Artist.

        Parameters
        ---
        x : Iterable[int | float]
            The Artist `xdata`.

        y : Iterable[int | float]
            The Artist `ydata`.

        name : str
            The Artist identity or `name`.
        """
        xdata = np.array(x, dtype=float).flatten()
        ydata = np.array(y, dtype=float).flatten()
        assert xdata.size == ydata.size, (
            'Tried to initialize Artist, but `x` and `y` don\'t have the '
            'same size.'
        )
        self._xdata = xdata
        self._ydata = ydata
        self.set_name(name)

    # ...............{ PUBLIC METHODS                           }..............
    def draw(
        self, 
        figure, 
        label: str = '', 
        overwrite: bool = False
    ):
        """Adds the Artist to a Figure.

        Parameters
        ---
        figure : pygraph.pygraph.Figure
            The Figure on which to draw the Artist.

        label : str (optional)
            The Artist Label when added to the Figure Legend. Default is 
            Artist `name`.

        overwrite : bool (optional)
            If another Artist with the same Artist `name` is currently 
            displayed, remove that Artist and add this Artist to the Figure.
            Default is False.

        See Also
        ---
        Figure.add_artist from pygraph.pygraph.Figure.
        """
        figure.add_artist(self, label, overwrite)

    # ...............{ PROPERTIES                               }..............
    def get_xdata(self):
        """Gets the Artist `xdata`."""
        return self._xdata

    def get_ydata(self):
        """Gets the Artist `ydata`."""
        return self._ydata
    
    def get_name(self):
        """Gets the Artist `name`."""
        return self._name
    
    def set_name(self, name: str):
        """Sets the Artist `name`."""
        self._name = name
        return name


class Line(Artist):
    """Artist subclass for storing and keeping track of 2D line-type visual 
    data under an identity.
    """
    # ...............{ CLASS VARIABLES                          }..............
    # linestyle options (str) (from matplotlib)
    LS_OPTIONS = {
        'solid',
        'dashed',
        'dotted',
        'dashdot',
        '-',
        '--'
        ':',
        '-.'
    }

    # ...............{ DUNDERS                                  }..............
    def __init__(
        self, 
        x, 
        y, 
        name: str, 
        c: str = 'k', 
        lw: int | float = 1.0, 
        ls: str = 'solid'
    ):
        """Initializes the Artist.

        Parameters
        ---
        x : Iterable[int | float]
            The Artist `xdata`.

        y : Iterable[int | float]
            The Artist `ydata`.

        name : str
            The Artist identity or `name`.

        c : str (optional):
            The Artist `color`. Default is black.

        lw : int | float (optional)
            The Artist `linewidth`. Default is 1.0.

        ls : str (optional)
            The Artist `linestyle`. Default is solid.
        """
        super().__init__(x, y, name)
        self.set_color(c)
        self.set_linewidth(lw)
        self.set_linestyle(ls)

    # ...............{ PROPERTIES                               }..............
    def get_color(self):
        """Gets the Artist `color`."""
        return self._c
        
    def set_color(self, c: str):
        """Sets the Artist `color`."""
        assert c in Artist.COLOR_OPTIONS, e.OptionsError('Line', 'c')
        self._c = c
        return c
    
    def get_linewidth(self):
        """Gets the Artist `linewidth`."""
        return self._lw
    
    def set_linewidth(self, lw: int | float):
        """Sets the Artist `linewidth`."""
        self._lw = lw
        return lw
    
    def get_linestyle(self):
        """Gets the Artist `linestyle`."""
        return self._ls
    
    def set_linestyle(self, ls: str):
        """Sets the Artist `linestyle`."""
        assert ls in Line.LS_OPTIONS, e.OptionsError(
            'Line', 'ls', options=Line.LS_OPTIONS
        )
        self._ls = ls
        return ls
    
    
class Straight(Line):
    """Artist subclass for storing and keeping track of 2D straight-type
    visual data under an identity.
    """
    # ...............{ DUNDERS                                  }..............
    def __init__(
        self, 
        xy: tuple[int | float, int | float], 
        dir: tuple[int | float, int | float], 
        name: str, 
        c: str = 'k', 
        lw: int | float = 1.0, 
        ls: str = 'solid'
    ):
        """Initializes the Artist.

        Parameters
        ---
        xy : tuple[int | float, int | float]
            The Artist `xdata` and `ydata`. This is the point through which the
            Straight runs.

        dir : tuple[int | float, int | float]
            The Artist `dir`. This is the direction of the Straight.

        name : str
            The Artist identity or `name`.

        c : str (optional):
            The Artist `color`. Default is black.

        lw : int | float (optional)
            The Artist `linewidth`. Default is 1.0.

        ls : str (optional)
            The Artist `linestyle`. Default is solid.
        """
        dx, dy = dir
        super().__init__(*xy, name, c, lw, ls)
        self._dx = dx
        self._dy = dy

    # ...............{ PROPERTIES                               }..............
    def get_dir(self):
        """Gets the Artist `dir`."""
        return self._dx, self._dy


class Points(Artist):
    """Artist subclass for storing and keeping track of 2D point-type visual 
    data under an identity.
    """
    # ...............{ DUNDERS                                  }..............
    def __init__(
        self, 
        x, 
        y, 
        name: str, 
        c='k', 
        s=1.0,
        t='.'
    ):
        """Initializes the Artist.

        Parameters
        ---
        x : Iterable[int | float]
            The Artist `xdata`.

        y : Iterable[int | float]
            The Artist `ydata`.

        name : str
            The Artist identity or `name`.

        c : str | Iterable[int | float] (optional)
            The Artist `color`. If an Iterable[int | float] is passed, the size
            must match the Artist `xdata` and `ydata` size. Default is black.

        s : int | float | Iterable[int | float] (optional)
            The Artist `size`. If an Iterable[int | float] is passed, the size
            must match the Artist `xdata` and `ydata` size. Default is 1.0.

        t : str (optional)
            The Artist `type`. Default is point.
        """
        super().__init__(x, y, name)
        self.set_color(c)           
        self.set_size(s)
        self._t = t

    # ...............{ PROPERTIES                               }..............
    def get_color(self):
        """Gets the Artist `color`."""
        return self._c

    def set_color(self, c):
        """Sets the Artist `color`. If an Iterable[int | float] is passed, the 
        size must match the Artist `xdata` and `ydata` size.
        """
        if isinstance(c, str):
            assert c in Artist.COLOR_OPTIONS, e.OptionsError('Points', 'c')
        else:
            c = np.array(c, dtype=float).flatten()
            assert c.size == self._xdata.size, (
                'Tried to set Points `color`, but `c` doesn\'t have the same '
                'size as `x` and `y`.'
            )

        self._c = c
        return c
    
    def get_size(self):
        """Gets the Artist `size`."""
        return self._s
    
    def set_size(self, s):
        """Sets the Artist `size`. If an Iterable[int | float] is passed, the 
        size must match the Artist `xdata` and `ydata` size.
        """
        if not isinstance(s, int | float):
            s = np.array(s, dtype=float).flatten()
            assert s.size == self._xdata.size, (
                'Tried to set Points `size`, but `s` doesn\'t have the same '
                'size as `x` and `y`.'
            )

        self._s = s
        return s
    
    def get_mpl_size(self):
        """Gets the matplotlib.collections.Pathcollection size."""
        return self._s * mpl.rcParams['lines.markersize']**2 / 4

    def get_type(self):
        """Gets the Artist `type`."""
        return self._t


class Arrows(Artist):
    PIVOT_OPTIONS = {'tip', 'mid', 'tail'}

    def __init__(
        self,
        x,
        y,
        u,
        v,
        name: str,
        c=0,
        pivot: str = 'mid'
    ):
        super().__init__(x, y, name)

        u = np.array(u, dtype=float).flatten()
        v = np.array(v, dtype=float).flatten()
        assert u.size == v.size == self._xdata.size, (
            'Tried to initialize Arrows, but `u` and `v` don\'t have the '
            'same size as `x` and `y`.'
        )

        self._uv = np.vstack((u, v))
        self.set_color(c)
        self._pivot = pivot

    # ...............{ PROPERTIES                               }..............
    def get_dir(self):
        """Gets the Artist `dir`."""
        return self._uv
    
    def get_color(self):
        """Gets the Artist `color`."""
        return self._c

    def set_color(self, c):
        """Sets the Artist `color`. If an Iterable[int | float] is passed, the 
        size must match the Artist `xdata` and `ydata` size.
        """
        if not isinstance(c, int | float):
            c = np.array(c, dtype=float).flatten()
            assert c.size == self._xdata.size, (
                'Tried to set Arrows `color`, but `c` doesn\'t have the same '
                'size as `x` and `y`.'
            )

        self._c = c
        return c
    
    def get_pivot(self):
        """Gets the Artist `pivot`."""
        return self._pivot
    
    def set_pivot(self, pivot: str):
        """Sets the Artist `pivot`. Options are \'tip\', \'mid\' and 
        \'tail\'.
        """
        assert pivot in Arrows.PIVOT_OPTIONS, e.OptionsError(
            'Arrows', 'pivot', Arrows.PIVOT_OPTIONS
        )
        self._pivot = pivot
        return pivot


class Text(Artist):
    """Artist subclass for storing and keeping track of 2D text-type visual 
    data under an identity.
    """
    # ...............{ CLASS VARIABLES                          }..............
    # dictionary mapping valid coordinate options (str) to
    # matplotlib.text.Annotation.xycoords (str) (from matplotlib.text)
    COORD_OPTIONS = {
        'data': 'data', 
        'fraction': 'axes fraction'
    }

    # ...............{ DUNDERS                                  }..............
    def __init__(
        self, 
        x: int | float, 
        y: int | float, 
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
        super().__init__(x, y, name)
        self.set_text(text)
        self.set_color(c)
        self.set_size(s)
        self.set_coord_type(coord_type)
        self.set_offset(offset)

    # ...............{ PROPERTIES                               }..............
    def get_text(self):
        """Gets the Artist `text`."""
        return self._text
    
    def set_text(self, text: str):
        """Sets the Artist `text`."""
        self._text = text
        return text
    
    def get_color(self):
        """Gets the Artist `color`."""
        return self._c
    
    def set_color(self, c: str):
        """Sets the Artist `color`."""
        assert c in Artist.COLOR_OPTIONS, e.OptionsError('Text', 'c')
        self._c = c
        return c
    
    def get_size(self):
        """Gets the Artist `size`."""
        return self._s
    
    def set_size(self, s: int | float):
        """Sets the Artist `size`."""
        self._s = s
        return s
    
    def get_coord_type(self):
        """Gets the Artist `coord_type`."""
        return self._coord_type
    
    def set_coord_type(self, coord_type: str):
        """Sets the Artist `coord_type`. Valid options are \'data\' and 
        \'fraction\'.
        """
        assert coord_type in Text.COORD_OPTIONS, e.OptionsError(
            'Text', 'coord_type', options=Text.COORD_OPTIONS
        )
        self._coord_type = coord_type
        return coord_type
    
    def get_offset(self):
        """Gets the Artist text `offset` in points."""
        return self._offset
    
    def set_offset(self, offset):
        """Sets the Artist text `offset` in points."""
        self._offset = offset
        return offset