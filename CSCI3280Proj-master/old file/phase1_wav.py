import pywintypes
import struct
import win32event
import win32com.directsound.directsound as ds
import os
import sys

#4char int 4char 4char int short short int int short short 4char int

WAV_HEADER_SIZE = struct.calcsize('<4si4s4sihhiihh4si')

def wav_header_unpack(data):
  print("Start reading wave file.")
  #unpack wav header information
  (riff, riffsize, wave, fmt, fmtsize, format, nchannels, samplespersecond, \
  datarate, blockalign, bitspersample, data, datalength) = struct.unpack('<4si4s4sihhiihh4si', data)
  if riff != b'RIFF' or fmtsize != 16 or fmt != b'fmt ' or data != b'data':
    print("Error! Please check your file!")
    exit(1)
  print("File size: " + str(riffsize))
  wfx = pywintypes.WAVEFORMATEX()
  wfx.wFormatTag = format
  print("Audio format code: " + str(format))
  wfx.nChannels = nchannels
  print("Number of channels: " + str(nchannels))
  wfx.nSamplesPerSec = samplespersecond
  print("Sample rate: " + str(samplespersecond))
  wfx.nAvgBytesPerSec = datarate
  print("Byte rate: " + str(datarate))
  wfx.nBlockAlign = blockalign
  print("Block align: " + str(blockalign))
  wfx.wBitsPerSample = bitspersample
  print("Bits per sample: " + str(bitspersample))
  return wfx, datalength

sound_file = sys.argv[1]
fname = os.path.join(os.path.dirname(__file__), sound_file)
print("You want to play file: " + fname)
f = open(fname, 'rb')

#read wav header and unpack
hdr = f.read(WAV_HEADER_SIZE)
wfx, size = wav_header_unpack(hdr)


d = ds.DirectSoundCreate(None, None)
d.SetCooperativeLevel(None, ds.DSSCL_PRIORITY)

sdesc = ds.DSBUFFERDESC()
sdesc.dwFlags = ds.DSBCAPS_STICKYFOCUS | ds.DSBCAPS_CTRLPOSITIONNOTIFY
sdesc.dwBufferBytes = size
sdesc.lpwfxFormat = wfx

buffer = d.CreateSoundBuffer(sdesc, None)
event = win32event.CreateEvent(None, 0, 0, None)
notify = buffer.QueryInterface(ds.IID_IDirectSoundNotify)
notify.SetNotificationPositions((ds.DSBPN_OFFSETSTOP, event))
buffer.Update(0, f.read(size))
buffer.Play(0)

win32event.WaitForSingleObject(event, -1)
