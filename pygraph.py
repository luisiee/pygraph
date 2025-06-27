"""
A collection of classes for plotting data. This module relies on matplotlib
and numpy, and uses the `Artist` class from pygraph.artists to keep track of 
data in a more intuitive way. 

Functionalities
---
* Keeping track of Artists currently plotted in an easy manner.
* Automatically adjusting limits of a matplotlib.axes.Axes.
* Adding to and removing from a matplotlib.Legend.

History
---
Jan 18th, 2023 - Louis Servaes
"""


# .................{ IMPORTS                                  }................
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

import pygraph.errors as e
from pygraph.artists import Arrows, Artist, Line, Points, Straight, Text
from pygraph.artists_3d import Artist3D, Line3D, Points3D, Text3D
from pygraph.mesh import ColorMesh
from pygraph.mpl_3d import configure_3d_artists

# .................{ CONFIGURATION                            }................
configure_3d_artists()


# .................{ CLASSES                                  }................
class Window:
    # ...............{ CLASS VARIABLES                          }..............
    PROJECTION_OPTIONS = {
        '2d': 'rectilinear', 
        '3d': '3d'
    }

    # ...............{ DUNDERS                                  }..............
    def __init__(
        self,
        windowsize: tuple[int | float, int | float] = (8, 6),
        nrows: int = 1,
        ncols: int = 1,
        title: str = '',
        figure_projection: str = '2d',
        figure_padding: int | float = 3,
    ):
        
        mpl_proj = Window.PROJECTION_OPTIONS[figure_projection]
        mpl_fig, mpl_axs = plt.subplots(
            nrows, 
            ncols, 
            figsize=windowsize, 
            subplot_kw={'projection': mpl_proj}
        )

        self._mpl_fig = mpl_fig
        self._mpl_axs = mpl_axs
        self._figures = self._create_figures(
            mpl_fig, mpl_axs, figure_projection
        )
        self._figure_projection = figure_projection

        mpl_fig.suptitle(title)
        plt.tight_layout(pad=figure_padding)

    # ...............{ PRIVATE METHODS                          }..............
    # initializes the figures when Window is initialized
    def _create_figures(self, mpl_fig, mpl_axs, figure_projection):
        match figure_projection:
            case '2d':
                if not isinstance(mpl_axs, np.ndarray):
                    return Figure(mpl_fig, mpl_axs)

                figures = []
                for mpl_ax in mpl_axs.flatten():
                    figures.append(Figure(mpl_fig, mpl_ax))
                return np.reshape(figures, np.shape(mpl_axs))
            
            case '3d':
                if not isinstance(mpl_axs, np.ndarray):
                    return Figure3D(mpl_fig, mpl_axs)

                figures = []
                for mpl_ax in mpl_axs.flatten():
                    figures.append(Figure3D(mpl_fig, mpl_ax))
                return np.reshape(figures, np.shape(mpl_axs))
            
        raise NotImplementedError()

    # ...............{ PUBLIC METHODS                           }..............
    def show(self):
        if self._figure_projection == '2d':
            for figure in np.array(self._figures).flatten():
                figure.update_scale()
        plt.show()

    def soft_destroy(self):
        plt.close(self._mpl_fig)

    # ...............{ PROPERTIES                               }..............
    def get_mpl_fig(self):
        return self._mpl_fig
    
    def get_mpl_axs(self):
        return self._mpl_axs

    def get_figures(self):
        return self._figures
    
    def get_figure_projection(self):
        return self._figure_projection
    

