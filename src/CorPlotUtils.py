#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python script for making correlation plots of data series.

Following third-party libraries are required:
    matplotlib
    numpy
"""

import numpy
import matplotlib.figure as Figure
import matplotlib.pyplot as PyPlot


def filterFinite(values: list) -> list:
    return [X != numpy.inf and X != -numpy.inf for X in values]

def scatter(x: list, y: list, filename = '', transform = None, 
            labels = None, colors = None, marker = 'o', 
            linearFit = False, showFormula = False,
            xlim = None, ylim = None, 
            xLogScale = False, yLogScale = False, 
            xLabel = None, yLabel = None, dataLabel = None, 
            legend = False, legendTitle = None, 
            append = None, fileFormat = 'png') -> object:
    '''
    Draw a scatter plot of the correlation between two data series.

    Parameters
    ----------
    x : list
        A list of numeric values representing the data point projected 
        on the X (horizontal) axis.
    y : list
        A list of numeric values representing the data point projected 
        on the Y (vertical) axis.
    filename : str, optional
        A string indicating the target image file to which the plot is saved. 
        The default is an empty string, i.e. no file will be generated.
    transform : object or NoneType, optional
        A callable object used to transform 'x' and 'y' before plotting. 
        The default is None, i.e. no transformation will be applied.
    labels : list or NoneType, optional
        A list of strings, corresponding to the label of each data point. 
        The default is None, i.e. no data label will be drawn.
    colors: list or NoneType, optional
        A list of strings, corresponding to the color of each data point. 
        The default is None, i.e. the default color ('1F77B4') will be used.
    marker: str, optional
        A string representing the marker sign.
        The default is 'o', i.e. a circle will be drawn on each data point.
    linearFit : bool, optional
        A boolean indicating whether a linearly fitted line should be drawn 
        among the data points. The default is False.
    showFormula : bool, optional
        A boolean indicating whether a linearly fitted formula should be 
        drawn alongside the plot. The default is False.
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
    xLogScale : bool, optional
        A boolean indicating whether the x axis should be of logarithm scale. 
        The default is False.
    yLogScale : bool, optional
        A boolean indicating whether the y axis should be of logarithm scale. 
        The default is False.
    xLabel : str or NoneType, optional
        A string used as a title for the x axis, or None if no title. 
        The default is None.
    yLabel : str or NoneType, optional
        A string used as a title for the y axis, or None if no title. 
        The default is None.
    dataLabel : str or NoneType, optional
        A string used to mark the data series in the legend when **legend** 
        == True, or None if no label shall be shown.
        The default is None.
    legend : bool, optional
        A boolean indcating whether the legend box shall be shown.
        The default is False.
    legendTitle : str or NoneType, optional
        A string indicating the title of the legend when **legend** == True, 
        or None if no label shall be shown.
        The default is None.
    append : matplotlib.Figure or NoneType, optional
        An object of matplotlib.Figure to which the scatter plot is appended, 
        or None if a new Figure shall be created. The default is None.
    fileFormat : str, optional
        A string indicating the format of target image file.
        The default is 'png'.

    Returns
    -------
    object
        An object of type 'matplotlib.figure.Figure' holding the scatter plot.
    '''
    # Transform the data before plotting
    if transform != None:
        x = list(map(transform, x))
        y = list(map(transform, y))
    
    # Exclude infinite values
    masks = [X and Y for X, Y in zip(filterFinite(x), filterFinite(y))]
    x = [X for X, mask in zip(x, masks) if mask]
    y = [X for X, mask in zip(y, masks) if mask]
    
    # Get an existing plot
    update = False
    if type(append) == Figure.Figure:
        figure = append
        if len(append.get_axes()) > 0:
            axes = figure.get_axes()[0]
            update = True
        else:
            axes = figure.subplots()
    else:
        figure, axes = PyPlot.subplots()
    
    # Set the axis scale
    if not update:
        axes.set_xscale('log' if xLogScale else 'linear')
        axes.set_yscale('log' if yLogScale else 'linear')
    
    # Make a scatter plot
    axes.scatter(x, y, c = colors, marker = marker, label = dataLabel)
    
    # Add labels alongside points
    if labels != None:
        for pointX, pointY, label in zip(x, y, labels):
            axes.annotate(label, (pointX, pointY), 
                          textcoords = 'offset points',
                          xytext = (0, 2), ha = 'center')
    
    # Draw a linearly fitted curve
    if linearFit:
        a1, a0 = numpy.polyfit(x, y, deg = 1)
        x = sorted(x)
        axes.plot(x, [x0 * a1 + a0 for x0 in x], 'r-')
        if showFormula:
            axes.text(0.7, 0.05, 'y = {:.2} x + {:.2}'.format(a1, a0),
                      transform = axes.transAxes)
    
    # Adjust the plot range
    if xlim != None:
        axes.set_xlim(xlim)
    if ylim != None:
        axes.set_ylim(ylim)
    
    # Set the axis label
    axes.set_xlabel(xLabel)
    axes.set_ylabel(yLabel)
    
    # Set the legend
    if legend:
        axes.legend(loc = 'right', title = legendTitle)
    
    # Save the plot to a file if needed
    if len(filename) > 0:
        figure.savefig(filename, format = fileFormat)
    
    return figure

def scatterCurve(x: list, y: list, curve: object, filename = '', 
                 curveColor = None, curveStyle = '-', curveLabel = None, 
                 samplingDensity = 3, fileFormat = 'png', 
                 **kwargs) -> object:
    '''
    Draw a scatter plot of the correlation between two data series, with a 
    curve alongside the data points.
    
    Parameters
    ----------
    x : list
        A list of numeric values representing the data point projected 
        on the X (horizontal) axis.
    y : list
        A list of numeric values representing the data point projected 
        on the Y (vertical) axis.
    curve: object
        A callable object used to draw the additional curve. It should accept 
        one input (an 'x' value) and give one ouput (a 'y' value).
    filename : str, optional
        A string indicating the target image file to which the plot is saved. 
        The default is an empty string, i.e. no file will be generated.int.
    samplingDensity : int or float, optional
        A numeric value indicating the number of sample points used to 
        interpolate the specified curve.
    curveColor : str or NoneType, optional
        A string corresponding to the color of the additional curve. 
        The default is None, i.e. the default color ('1F77B4') will be used.
    curveStyle : str or NoneType, optional
        A string indicatign the style of the additional curve. 
        The default is '-', i.e. drawing solid lines.
    curveLabel : str or NoneType, optional
        A string used to mark the curve in the legend when **legend** == True, 
        or None if no label for the curve shall be shown.
        The default is None.
    fileFormat : str, optional
        A string indicating the format of target image file.
        The default is 'png'.
    
    **kwargs : dict
        Additional arguments passed to the function **scatter**.
    
    Returns
    -------
    object
        An object of type 'matplotlib.figure.Figure' holding the scatter plot.
    '''
    # Create a base scatter plot
    figure = scatter(x, y, **kwargs)
    axes = figure.get_axes()[0]
    
    # Make a (smooth) line plot
    xLogScale = kwargs.get('xLogScale', False)
    xlim = kwargs.get('xlim', None)
    xRange = (min(x0 for x0 in x if x0 > 0) if xLogScale else min(x), max(x))
    if xlim != None:
        xRange = (xlim[0] if xlim[0] is not None else xRange[0], 
                  xlim[1] if xlim[1] is not None else xRange[1])
    if xLogScale:
        xDense = numpy.logspace(numpy.log(xRange[0]), numpy.log(xRange[1]), 
                                base = numpy.e, 
                                num = len(x) * samplingDensity)
    else:
        xDense = numpy.linspace(xRange[0], xRange[1], 
                                num = len(x) * samplingDensity)
    axes.plot(xDense, [curve(X) for X in xDense], label = curveLabel, 
              color = curveColor, linestyle = curveStyle) 
    
    # Set the legend
    legend = kwargs.get('legend', None)
    if legend:
        axes.legend(loc = 'right', title = kwargs.get('legendTitle', None))
    
    # Save the plot to a file if needed
    if len(filename) > 0:
        figure.savefig(filename, format = fileFormat)
    
    return figure
