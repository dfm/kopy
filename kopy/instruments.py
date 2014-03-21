# encoding: utf-8
"""
In the Key of Python (version 0.1)
Instrument Rack.

An instrument is a function that returns a single note in the form of a Track object. It accepts
as arguments any subset of the following:
  - frequency
  - volume [1 is reasonable, 10 is max]
  - duration
  - attack [units of seconds]
  - sustain [units of seconds]
  - decay [units of seconds]
  ? bpm
  ? other...

"""

__all__ = ["bell","drone"]

import numpy as np
import pylab as pb
import scipy.io.wavfile
import wave as kp
import random
#sps=kp.sps

def bell(freq=440.,volume=1.0,duration=None,attack=0.001,sustain=None,decay=0.5,bpm=120):
  assert freq<2000., "bells don't go that high"
  A=10**((volume-10.0)/3)
  t=np.arange(0.0,5.0,1./kp.sps)
  data=np.zeros([len(t),2])
  data[:,0]=A*np.sin(2*np.pi*t*freq)*np.exp(-t/decay)
  data[:,1]=data[:,0]
  W=kp.Wave(data=(kp.sps,data))
  return kp.Track(Wave=W,zero=0)
  
def drone(freq=440.,volume=1.0,duration=4.0,attack=0.1,sustain=None,decay=0.1,bpm=120):
  assert freq<600., "drones shouldn't be high... that's annoying"
  A=10**((volume-10.0)/3)
  t_cut=duration*60./bpm
  t_end=(duration+4)*60/bpm
  t=np.arange(0.0,t_end,1./kp.sps)
  drfreq=bpm/60.*random.randint(1,2)
  depth=0.1+0.2*random.random()
  Amp=(1-depth)*A+depth*A*np.cos(2*np.pi*t*drfreq)
  dt=np.sin(2*np.pi*t*freq)*(1-np.exp(-t/attack))
  dt=Amp*dt
  dt[t>t_cut]=dt[t>t_cut]*np.exp(-(t[t>t_cut]-t_cut)/decay)
  if sustain!=None:dt*=np.exp(-t/sustain)
  data=np.zeros([len(t),2])
  data[:,0]=dt
  data[:,1]=dt
  W=kp.Wave(data=(kp.sps,data))
  return kp.Track(Wave=W,zero=0)
  
  
  
  