class _Figure:
    # ...............{ DUNDERS                                  }..............
    def __init__(
        self,
        mpl_fig,
        mpl_ax,
        xlabel='',
        ylabel='',
        title='',
    ):
        self._mpl_fig = mpl_fig
        self._mpl_ax = mpl_ax
        self._mpl_artists = {}
        self._artists = {}
        self._color_mesh = None

        mpl_ax.set_xlabel(xlabel)
        mpl_ax.set_ylabel(ylabel)
        mpl_ax.set_title(title)

        self.legend = Legend(self)

    # ...............{ PRIVATE METHODS                          }..............
    def _add_mpl_artist(self, artist: Artist, label: str):
        raise NotImplementedError()
    
    # ...............{ PUBLIC METHODS                           }..............
    def soft_destroy(self):
        self._mpl_ax.set_visible(False)
                
    def add_artist(
        self, 
        artist: Artist, 
        label: str = '', 
        overwrite: bool = False
    ):

        name = artist.get_name()
        
        if name in self._artists:
            if overwrite:
                self.remove_artist(name)
            else:
                raise AssertionError(e.IndexError(
                    'Figure', 'artist', overwrite=True
                ))
            
        if not label:
            label = name

        self._add_mpl_artist(artist, label)
        self._artists[name] = artist

    def remove_artist(self, name: str):
        assert name in self._artists, e.IndexError(
            'Figure', 'artist', action='remove Artist from Figure'
        )
        self._artists.pop(name)
        mpl_artist = self._mpl_artists.pop(name)
        mpl_artist.remove()

    def set_visible(self, name: str, visibility: bool = True):
        assert name in self._artists, e.IndexError(
            'Figure', 'artist', action='set Artist visibility'
        )
        self._mpl_artists[name].set_visible(visibility)

    def add_colorbar(self, name: str = None):
        if name is not None:
            assert name in self._artists, e.IndexError(
                'Figure', 'artist', action='add Figure colorbar'
            )
            artist = self._artists[name]
        else:
            artist = self._color_mesh

        data = artist.get_color()
        norm = mcolors.Normalize(np.min(data), np.max(data))
        sm = cm.ScalarMappable(norm, artist.get_cmap())
        self._mpl_fig.colorbar(sm, ax=self._mpl_ax)

    # ...............{ PROPERTIES                               }..............
    def get_mpl_ax(self):
        return self._mpl_ax
    
    def get_mpl_artists(self):
        return self._mpl_artists

    def get_artists(self):
        return self._artists
    
    def get_color_mesh(self):
        return self._color_mesh


