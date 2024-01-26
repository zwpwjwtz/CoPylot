#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python script for plotting distributions of data series.

Following third-party libraries are required:
    matplotlib
    numpy
"""

import numpy
import matplotlib.pyplot as PyPlot


def filterFinite(values: list) -> list:
    return [X != numpy.inf and X != -numpy.inf for X in values]

def hist(x: list, filename = '', transform = None, binCount = 10, 
         color = None, xlim = None, ylim = None) -> object:
    '''
    Draw a histogram of a data series.

    Parameters
    ----------
    x : list
        A list of numeric values representing the data point projected 
        on the X (horizontal) axis.
    filename : str, optional
        A string indicating the target image file to which the plot is saved. 
        The default is an empty string, i.e. no file will be generated.
    transform : object or NoneType, optional
        A callable object used to transform 'x' and 'y' before plotting. 
        The default is None, i.e. no transformation will be applied.
    binCount : int, optional
        An integer indicating the number of equal-width bins to categorize 
        the data points.
        The default is 10.
    color : str or NoneType, optional
        A string indicating the color of each data point. 
        The default is None, i.e. the default color ('1F77B4') will be used.
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

    Returns
    -------
    object
        An object of type 'matplotlib.Figure' holding the scatter plot.
    '''
    # Transform the data before plotting
    if transform != None:
        x = list(map(transform, x))
    
    # Exclude infinite values
    x = [X for X, mask in zip(x, filterFinite(x)) if mask]
    
    # Make a scatter plot
    figure, axes = PyPlot.subplots()
    axes.hist(x, bins = binCount, color = color)
    
    # Adjust the plot range
    if xlim != None:
        axes.set_xlim(xlim)
    if ylim != None:
        axes.set_ylim(ylim)
    
    # Save the plot to a file if needed
    if len(filename) > 0:
        figure.savefig(filename, format = 'png')
    
    return figure

def histVLine(x: list, x0: list, filename = '', transform = None, 
              binCount = 10, color = None, 
              lineColors = None, lineStyles = None, 
              xlim = None, ylim = None) -> object:
    '''
    Draw a histogram of a data series plus several vertical lines.
    
    Parameters
    ----------
    x : list
        A list of numeric values representing the data point projected 
        on the X (horizontal) axis.
    x0 : list
        A list of numeric values indicating the coordinates on the horizontal 
        (X) axis that the vertical lines should intersect.
    filename : str, optional
        A string indicating the target image file to which the plot is saved. 
        The default is an empty string, i.e. no file will be generated.
    transform : object or NoneType, optional
        A callable object used to transform 'x' and 'y' before plotting. 
        The default is None, i.e. no transformation will be applied.
    binCount : int, optional
        An integer indicating the number of equal-width bins to categorize 
        the data points.
        The default is 10.
    color : str or NoneType, optional
        A strings indicating the color of each data point. 
        The default is None, i.e. the default color ('1F77B4') will be used.
    lineColors : list or NoneType, optional
        A list of strings indicating the color of each verticle line.
        The default is None, i.e. the default color ('black') will be used.
    lineStyles : list or NoneType, optional
        A list of strings indicating the style of each verticle line.
        The default is None, i.e. the default style ('-') will be used.
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
    
    Returns
    -------
    object
        An object of type 'matplotlib.Figure' holding the scatter plot.
    '''
    # Transform the data before plotting
    if transform != None:
        x = list(map(transform, x))
    
    # Exclude infinite values
    x = [X for X, mask in zip(x, filterFinite(x)) if mask]
    
    # Make a scatter plot
    figure, axes = PyPlot.subplots()
    axes.hist(x, bins = binCount, color = color)
    
    # Add verticle lines
    if type(x0) != list:
        x0 = [x0]
    if type(lineColors) != list:
        lineColors = [lineColors] * len(x0)
    if type(lineStyles) != list:
        lineStyles = [lineStyles] * len(x0)
    for X, color, style in zip(x0, lineColors, lineStyles):
        axes.axvline(X, color = color, linestyle = style)
    
    # Adjust the plot range
    if xlim != None:
        axes.set_xlim(xlim)
    if ylim != None:
        axes.set_ylim(ylim)
    
    # Save the plot to a file if needed
    if len(filename) > 0:
        figure.savefig(filename, format = 'png')
    
    return figure
