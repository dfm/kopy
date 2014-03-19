import sys
import random
import numpy as np
import pylab as pb
import scipy.io.wavfile
import kopy as kp

def main():
  sps=41000
  data=np.zeros([8.2*sps,2])
  W=kp.Wave(data=(sps,data))
  W[:]=0.01*np.sin(2*np.pi*440*W.time)
  W.write('testwav.wav')
  return

if __name__=='__main__':
  main()