class Figure(_Figure):
    # ...............{ CLASS VARIABLES                          }..............
    # options for automatically adjusting Figure xlim and ylim
    AUTOSCALE_OPTIONS = {
        'all',      # fit Figure width and height to artists
        'width',    # only width
        'height',   # only height
        'none'      # don't automatically adjust xlim and ylim
    }
    # NOTE: # Figure is scaled once when the Window is shown via Window.show.
    # It is however still possible to manually call update_scale.

    # ...............{ DUNDERS                                  }..............
    def __init__(
        self,
        mpl_fig,
        mpl_ax,
        xlabel='',
        ylabel='',
        title='',
        autoscale='none',
    ):
        super().__init__(mpl_fig, mpl_ax, xlabel, ylabel, title)
        self._mpl_quad_mesh = None
        self.set_autoscale(autoscale)
        
    # ...............{ PRIVATE METHODS                          }..............
    def _add_mpl_artist(self, artist: Artist, label: str):
        if isinstance(artist, Straight):
            self._add_mpl_axline(artist, label)
        elif isinstance(artist, Line):
            self._add_mpl_line(artist, label)
        elif isinstance(artist, Points):
            self._add_mpl_scatter(artist, label)
        elif isinstance(artist, Arrows):
            self._add_mpl_quiver(artist, label)
        elif isinstance(artist, Text):
            self._add_mpl_annotation(artist)
        else:
            raise NotImplementedError()

    # draws Straight via matplotlib.pyplot.axline
    def _add_mpl_axline(self, straight, label):
        x = straight.get_xdata()[0]
        y = straight.get_ydata()[0]
        dx, dy = straight.get_dir()
        mpl_axline = self._mpl_ax.axline(
            (x, y),
            (x + dx, y + dy),
            color=straight.get_color(), 
            linewidth=straight.get_linewidth(),
            linestyle = straight.get_linestyle(),
            label=label
        )
        self._mpl_artists[straight.get_name()] = mpl_axline
    
    # draws Line via matplotlib.pyplot.plot
    def _add_mpl_line(self, line, label):
        (mpl_line,) = self._mpl_ax.plot(
            line.get_xdata(), 
            line.get_ydata(), 
            color=line.get_color(), 
            linewidth=line.get_linewidth(),
            linestyle = line.get_linestyle(),
            label=label
        )
        self._mpl_artists[line.get_name()] = mpl_line

    # draws Points via matplotlib.pyplot.scatter
    def _add_mpl_scatter(self, points, label):
        mpl_path_collection = self._mpl_ax.scatter(
            points.get_xdata(), 
            points.get_ydata(), 
            c=points.get_color(), 
            s=points.get_mpl_size(), 
            marker=points.get_type(),
            label=label
        )
        self._mpl_artists[points.get_name()] = mpl_path_collection

    # draws Arrows via matplotlib.pyplot.quiver
    def _add_mpl_quiver(self, arrows, label):
        u, v = arrows.get_dir()
        mpl_quiver = self._mpl_ax.quiver(
            arrows.get_xdata(),
            arrows.get_ydata(),
            u,
            v,
            arrows.get_color(),
            pivot=arrows.get_pivot(),
            label=label
        )
        self._mpl_artists[arrows.get_name()] = mpl_quiver

    # draws Text via matplotlib.pyplot.annotate
    def _add_mpl_annotation(self, text):
        mpl_annotation = self._mpl_ax.annotate(
            text.get_text(),
            (text.get_xdata()[0], text.get_ydata()[0]),
            text.get_offset(),
            Text.COORD_OPTIONS[text.get_coord_type()],
            'offset points',
            color=text.get_color(),
            fontsize=text.get_size()
        )
        self._mpl_artists[text.get_name()] = mpl_annotation

    # draws ColorMesh via matplotlib.pyplot.pcolormesh
    def _add_mpl_quad_mesh(self, color_mesh):
        mpl_quad_mesh = self._mpl_ax.pcolormesh(
            color_mesh.get_xdata(),
            color_mesh.get_ydata(),
            color_mesh.get_color(),
            cmap=color_mesh.get_cmap()
        )
        self._mpl_quad_mesh = mpl_quad_mesh
    
    # ...............{ PUBLIC METHODS                           }..............
    # +-----------------------------------------------------------------------+
    # Adjusts Figure xlim and ylim when Figure autoscale is not 'none'. It does
    # this by concatenating all artists xdata and ydata and calculating the min
    # and max values.
    # 
    # NOTE: This should only be called once when the Window is shown via 
    # Window.show, and could throw an error when only artists of type Straight
    # or Text are found. This is why the Figure autoscale default is 'none'.
    # +-----------------------------------------------------------------------+
    def update_scale(self):
        if len(self._artists) > 0 or self._color_mesh is not None:
            if len(self._artists) == 0:
                xdata = self._color_mesh.get_xdata()
                ydata = self._color_mesh.get_ydata()
            
            else:
                xdata = np.concatenate(tuple(
                    artist.get_xdata() for artist in self._artists.values()
                ))
                ydata = np.concatenate(tuple(
                    artist.get_ydata() for artist in self._artists.values()
                ))
            
                if self._color_mesh is not None:
                    xdata = np.concatenate((
                        xdata, self._color_mesh.get_xdata().flatten()
                    ))
                    ydata = np.concatenate((
                        ydata, self._color_mesh.get_ydata().flatten()
                    ))

            x_min, x_max = np.min(xdata), np.max(xdata)
            y_min, y_max = np.min(ydata), np.max(ydata)

            match self._autoscale:
                case 'all':
                    self._mpl_ax.set_xlim(x_min, x_max)
                    self._mpl_ax.set_ylim(y_min, y_max)
                case 'width':
                    self._mpl_ax.set_xlim(x_min, x_max)
                case 'height':
                    self._mpl_ax.set_ylim(y_min, y_max)
                case _:
                    pass

    def add_color_mesh(self, color_mesh: ColorMesh, overwrite: bool = False):
        if self._color_mesh is not None:
            if overwrite:
                self.remove_color_mesh()
            else:
                raise AssertionError(e.IndexError(
                    'Figure', 'color_mesh', 'color_mesh', overwrite=True
                ))
        
        self._add_mpl_quad_mesh(color_mesh)
        self._color_mesh = color_mesh

    def remove_color_mesh(self):
        assert self._color_mesh, e.IndexError(
            'Figure', 'color_mesh', 'color_mesh', 
            action='remove ColorMesh from Figure'
        )
        self._color_mesh = None
        self._mpl_quad_mesh.remove()
        self._mpl_quad_mesh = None

    def straight(
        self, 
        xy,
        dir,
        name: str, 
        c='k', 
        lw=1, 
        ls='solid', 
        label='', 
        overwrite=False
    ):
        straight = Straight(xy, dir, name, c, lw, ls)
        self.add_artist(straight, label, overwrite)
        return straight

    def plot(
        self, 
        x, 
        y, 
        name: str, 
        c='k', 
        lw=1, 
        ls='solid', 
        label='', 
        overwrite=False
    ):
        line = Line(x, y, name, c, lw, ls)
        self.add_artist(line, label, overwrite)
        return line

    def scatter(
        self, 
        x, 
        y, 
        name: str, 
        c='k', 
        s=1, 
        label='',
        overwrite=False,
    ):
        points = Points(x, y, name, c, s)
        self.add_artist(points, label, overwrite)
        return points
    
    def arrows(
        self,
        x,
        y,
        u,
        v,
        name: str,
        c=0,
        pivot: str = 'mid',
        label: str = '',
        overwrite: bool = False,
    ):
        arrows = Arrows(x, y, u, v, name, c, pivot)
        self.add_artist(arrows, label, overwrite)
        return arrows

    def text(
        self,
        x: int | float,
        y: int | float,
        text: str,
        name: str,
        c: str = 'k',
        s: int | float = 10,
        coord_type: str = 'data',
        offset: tuple = (0, 0),
        overwrite: bool = False,
    ):
        text_obj = Text(x, y, text, name, c, s, coord_type, offset)
        self.add_artist(text_obj, overwrite=overwrite)
        return text_obj

    def color_mesh(
            self,
            X,
            Y,
            C,
            cmap: str = 'plasma',
            overwrite: bool = False
    ):
        color_mesh = ColorMesh(X, Y, C, cmap)
        self.add_color_mesh(color_mesh, overwrite)
        return color_mesh

    # ...............{ PROPERTIES                               }..............
    def get_mpl_quad_mesh(self):
        return self._mpl_quad_mesh

    def get_autoscale(self):
        return self._autoscale
    
    def set_autoscale(self, autoscale='all'):
        assert autoscale in Figure.AUTOSCALE_OPTIONS, e.OptionsError(
            'Figure', 'autoscale', options=Figure.AUTOSCALE_OPTIONS
        )
        self._autoscale = autoscale
        return autoscale


