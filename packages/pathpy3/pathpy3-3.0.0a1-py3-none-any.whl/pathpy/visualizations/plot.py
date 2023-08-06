#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : plot.py -- Module to plot networks as a tikz-network
# Author    : Jürgen Hackl <hackl@ifi.uzh.ch>
# Time-stamp: <Fri 2019-12-20 15:30 juergen>
#
# Copyright (c) 2016-2019 Pathpy Developers
# =============================================================================
from .. import logger
from .easel import D3JS, PDF, CSV, TEX
from .utils import _check_filename

log = logger(__name__)


def plot(self, filename=None, fileformat=None, **kwargs):
    """Plot a network."""

    # initialize plot class
    plt = Plot()

    # plot the network
    plt.plot(self, filename=filename, fileformat=fileformat, **kwargs)
    return plt


class Plot:
    """Plots the network as a tikz-network.

    """

    def __init__(self):
        """Initialize the Plot class."""

        # set default filename
        # TODO: Get this name form the config file
        self.filename = 'default'
        self.fileformat = 'html'

        # supported file fileformats and corresponding easels
        self.fileformats = {'html': D3JS, 'csv': CSV, 'tex': TEX, 'pdf': PDF}

        # initialize easel
        self.easel = None

        # initialize data and config
        self.data = {}
        self.config = {}

    def __call__(self, network=None, filename=None, fileformat=None, **kwargs):
        """Call the plot function and plot or show the results.

        """
        # call the plot function
        self.plot(network=network, filename=filename,
                  fileformat=fileformat, **kwargs)

    def _repr_html_(self):
        self.show()

    def plot(self, network=None, filename=None, fileformat=None, **kwargs):

        # update data and config
        self.data['network'] = network
        self.config.update(**kwargs)

        # check filename and file format
        self.filename, self.fileformat = _check_filename(self, filename,
                                                         fileformat)

        # setup plot environment
        self.easel = self.fileformats[self.fileformat](self.filename)

        # draw object
        self.easel.draw(network, **kwargs)

        # save object
        if filename is not None:
            self.easel.save()

    def save(self, filename=None, fileformat=None):

        # check filename and file format
        _filename, _fileformat = _check_filename(self, filename, fileformat)

        # if no filename and fileformat is given save the default plot
        if filename is None and fileformat is None:
            self.easel.save()

        # if the format is the same save the file with the new name
        elif _fileformat == self.fileformat:
            self.easel.save(_filename)

        # create new plot
        else:
            self.plot(network=self.data['network'],
                      filename=_filename,
                      fileformat=_fileformat,
                      **self.config)

    def show(self, **kwargs):
        self.easel.show(**kwargs)


# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 79
# End:
