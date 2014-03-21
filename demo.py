import sys
import random
import numpy as np
import pylab as pb
import scipy.io.wavfile
import kopy as kp
import random
sps=kp.sps

def main():
  
  ## illustrate Wave and Track objects
  # first note
  data1=np.zeros([0.125*sps,2])
  W1=kp.Wave(data=(sps,data1))
  W1[:]=0.01*np.sin(2*np.pi*440*W1.time)
  T1=kp.Track(W1,bpm=120)
  
  # second note
  data2=np.zeros([0.125*sps,2])
  W2=kp.Wave(data=(sps,data2))
  W2[:]=0.01*np.sin(2*np.pi*(440.*2**(3./12))*W2.time)
  T2=kp.Track(W2,bpm=120)
  
  # make music
  T=kp.Track(bpm=120)
  for i in range(32):
    T.add(T1,beat=2*i)
    T.add(T1,beat=2*i+0.5)
    T.add(T2,beat=2*i+1)
    T.add(T2,beat=2*i+1.75)
  T.write('DEMO.wav')
  
  ## try out some instruments
  T=kp.Track(bpm=148)
  freqs=[440*2**(i/12) for i in np.arange(-24,13,dtype=float)]
  beat=0
  while beat<64*20:
    T.add(kp.rack.bell(freq=random.choice(freqs),volume=2), beat=beat)
    beat+=random.randint(1,6)
  T.write('INSTRUMENTS_bell.wav')
  
  D=kp.Track(bpm=148)
  freqs=[440*2**(i/12) for i in np.arange(-30,-6,dtype=float)]
  durations=range(2,8)
  beat=0
  while beat<64*20:
    duration=random.choice(durations)
    D.add(kp.rack.drone(freq=random.choice(freqs),volume=4,duration=duration,bpm=148),beat=beat)
    beat+=duration
  D.write('INSTRUMENTS_drone.wav')
  T.add(D)
  T.write('INSTRUMENTS_both.wav')

  ## try out some players
  barlines=[]
  barline=0
  while barline<64*8:
    if random.random()<0.8:barlines.append(barline)
    barline+=2
    if random.random()<0.2:barlines.append(barline)
    barline+=2
    if random.random()<0.4:barlines.append(barline)
    barline+=2
    if random.random()<0.2:barlines.append(barline)
    barline+=2
    
  chords=[]
  chtypes={'maj9':[0,4,7,11,14],
    'min9':[0,3,7,10,14],
    'dom':[0,4,7,10,14],
    'majmin':[0,3,7,11],
    'stack4':[0,5,10,15,20],
    'stack5':[0,7,14,21,28,35]
    }
  
  for barline in barlines:
    fundamental=110.*2**(random.randint(0,12)/12.)
    intervals=random.choice(chtypes.values())
    chord=fundamental*2**(np.array(intervals)/12.)
    chords.append(chord)
  T=kp.plyr.sloppychord(kp.rack.bell,barlines,chords,bpm=148)
  T.write('PLAYERS_sloppychord.wav')
  T2=kp.plyr.bassplayer(kp.rack.drone,barlines,chords,bpm=148)
  T2.write('PLAYERS_bassplayer.wav')
  T.add(T2)
  T.write('PLAYERS_both.wav')
  
  return

if __name__=='__main__':
  main()


