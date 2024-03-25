#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python script for splitting axes in figures.

Following third-party libraries are required:
    matplotlib
"""

import matplotlib.pyplot as PyPlot
import matplotlib.figure as Figure
import matplotlib.artist as Artist
import matplotlib.axis as Axis
import matplotlib.collections as Collections
import matplotlib.lines as Lines
import matplotlib.patches as Patches
import matplotlib.spines as Spine
import matplotlib.text as Text


def cloneArtist(artist: Artist.Artist, axes = None) -> Artist.Artist:
    '''
    Duplicate a paintable element (artist)

    Parameters
    ----------
    artist : Artist
        An object of class 'matplotlib.artist.Artist' to duplicate.
    axes : Axes or NoneType, optional
        An object of class 'matplotlib.axes.Axes' to which 
        the duplicated element is attached.
        The default is None, i.e. the duplicated element is free.

    Returns
    -------
    Artist
        An object of class 'matplotlib.artist.Artist' holding 
        the duplicated element.
    '''
    if isinstance(artist, Collections.PathCollection):
        data = artist.get_offsets().data.T
        newArtist = axes.scatter(data[0], data[1])
        newArtist.set_facecolors(artist.get_facecolors())
        newArtist.set_edgecolors(artist.get_edgecolors())
    elif isinstance(artist, Axis.Axis):
        newArtist = artist.__class__(axes)
    elif isinstance(artist, Lines.Line2D):
        newArtist = artist.__class__(artist.get_xdata(), artist.get_ydata(),
                                     color = artist.get_color())
    elif isinstance(artist, Patches.Rectangle):
        newArtist = artist.__class__(artist.xy, 
                                     artist.get_width(), artist.get_height())
    elif isinstance(artist, Spine.Spine):
        newArtist = artist.__class__(axes, artist.spine_type, 
                                     artist.get_path())
    elif isinstance(artist, Text.Text):
        newArtist = artist.__class__(artist.get_position()[0], 
                                     artist.get_position()[1], 
                                     artist.get_text())
    else:
        raise TypeError('The artist of type "{}" cannot be cloned.'.
                        format(type(artist)))
    
    return newArtist

def splitAxes(figure: Figure, filename = '', fileFormat = 'png', 
              xSubranges = [], ySubranges = [], xRatio = [], yRatio = [],
              xSpacing = 0.05, ySpacing = 0.05) -> Figure.Figure:
    '''
    Split the axes in a plot into subplots and create broken axes

    Parameters
    ----------
    figure : Figure
        An object of class 'matplotlib.Figure' to split.
    filename : str, optional
        A string indicating the target image file to which the plot is saved. 
        The default is an empty string, i.e. no file will be generated.
    fileFormat : str, optional
        A string indicating the format of target image file.
        The default is 'png'.
    xSubranges : list, optional
        A list of tuples of (float, float) indicating the limit of horizontal 
        axis for each splitted plot.
        The default is an empty list, i.e. no splitting on the horizontal axis.
    ySubranges : list, optional
        A list of tuples of (float, float) indicating the limit of vertical 
        axis for each splitted plot.
        The default is an empty list, i.e. no splitting on the vertical axis.
    xRatio : list, optional
        A list of float numbers between 0 and 1 indicating the relative width 
        for each splitted plot.
        The default is an empty list, i.e. no splitting on the horizontal axis.
    yRatio : list, optional
        A list of float numbers between 0 and 1 indicating the relative height 
        for each splitted plot.
        The default is an empty list, i.e. no splitting on the vertical axis.
    xSpacing : float, optional
        A float number indicating the horizontal spacing between splitted plot.
        The default is 0.05.
    ySpacing : float, optional
        A float number indicating the vertical spacing between splitted plot.
        The default is 0.05.

    Returns
    -------
    Figure
        An object of class 'matplotlib.Figure' holding the splitted plot.
    '''
    if len(figure.axes) == 0:
        return figure
    
    # Determine the number of column and row
    columnCount = max(len(xSubranges), 1)
    rowCount = max(len(ySubranges), 1)
    if len(xRatio) < columnCount:
        xRatio = xRatio + \
                 [(1 - sum(xRatio)) / (columnCount - len(xRatio))] * \
                 (columnCount - len(xRatio))
    if len(yRatio) < rowCount:
        yRatio = yRatio + \
                 [(1 - sum(yRatio)) / (rowCount - len(yRatio))] * \
                 (rowCount - len(yRatio))
    
    # Inverse the parameter order for the vertical axis
    ySubranges = ySubranges[::-1]
    yRatio = yRatio[::-1]
    
    # Draw a new figure with the specified layout
    newFigure, _ = PyPlot.subplots(rowCount, columnCount, 
                                   gridspec_kw = {'width_ratios': xRatio, 
                                                  'height_ratios': yRatio}, 
                                   sharex = columnCount < 2, 
                                   sharey = rowCount < 2)
    newFigure.subplots_adjust(hspace = ySpacing if columnCount else None, 
                              wspace = xSpacing if rowCount else None)
    
    # Add artists in the existing plot to each subplot in the new plot
    axes = figure.axes[0]
    artists = axes.get_children()
    for i in range(0, columnCount):
        for j in range(0, rowCount):
            newAxes = newFigure.axes[i + j * rowCount]
            for artist in artists:
                if not any(isinstance(artist, X) 
                           for X in 
                           (Axis.Axis, Patches.Patch, Spine.Spine, Text.Text)):
                    newAxes.add_artist(cloneArtist(artist, newAxes))
            if len(xSubranges) > 0 and i < len(xSubranges):
                newAxes.set_xlim(xSubranges[i])
            else:
                newAxes.set_xlim(axes.get_xlim())
            if len(ySubranges) > 0 and j < len(ySubranges):
                newAxes.set_ylim(ySubranges[j])
            else:
                newAxes.set_ylim(axes.get_ylim())
            newAxes.set_xscale(axes.get_xscale())
            newAxes.set_yscale(axes.get_yscale())
            newAxes.tick_params(bottom = (j == rowCount - 1), 
                                labelbottom = (j == rowCount - 1), 
                                top = False, 
                                left = (i == 0), 
                                labelleft = (i == 0), 
                                right = False)
            newAxes.spines.bottom.set_visible(j == rowCount - 1)
            newAxes.spines.top.set_visible(j == 0)
            newAxes.spines.left.set_visible(i == 0)
            newAxes.spines.right.set_visible(i == columnCount - 1)
            newAxes.xaxis.set_ticks_position('bottom' if j == rowCount - 1 
                                             else 'none')
            newAxes.yaxis.set_ticks_position('left' if i == 0 else 'none')
    
    # Add slanted lines on the axes
    parameters = dict(marker=[(-1, -1), (1, 1)], 
                      markersize = 12, linestyle = 'none', 
                      color = 'black', mew = 1, clip_on = False)
    for i in range(0, columnCount):
        for j in range(0, rowCount):
            newAxes = newFigure.axes[i + j * rowCount]
            if (i > 0) ^ (j < rowCount - 1):
                newAxes.plot([0], [0], transform = newAxes.transAxes, 
                             **parameters)
            if (i < columnCount - 1) ^ (j < rowCount - 1):
                newAxes.plot([1], [0], transform = newAxes.transAxes, 
                             **parameters)
            if (i == 0) ^ (j == 0):
                newAxes.plot([0], [1], transform = newAxes.transAxes, 
                             **parameters)
            if (i < columnCount - 1) ^ (j > 0):
                newAxes.plot([1], [1], transform = newAxes.transAxes, 
                             **parameters)
    
    newFigure.supxlabel(axes.get_xlabel())
    newFigure.supylabel(axes.get_ylabel())
    
    if len(axes.title.get_text()) > 0:
        newFigure.suptitle(axes.title.get_text())
    
    # Save the plot to a file if needed
    if len(filename) > 0:
        newFigure.savefig(filename, format = fileFormat)
    
    return newFigure
