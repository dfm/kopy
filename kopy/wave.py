# encoding: utf-8
"""
In the Key of Python (version 0.1)

"""

__all__ = ["sps","bits","Wave","Track"]

sps=4410 ## 44100 is standard
bits=16 ## 8 16 32 -- 32 is good

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
    if 'float' in str(self.data.dtype):
      if np.abs(self.data).mean()>0.05: print "this is going to be loud"
      elif np.abs(self.data).max()>0.3: print "this might have loud parts"
      if bits==8:scaled = np.int16(self.data*127) ## 32 bit signed integer
      elif bits==16:scaled = np.int16(self.data*32767) ## 32 bit signed integer
      elif bits==32:scaled = np.int32(self.data*2147483647) ## 32 bit signed integer
      scipy.io.wavfile.write(fn,self.sps,scaled)
    else:
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
    
  def add(self,Wave2,place=0):
    ## adds starting at place (which can potentially be negative)
    ## what about adding mono to stereo?
    assert self.sps==Wave2.sps, "sample rates need to be the same"
    start=place
    end=place+Wave2.data.shape[0]
    newdata=self.data
    shift=0
    if end<=self.data.shape[0] and start>=0:
      newdata[start:end]+=Wave2.data
    elif end>self.data.shape[0] and start>=0:
      newdata=np.zeros([end,self.data.shape[1]])
      newdata[:self.data.shape[0]]+=self.data
      newdata[start:end]+=Wave2.data
    elif end<=self.data.shape[0] and start<0:
      shift=-start
      newdata=np.zeros([self.data.shape[0]-start,self.data.shape[1]])
      newdata[shift:]+=self.data
      newdata[start+shift:end+shift]+=Wave2.data
    elif end>self.data.shape[0] and start<0:
      shift=-start
      newdata=np.zeros([end+shift,self.data.shape[1]])
      newdata[shift:self.data.shape[0]+shift]+=self.data
      newdata[start+shift:end+shift]+=Wave2.data
    return (Wave(data=(self.sps,newdata)),shift)
    
    
class Track(object): 
  """
  A Track is a layer above a Wave, with some added features like bpm and a zero, which is 
  the index of the zeroth beat (what musicians call "1"). Tracks are meant for manipulating
  already made or acquired samples. A track can be a single note, or an entire take. If 
  you want to edit the actual data, it's probably best to work directly with the Wave. 
  The "add" method is its most important feature.
  """
  def __init__(self, Wave=None, bpm=60, zero=0):
    ## if no bpm is specified, 60 is assumed, so that beats are equivalent to seconds
    self.Wave=Wave
    self.bpm=bpm
    self.zero=zero

  def write(self, fn):
    """
    Write the wave file to disk

    Parameters
    ----------
    fn : str
        The filename to save as

    """
    self.Wave.write(fn)

  def get_channel(self, channel):
    return self.Wave.getchannel(channel)

  @property
  def sps(self):
    return self.Wave.sps
  
  @property
  def data(self):
    return self.Wave.data

  @property
  def left(self):
    return self.get_channel(0)

  @property
  def right(self):
    return self.get_channel(1)

  @property
  def time(self):
    return (np.arange(self.data.shape[0], dtype=float)-self.zero)/self.sps
    
  def add(self,Track2,beat=0):
    if self.Wave==None:
      self.Wave=Track2.Wave
      return
    place=self.zero+beat*self.sps*60/self.bpm-Track2.zero
    self.Wave,shift=self.Wave.add(Track2.Wave,place=place)
    self.zero+=shift
    return
    

