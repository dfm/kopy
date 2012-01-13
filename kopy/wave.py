# encoding: utf-8
"""
In the Key of Python (version 0.1)

"""

# here, you should put the names of everything that you want imported when
# you do something like "from marcomod import *"
__all__ = ["Wave"]

#Real code starts here...

# only import what you need...
import numpy as np
import scipy.io.wavfile

class Wave(object): # classes should have capitalized names... and inherit from "object"... don't ask...
    def __init__(self, filename=None, data=None):
        if filename is not None:
            self.sps, self.data = scipy.io.wavfile.read(filename)
        elif data is not None:
            self.sps, self.data = data

        # you don't need a loop to generate this...
        # self.t = np.arange(self.data.shape[0], dtype=float)/self.sps
        # but I prefer using a "property"... see below

        self.channels = len(self.data.shape) # make this work for mono signals
        assert self.channels in [1,2], "You're a tard"

    def write(self, fn):
        """
        Write the wave file to disk

        Parameters
        ----------
        fn : str
            The filename to save as

        """
        scipy.io.wavfile.write(fn,self.sps,self.data)

    def get_channel(self, channel):
        """
        Return the data from a particular channel but also works for mono

        Parameters
        ----------
        channel : int
            Must be either 0=left or 1=right

        Returns
        -------
        data : numpy.ndarray
            Returns the data from the specified channel or the mono signal if
            that's all we got.

        """
        assert channel in [0,1], "You're a tard"
        try:
            return self.data[:,channel]
        except IndexError:
            return self.data

    # below is some crazy Python foo for using properties...
    # you can then access the left and right channels using something like:
    #
    #    W = Wave("example.wav")
    #    R = W.right
    #    L = W.left
    #
    # Nice, eh?
    @property
    def left(self):
        return self.get_channel(0)

    @property
    def right(self):
        return self.get_channel(1)

    # we'll also use a property to access the timestamps because we want it
    # to change if we change "sps", right?
    @property
    def time(self):
        return np.arange(self.data.shape[0], dtype=float)/self.sps

    # and for the grand finale... try to see what this does!
    def __getitem__(self, ind):
        if self.channels == 1 and len(ind) > 1: # make this work for mono
            ind = ind[0]
        return Wave(data=(self.sps, self.data[ind]))