class Figure3D(_Figure):
    # ...............{ DUNDERS                                  }..............
    def __init__(
        self,
        mpl_fig,
        mpl_ax,
        xlabel='',
        ylabel='',
        zlabel='',
        title='',
    ):
        super().__init__(mpl_fig, mpl_ax, xlabel, ylabel, title)
        mpl_ax.set_zlabel(zlabel)
        self._mpl_surf = None

    # ...............{ PRIVATE METHODS                          }..............
    def _add_mpl_artist(self, artist: Artist3D, label: str):
        if isinstance(artist, Line3D):
            self._add_mpl_line(artist, label)
        elif isinstance(artist, Points):
            self._add_mpl_scatter(artist, label)
        elif isinstance(artist, Text3D):
            self._add_mpl_annotation(artist)
        else:
            raise NotImplementedError()
    
    # draws Line3D via matplotlib.pyplot.plot
    def _add_mpl_line(self, line_3d, label):
        (mpl_line,) = self._mpl_ax.plot(
            line_3d.get_xdata(), 
            line_3d.get_ydata(), 
            line_3d.get_zdata(),
            color=line_3d.get_color(), 
            linewidth=line_3d.get_linewidth(),
            linestyle = line_3d.get_linestyle(),
            label=label,
        )
        self._mpl_artists[line_3d.get_name()] = mpl_line

    # draws Points3D via matplotlib.pyplot.scatter
    def _add_mpl_scatter(self, points_3d, label):
        mpl_path_collection = self._mpl_ax.scatter(
            points_3d.get_xdata(), 
            points_3d.get_ydata(), 
            points_3d.get_zdata(),
            c=points_3d.get_color(), 
            s=points_3d.get_mpl_size(), 
            label=label,
        )
        self._mpl_artists[points_3d.get_name()] = mpl_path_collection

    # draws Text3D via matplotlib.pyplot.annotate3D
    def _add_mpl_annotation(self, text):
        mpl_annotation = self._mpl_ax.annotate3D(
            text.get_text(),
            (text.get_xdata()[0], text.get_ydata()[0], text.get_zdata()[0]),
            xytext=text.get_offset(),
            textcoords='offset points',
            color=text.get_color(),
            fontsize=text.get_size()
        )
        self._mpl_artists[text.get_name()] = mpl_annotation

    # draws ColorMesh via matplotlib.pyplot.plot_surface
    def _add_mpl_surf(self, color_mesh):
        mpl_surf = self._mpl_ax.plot_surface(
            color_mesh.get_xdata(),
            color_mesh.get_ydata(),
            color_mesh.get_color(),
            cmap=color_mesh.get_cmap()
        )
        self._mpl_surf = mpl_surf

    # ...............{ PUBLIC METHODS                           }..............
    def add_color_mesh(
        self, 
        color_mesh: ColorMesh, 
        overwrite: bool = False
    ):
        if self._color_mesh is not None:
            if overwrite:
                self.remove_color_mesh()
            else:
                raise AssertionError(e.IndexError(
                    'Figure3D', 'color_mesh', 'color_mesh', 
                    overwrite=True
                ))
        
        self._add_mpl_surf(color_mesh)
        self._color_mesh = color_mesh

    def remove_color_mesh(self):
        assert self._color_mesh, e.IndexError(
            'Figure3D', 'color_mesh', 'color_mesh', 
            action='remove ColorMesh from Figure3D'
        )
        self._color_mesh = None
        self._mpl_surf.remove()
        self._mpl_surf = None
    
    def plot3D(
        self, 
        x, 
        y, 
        z, 
        name: str, 
        c: str = 'k', 
        lw: int | float = 1.0, 
        ls: str = 'solid',
        label: str = '', 
        overwrite: bool = False,
    ):
        line_3d = Line3D(x, y, z, name, c, lw, ls)
        self.add_artist(line_3d, label, overwrite)
        return line_3d

    def scatter3D(
        self, 
        x, 
        y, 
        z, 
        name: str, 
        c='k', 
        s=1.0,
        label: str = '',
        overwrite: bool = False,
    ):
        points_3d = Points3D(x, y, z, name, c, s)
        self.add_artist(points_3d, label, overwrite)
        return points_3d
    
    def text3D(
        self,
        x: int | float,
        y: int | float,
        z: int | float,
        text: str,
        name: str,
        c: str = 'k',
        s: int | float = 10,
        coord_type: str = 'data',
        offset: tuple = (0, 0),
        overwrite: bool = False,
    ):
        text_3d_obj = Text3D(x, y, z, text, name, c, s, coord_type, offset)
        self.add_artist(text_3d_obj, overwrite=overwrite)
        return text_3d_obj
    
    def color_mesh(
        self,
        X,
        Y,
        Z,
        cmap: str = 'plasma',
        overwrite: bool = False
    ):
        color_mesh = ColorMesh(X, Y, Z, cmap)
        self.add_color_mesh(color_mesh, overwrite)
        return color_mesh
    

    # ...............{ PROPERTIES                               }..............
    def get_mpl_surf(self):
        return self._mpl_surf


