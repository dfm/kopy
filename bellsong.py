import sys
import random
import numpy as np
import pylab as pb
import scipy.io.wavfile

Fs=44100

def make16bit(data):
  data=data/100 # corrects for our funny volume convention
  bits=16
  RANGE=2**(bits-1)
  data=data*RANGE
  data=np.array(data,dtype='int16')
  pb.plot(data)
  return data

def bell(V=30,freq=880,attack=0.001,decay=1.,cut=None,damp=0.1):
  T=decay*4
  t=np.linspace(0,T,T*Fs)
  if cut==None:
    data=V*(1-np.exp(-t/attack))*np.sin(2*np.pi*freq*t)*np.exp(-t/decay)
  else:
    C=1/(1+np.exp((t-cut)/damp))
    data=C*V*(1-np.exp(-t/attack))*np.sin(2*np.pi*freq*t)*np.exp(-t/decay)
  return data

def rnmel(key,RANGE='ALTO',Lmel=800):
  '''
  eventually this should accept any key, with names like 'C', 'C#','Bb',... etc.
  '''
  freqs=[]
  if key=='chrom':
    freqs=[220*2**(float(x)/12) for x in range(25)]
  if key=='A':
    freqs=[220*2**(float(x)/12) for x in [0,2,4,5,7,9,11,12,14,16,17,19,21,23,24]]
  else:
    print "we ain't ready for that!"
    sys.exit(0)
  mel=[]
  for count in range(Lmel):
    mel.append(freqs[random.randint(0,len(freqs)-1)])
  return mel
  
def main():
  data=bell(cut=1)#goes from -100 to 100
  #pb.plot(data)
  #pb.show()
  
  #make some music
  bpm=132
  mel=rnmel('A')
  #quarternotes
  song=np.zeros(Fs*(len(mel)+20)*60/bpm)
  
  k=0
  for notefreq in mel:
    start=int(k*Fs*60/bpm)
    VOL=30
    if notefreq>440: VOL=20
    note=bell(freq=notefreq,cut=1,V=VOL)
    end=start+len(note)
    song[start:end]+=note
    k+=1
  
  #add some quick runs - sixteenth notes
  runs=[]
  end=0
  while sum(len(run) for run in runs)<len(song):
    runmel=rnmel('A',Lmel=random.randint(4,32))
    run=np.zeros(Fs*(len(runmel))*0.25*60/bpm+Fs*4)
    k=0
    for notefreq in runmel:
      start=int(k*Fs*0.25*60/bpm)
      note=bell(freq=notefreq,V=25,cut=0.02,damp=0.01)
      print note
      end=start+len(note)
      run[start:end]+=note
      k+=1
    runs.append(run)
  end=0
  for run in runs:
    start=end+int(random.randint(1/2*4,16*4)*0.25*Fs/bpm)
    end=start+len(run)
    if end<len(song):
      song[start:end]+=run
  
  #add some low sustained notes
  bassmel=rnmel('A',Lmel=300)
  bassmel=[freq/2 for freq in bassmel]
  end=0
  for bassfreq in bassmel:
    start=end+int(random.randint(4,16)*Fs/bpm)
    note=bell(freq=bassfreq,V=60,cut=4.0,damp=8.)
    end=start+len(note)
    if end<len(song):
      song[start:end]+=note
  
  D=(Fs,make16bit(song))
  
  fn='demo.wav'
  scipy.io.wavfile.write(fn,*D)

if __name__=='__main__':
  main()


