import pywintypes
import struct
import win32com.directsound.directsound as ds
import tkinter
from tkinter import filedialog
#4char int 4char 4char int short short int int short short 4char int
WAV_HEADER_SIZE = struct.calcsize('<4sl4s4slhhllhh4sl')
BUFFERSIZE = 204800

class Window:
    def __init__(self):
        self.root = root = tkinter.Tk()
        buttonAdd = tkinter.Button(root, text = 'Add', command = self.add)
        buttonAdd.pack(side = 'left')
        buttonPlay = tkinter.Button(root, text = 'Play', command = self.play)
        buttonPlay.pack(side = 'left')           
        buttonStop = tkinter.Button(root, text = 'Stop', command = self.stop)
        buttonStop.pack(side = 'left')
        buttonPause = tkinter.Button(root, text = "Pause", command = self.pause)
        buttonPause.pack(side = 'left')
        self.currentpos = 0

    def add(self):
        self.file = filedialog.askopenfilename(title = 'Python DirectSound',filetypes =[('WAV','*.wav')])
        f = open(self.file, 'rb')
        hdr = f.read(WAV_HEADER_SIZE)
        wfx, size = self.wav_header_unpack(hdr)
        d = ds.DirectSoundCreate(None, None)
        d.SetCooperativeLevel(None, ds.DSSCL_PRIORITY)
        sdesc = ds.DSBUFFERDESC()
        sdesc.dwFlags = (
            ds.DSBCAPS_STICKYFOCUS |
            ds.DSBCAPS_CTRLPOSITIONNOTIFY
        )
        sdesc.dwBufferBytes = size
        sdesc.lpwfxFormat = wfx
        self.buffer = buffer = d.CreateSoundBuffer(sdesc,None)
        buffer.Update(0, f.read(size))

    def wav_header_unpack(self, data):
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

    def play(self):
        self.buffer.SetCurrentPosition(self.currentpos)
        self.buffer.Play(0)

    def pause(self):
        play, write = self.buffer.GetCurrentPosition()
        self.currentpos = play
        print(self.currentpos)
        self.buffer.Stop()

    def conti(self):
    	self.buffer.SetCurrentPosition(self.currentpos)
    	self.buffer.Play(0)

    def stop(self):
        self.currentpos = 0
        self.buffer.Stop()

    def MainLoop(self):
        self.root.mainloop()

window = Window()
window.MainLoop()