class Legend:
    # ...............{ DUNDERS                                  }..............
    def __init__(
        self, 
        figure: _Figure,
    ):
        self._figure = figure
        self._mpl_legend = figure.get_mpl_ax().legend(handles=[])
        self._artists = {}

        self._update()

    # ...............{ PRIVATE METHODS                          }..............
    # updates the Legend by searching for current artists
    def _update(self):
        mpl_handles = [
            self._figure.get_mpl_artists()[name] for name in self._artists
        ]
        if len(mpl_handles) > 0:
            self._mpl_legend = self._figure.get_mpl_ax().legend(
                handles=mpl_handles
            )
            self._mpl_legend.set_visible(True)
        else:
            self._mpl_legend.set_visible(False)

    # ...............{ PUBLIC METHODS                           }..............
    def add(self, names: list | tuple | np.ndarray | str = 'all'):
        if isinstance(names, str):
            assert names == 'all', (
                'Tried to add Artist to Figure Legend, but `names` is '
                'invalid. Make sure `names` is of type list | tuple | '
                'numpy.ndarray, or use the keyword \'all\' to add all Artists '
                'to the Figure Legend.'
            )

            self._artists = {
                name: artist 
                for name, artist in self._figure.get_artists().items() 
                if not isinstance(artist, Text)
            }

        else:
            assert all((
                name in self._figure.get_artists() and not 
                isinstance(self._figure.get_artists()[name], Text)
            ) for name in names), e.IndexError(
                'Legend', 'artist', 
                add_msg='Maybe Artist is of type pygraph.artists.Text.'
            )

            self._artists |= {
                name: self._figure.get_artists()[name] for name in names
            }

        self._update()

    def remove(self, names: list | tuple | np.ndarray | str = 'all'):
        if isinstance(names, str):
            assert names == 'all', (
                'Tried to remove Artist from Figure Legend, but `names` is '
                'invalid. Make sure `names` is of type list | tuple | '
                'numpy.ndarray, or use the keyword \'all\' to remove all '
                'Artists from the Figure Legend.'
            )

            self._artists = {}

        else:
            for name in names:
                assert (
                    name in self._figure.get_artists() and not 
                    isinstance(self._figure.get_artists()[name], Text)
                ), e.IndexError(
                    'Legend', 'artist', action='remove Artist from Legend',
                    add_msg='Maybe Artist is of type pygraph.artists.Text.'
                )

                self._artists.pop(name)

        self._update()
        
    # ...............{ PROPERTIES                               }..............
    def get_mpl_legend(self):
        return self._mpl_legend
        
    def get_artists(self):
        return self._artists