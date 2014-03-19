# encoding: utf-8
"""
In the Key of Python (version 0.1)

"""

__all__ = ["Wave"]

import numpy as np
import scipy.io.wavfile

class Wave(object):
  def __init__(self, filename=None, data=None):
    assert (filename is None) != (data is None), \
            "You must specify a filename or provide data."
    if filename is not None:
      self.sps, self.data = scipy.io.wavfile.read(filename)
    elif data is not None:
      self.sps, self.data = data

    self.channels = self.data.shape[1] # This should be 1 or 2
    assert self.channels in [1,2], \
            "Wave can only load mono or stereo files."

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

  # Nice, eh?
  @property
  def left(self):
    return self.get_channel(0)

  @property
  def right(self):
    return self.get_channel(1)

  @property
  def time(self):
    return np.arange(self.data.shape[0], dtype=float)/self.sps

  def __getitem__(self, ind):
    return self.data[ind] ## I like this better: let's you look at data with Wave[0:50,:]
    #return Wave(data=(self.sps, self.data[ind]))
      
  def __setitem__(self,key,val):
    if type(val)==np.ndarray:
      assert len(val.shape) in [1,2], "can only assign 1D arrays or 2D arrays"
      if val.shape==self.data[key].shape: pass
      elif len(val.shape)==1: ## 1D array
        assert len(val)==self.data[key].shape[0], "lengths don't match"
        self.data[key][:,0]=val
        self.data[key][:,1]=val
        return
      elif len(val.shape)==2: ## 2D array
        assert val.shape[0]==self.data[key].shape[0], "lengths don't match"
    self.data[key]=val
    return

