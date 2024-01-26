#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python script for plotting contours of data points.

Following third-party libraries are required:
    matplotlib
"""

import matplotlib.pyplot as PyPlot
import matplotlib.ticker as Ticker


def contour2D(X: list, Y: list, Z: list, filename = '', 
              xLogScale = False, yLogScale = False, 
              xlim = None, ylim = None, fillRange = None, 
              xLabel = 'x', yLabel = 'y', fillLabel = '', 
              fillTickCount = 11, fillLogScale = False, 
              fillLogScaleBase = 2) -> object:
    '''
    Draw a 2-D contour plot filled with colors.

    Parameters
    ----------
    X : list
        A list of numeric values representing the data point projected 
        on the X (horizontal) axis.
    Y : list
        A list of numeric values representing the data point projected 
        on the Y (vertical) axis.
    Z : list
        A list of list of numeric values representing the data points.
        The length of the outer list should equal to that of 'X', and 
        the length of the inner list should equal to that of 'Y'.
    filename : str, optional
        A string indicating the target image file to which the plot is saved. 
        The default is an empty string, i.e. no file will be generated.
    xLogScale : bool, optional
        A boolean indicating whether the x axis should be of logarithm scale. 
        The default is False.
    yLogScale : bool, optional
        A boolean indicating whether the y axis should be of logarithm scale. 
        The default is False.
    xlim : tuple or NoneType, optional
        A tuple of (int, int), indicating the left (lower) bound and the right 
        (upper) bound of the X axis. 
        The default is None, i.e. the axis range is automatically determined 
        from the data range.
    ylim : tuple or NoneType, optional
        A tuple of (int, int), indicating the left (lower) bound and the right 
        (upper) bound of the Y axis. 
        The default is None, i.e. the axis range is automatically determined 
        from the data range.
    xLabel : str, optional
        A string used as a title for the x axis. The default is 'x'.
    yLabel : str, optional
        A string used as a title for the y axis. The default is 'y'.
    fillLabel : str, optional
        A string used as a title for the color bar. 
        The default is an empty string.
    fillTickCount : int, optional
        An integer indicatin ghte number of ticks on the color bar. 
        The default is 11.
    fillLogScale : bool, optional
        A boolean indicating whether the ticks on the color bar should be of 
        logarithm scale. 
        The default is False.

    Returns
    -------
    object
        An object of class 'matplotlib.Figure' holding the contour plot.
    '''
    figure, axes = PyPlot.subplots()
    if len(X) == 0 or len(Y) == 0 or len(X) != len(Z) or len(Y) != len(Z[0]):
        return figure
    
    if fillLogScale:
        tickerLocator = Ticker.LogLocator(base = fillLogScaleBase, 
                                          numticks = fillTickCount)
    else:
        tickerLocator = Ticker.LinearLocator(numticks = fillTickCount)
    
    contour = axes.contourf(X, Y, 
                            [[z[i] for z in Z] for i in range(0, len(Z[0]))], 
                            locator = tickerLocator, cmap = 'turbo')
    colorbar = figure.colorbar(contour)
    if len(fillLabel) > 0:
        colorbar.ax.set_ylabel(fillLabel)
    axes.set_xscale('log' if xLogScale else 'linear')
    axes.set_yscale('log' if yLogScale else 'linear')
    if xlim != None:
        axes.set_xlim(xlim)
    if ylim != None:
        axes.set_ylim(ylim)
    if fillRange != None:
        contour.set_clim(fillRange)
    axes.set_xlabel(xLabel)
    axes.set_ylabel(yLabel)
    if len(filename) > 0:
        figure.savefig(filename, format = 'png')
    return figure

def contour2Dscatter(X: list, Y: list, Z: list, scatterX: list, scatterY: list,
                     colors = None, labels = None, marker = 'o', sizes = None, 
                     **kwargs) -> object:
    """
    Draw a 2-D contour plot plus several points.
    
    Parameters
    ----------
    X : list
        A list of numeric values representing the data point projected 
        on the X (horizontal) axis.
    Y : list
        A list of numeric values representing the data point projected 
        on the Y (vertical) axis.
    Z : list
        A list of list of numeric values representing the data points.
        The length of the outer list should equal to that of 'X', and 
        the length of the inner list should equal to that of 'Y'.
    scatterX : list
        A list of numeric values representing the horizontal coordinate 
        of data points in the additional scatter plot.
    scatterY : list
        A list of numeric values representing the vertical coordinate 
        of data points in the additional scatter plot.
    colors: list or NoneType, optional
        A list of strings, corresponding to the color of each data point 
        in the additional scatter plot. 
        The default is None, i.e. the default color ('1F77B4') will be used.
    labels : list or NoneType, optional
        A list of strings, corresponding to the label of each data point 
        in the additional scatter plot. 
        The default is None, i.e. no data label will be drawn.
    marker: str, optional
        A string representing the marker sign.
        The default is 'o', i.e. a circle will be drawn on each data point 
        in the additional scatter plot. 
    sizes : list or NoneType, optional
        A list of numeric values, corresponding to size of each data point 
        in the additional scatter plot. 
        The default is None.
    **kwargs : dict
        Additional arguments passed to function **contour2D**.

    Returns
    -------
    object
        An object of class 'matplotlib.Figure' holding the contour plot 
        and the scatter plot.
    """
    figure = contour2D(X, Y, Z, **kwargs)
    
    axes = figure.axes[0]
    axes.scatter(scatterX, scatterY, s = sizes, c = colors, marker = marker)
    if labels != None:
        for x, y, label in zip(scatterX, scatterY, labels):
            axes.annotate(label, (x, y), textcoords = 'offset points',
                          xytext = (0, 2), ha = 'center')
    if 'filename' in kwargs and len(kwargs['filename']) > 0:
        figure.savefig(kwargs['filename'], format = 'png')
    return figure

def contour2DVLine(X: list, Y: list, Z: list, x0: list, 
                   colors = None, styles = None,  **kwargs) -> object:
    """
    Draw a 2-D contour plot plus several vertical lines.
    
    Parameters
    ----------
    X : list
        A list of numeric values representing the data point projected 
        on the X (horizontal) axis.
    Y : list
        A list of numeric values representing the data point projected 
        on the Y (vertical) axis.
    Z : list
        A list of list of numeric values representing the data points.
        The length of the outer list should equal to that of 'X', and 
        the length of the inner list should equal to that of 'Y'.
    x0 : list
        A list of numeric values representing the horizontal coordinate 
        of vertical lines in the additional line plot.
    colors: list or NoneType, optional
        A list of strings, corresponding to the color of each additional lines.
        The default is None, i.e. the default color ('1F77B4') will be used.
    styles: str, optional
        A list of strings indicating the style of each verticle line.
        The default is None, i.e. the default style ('-') will be used.
    **kwargs : dict
        Additional arguments passed to function **contour2D**.

    Returns
    -------
    object
        An object of class 'matplotlib.Figure' holding the contour plot 
        and the line plot.
    """
    figure = contour2D(X, Y, Z, **kwargs)
    
    if type(x0) != list:
        x0 = [x0]
    if type(colors) != list:
        colors = [colors] * len(x0)
    if type(styles) != list:
        styles = [styles] * len(x0)
    for X, color, style in zip(x0, colors, styles):
        figure.axes[0].axvline(X, color = color, linestyle = style)
    if 'filename' in kwargs and len(kwargs['filename']) > 0:
        figure.savefig(kwargs['filename'], format = 'png')
    return figure
