import sys
import random
import numpy as np
import pylab as pb
import scipy.io.wavfile
import kopy as kp

def main():
  sps=44100
  ## first note
  data1=np.zeros([0.125*sps,2])
  W1=kp.Wave(data=(sps,data1))
  W1[:]=0.01*np.sin(2*np.pi*440*W1.time)
  T1=kp.Track(W1,bpm=120)
  
  ## second note
  data2=np.zeros([0.125*sps,2])
  W2=kp.Wave(data=(sps,data2))
  W2[:]=0.01*np.sin(2*np.pi*(440.*2**(3./12))*W2.time)
  T2=kp.Track(W2,bpm=120)
  
  ## make music
  T=kp.Track(bpm=120)
  for i in range(32):
    T.add(T1,beat=2*i)
    T.add(T1,beat=2*i+0.5)
    T.add(T2,beat=2*i+1)
    T.add(T2,beat=2*i+1.75)
  T.write('T.wav')
  
  return

if __name__=='__main__':
  main()


