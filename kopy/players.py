# encoding: utf-8
"""
In the Key of Python (version 0.1)
Players

A Player is like a musician. The player receives orders from the Composer and uses Instruments
from the Instrument Rack to make a new Track which it sends back to the Composer. The Composer 
puts that Track with others to make a song which gets written as a wav file.

Players take as inputs from Composers:
  - instrument
  - barlines
  - chords
  - bpm
  - volume

Players give Instruments inputs like:
  - freq
  - volume
  - attack
  - sustain
  - decay
  - duration

"""

__all__ = ["sloppychords","bassplayer"]

import numpy as np
import pylab as pb
import scipy.io.wavfile
import wave as kp
import random

def sloppychord(instrument,barlines,chords,bpm=120,volume=4): 
  assert len(barlines)==len(chords), "need one chord per bar"
  sloppiness=0.25 ## in units of beats
  T=kp.Track(bpm=bpm)
  for i in range(len(barlines)):
    barline=barlines[i]
    chord=chords[i]
    for note in chord:
      T.add(instrument(note,volume=volume,bpm=bpm),beat=barline+random.gauss(0,sloppiness))
  return T
  
def bassplayer(instrument,barlines,chords,bpm=120,volume=4):
  assert len(barlines)==len(chords), "need one chord per bar"
  T=kp.Track(bpm=bpm)
  for i in range(len(barlines)-1):
    barline=barlines[i]
    chord=chords[i] 
    T.add(instrument(chord[0]/2,duration=(barlines[i+1]-barline),attack=0.01,sustain=1.5,decay=0.25,bpm=bpm,volume=volume),beat=barline)
  return T
  
  