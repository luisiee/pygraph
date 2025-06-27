"""
History
---
Jan 9th, 2023 - Louis Servaes
"""

# .................{ IMPORTS                                  }................
import numpy as np


# .................{ CLASSES                                  }................
class ColorMesh:
    """Artist-like class for storing a 2D colored mesh."""
    # ...............{ DUNDERS                                  }..............
    def __init__(
        self, 
        X: np.ndarray, 
        Y: np.ndarray, 
        C: np.ndarray,
        cmap: str = 'plasma'
    ):
        """Initializes the ColorMesh.

        Parameters
        ---
        X, Y : np.meshgrid
            The ColorMesh `xdata` and `ydata`.

        C : np.ndarray
            The ColorMesh `color`. `C` must have the same shape as `X` and 
            `Y`.
        """
        assert len(np.shape(X)) == 2, (
            'Tried to initialize ColorMesh, but `X` isn\'t 2 dimensional.'
        )
        assert np.shape(X) == np.shape(Y) == np.shape(C), (
            'Tried to initialize ColorMesh, but `X`, `Y` and `C` don\'t have '
            'the same shape.'
        )
        self._X = X
        self._Y = Y
        self._C = C
        self._cmap = cmap
        
    # ...............{ PUBLIC METHODS                           }..............
    def draw(
        self, 
        figure, 
        overwrite: bool = False
    ):
        """Adds the ColorMesh to a Figure.

        Parameters
        ---
        figure : pygraph.pygraph.Figure
            The Figure on which to draw the ColorMesh.

        overwrite : bool (optional)
            If the Figure already has a ColorMesh, remove that ColorMesh and 
            add this ColorMesh to the Figure. Default is False.

        See Also
        ---
        Figure.add_color_mesh and Figure.color_mesh from 
        pygraph.pygraph.Figure.
        """
        figure.add_color_mesh(self, overwrite)
        
    # ...............{ PROPERTIES                               }..............
    def get_xdata(self):
        """Gets the ColorMesh `xdata`."""
        return self._X

    def get_ydata(self):
        """Gets the ColorMesh `ydata`."""
        return self._Y
    
    def get_color(self):
        """Gets the ColorMesh `color`."""
        return self._C
    
    def get_cmap(self):
        """Gets the ColorMesh `cmap`."""
        return self._cmap