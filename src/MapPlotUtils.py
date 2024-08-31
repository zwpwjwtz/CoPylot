#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python script for plotting maps of data points.

Following third-party libraries are required:
    matplotlib
"""

import math
import matplotlib
import matplotlib.pyplot as PyPlot
import matplotlib.colors as Colors


def heatmap2D(Z: list, X = None, Y = None, filename = '', 
              inverseX = False, inverseY = True, transpose = False, 
              paletteName = 'viridis', colorNA = 'white', 
              xLabel = None, yLabel = None, 
              fillLabel = None, fillLogScale = False, 
              rotateLabelX = 45, rotateLabelY = 0) -> object:
    """
    Draw a 2-D heatmap.

    Parameters
    ----------
    Z : list
        A list of list of numeric values representing the data points.
        The length of the outer list equals to the grid number on the 
        horizontal direction, and the length of the inner list equals to 
        the grid number on the vertical direction.
    X : list or NoneType, optional
        A list of numeric values representing the axis ticks on the 
        horizontal axis. The default is None.
    Y : list or NoneType, optional
        A list of numeric values representing the axis ticks on the 
        vertical axis. The default is None.
    filename : str, optional
        A string indicating the target image file to which the plot is saved. 
        The default is an empty string, i.e. no file will be generated.
    inverseX : bool, optional
        Whether the order of grids should be inverted on the 
        horizontal direction. The default is False.
    inverseY : bool, optional
        Whether the order of grids should be inverted on the 
        vertical direction. The default is True.
    transpose : bool, optional
        Whether the data matrix Z should be transpose before plotted.
        The default is False.
    paletteName : str, optional
        A string indicating the name of the built-in palette.
        The default is 'viridis'.
    colorNA : str, optional
         A string indicating the color for invalid values (NaN).
         The default is 'white'.
    xLabel : str or NoneType, optional
        A string used as a title for the x axis, or None if no title. 
        The default is None
    yLabel : str or NoneType, optional
        A string used as a title for the y axis, or None if no title.
        The default is None.
    fillLabel : str or NoneType, optional
        A string used as a title for the color bar, or None if no title. 
        The default is None.
    fillLogScale : bool, optional
        A boolean indicating whether the ticks on the color bar should be of 
        logarithm scale. 
        The default is False.
    rotateLabelX : float, optional
        A numeric value indicating the angle of tick labels on the X axis.
        The default is 45 (degrees).
    rotateLabelY : float, optional
        A numeric value indicating the angle of tick labels on the Y axis.
        The default is 0 (degrees).

    Returns
    -------
    object
        An object of class 'matplotlib.Figure' holding the heatmap plot.
    """
    figure, axes = PyPlot.subplots()
    if len(Z) == 0 or len(Z[0]) == 0:
        return figure
    if transpose:
        Z = [[math.nan if W is None else W for W in V] for V in Z]
    else:
        Z = [[math.nan if z[i] is None else z[i] for z in Z] 
             for i in range(0, len(Z[0]))]
    
    if fillLogScale:
        norm = Colors.LogNorm()
    else:
        norm = None
    
    colorMap = matplotlib.colormaps[paletteName]
    colorMap.set_bad(colorNA)
    heatmap = axes.imshow(Z, norm = norm, cmap = colorMap)
    colorbar = figure.colorbar(heatmap, shrink = 0.75)
    
    if X is not None:
        axes.set_xticks([i for i in range(0, len(X)) if X[i] is not None], 
                        labels = [x for x in X if x is not None], 
                        rotation = rotateLabelX)
    if Y is not None:
        axes.set_yticks([i for i in range(0, len(Y)) if Y[i] is not None], 
                        labels = [y for y in Y if y is not None], 
                        rotation = rotateLabelY)
    if inverseX:
        axes.invert_xaxis()
    if inverseY:
        axes.invert_yaxis()
    
    if xLabel is not None:
        axes.set_xlabel(xLabel)
    if yLabel is not None:
        axes.set_ylabel(yLabel)
    if fillLabel is not None:
        colorbar.ax.set_ylabel(fillLabel)
    
    # Save the plot to a file if needed
    if len(filename) > 0:
        figure.savefig(filename, format = 'png')
    
    return figure
