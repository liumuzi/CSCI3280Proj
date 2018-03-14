import pywintypes
import struct
import win32com.directsound.directsound as ds
from tkinter import *
import itertools as it

#4char int 4char 4char int short short int int short short 4char int
WAV_HEADER_SIZE = struct.calcsize('<4sl4s4slhhllhh4sl')
BUFFERSIZE = 204800

class Window:
    def __init__(self):
        self.root = Tk()

        self.root.title('Music Player')
        self.root.minsize(width=500,height=400)
        self.root.maxsize(width=500,height=400)
        self.root.resizable(width=False, height=False)

        albumFrame = Frame(self.root,width=500,height=145, bd = 3,bg='lightblue')
        toolBar = Frame(self.root,width=500,height=115, bd = 2,bg='white')
        musicList = Frame(self.root,width=500,height=100, bd = 2)
        volumeIcon = PhotoImage(file='volume.png').subsample(2,2)
        volumeUpIcon = PhotoImage(file='volume_up.png').subsample(3,3)
        volumeDownIcon = PhotoImage(file='volume_down.png').subsample(3,3)
        playLastIcon = PhotoImage(file='last_song.png').subsample(2,2)
        playNextIcon = PhotoImage(file='next_song.png').subsample(2,2)
        playIcon = PhotoImage(file='play.png').subsample(1,1)
        pauseIcon = PhotoImage(file='pause.png').subsample(1,1)
        stopIcon = PhotoImage(file='stop.png').subsample(1,1)
        lyricIcon = PhotoImage(file='lyric.png').subsample(2,2)

        
        buttonAdd = Button(self.root, text = 'Add', command = self.add)
        buttonAdd.pack(side = 'left')
        buttonPlay = Button(self.root, text = 'Play', command = self.play)
        buttonPlay.pack(side = 'left')           
        buttonStop = Button(self.root, text = 'Stop', command = self.stop)
        buttonStop.pack(side = 'left')
        buttonPause = Button(self.root, text = "Pause", command = self.pause)
        buttonPause.pack(side = 'left')
        

        volumeButton = Button(toolBar, image = volumeIcon, width = 35, height = 35,relief="solid",bd=0,bg='white')
        volumeButton.bind('<Button-1>', self.setVol)
        volumeButton.place(x=15,y=23)
        
        volumeDownButton = Button(toolBar, image = volumeDownIcon, width = 35, height = 35,relief="solid",bd=0,bg='white')
        volumeDownButton.bind('<Button-1>', self.setVolDown)
        volumeDownButton.place(x=59,y=41)
        
        volumeUpButton = Button(toolBar, image = volumeUpIcon, width = 35, height = 35,relief="solid",bd=0,bg='white')
        volumeUpButton.bind('<Button-1>', self.setVolUp)
        volumeUpButton.place(x=59,y=6)
        
        playLastButton = Button(toolBar, image = playLastIcon, width = 35, height = 35,relief="solid",bd=0,bg='white')
        playLastButton.bind('<Button-1>', self.playAudio)
        playLastButton.place(x=115,y=25)
        
        pauseButton = Button(toolBar, image = pauseIcon, width = 50, height = 50,relief="solid",bd=0,bg='white')
        pauseButton.bind('<Button-1>', self.playAudio)
        pauseButton.place(x=165,y=16)
        
        playButton = Button(toolBar, image = playIcon, width = 50, height = 50,relief="solid",bd=0,bg='white')
        playButton.bind('<Button-1>', self.playAudio)
        playButton.place(x=235,y=16)
        
        stopButton = Button(toolBar, image = stopIcon,width = 50, height = 50,relief="solid",bd=0,bg='white')
        stopButton.bind('<Button-1>', self.playAudio)
        stopButton.place(x=305,y=16)
        
        playNextButton = Button(toolBar, image = playNextIcon, width = 35, height = 35,relief="solid",bd=0,bg='white')
        playNextButton.bind('<Button-1>', self.playAudio)
        playNextButton.place(x=383,y=25)
        
        lyricButton = Button(toolBar, image = lyricIcon,width = 35, height = 35,relief="solid",bd=0,bg='white')
        lyricButton.bind('<Button-1>', self.playAudio)
        lyricButton.place(x=447,y=24)

        self.currentpos = 0

    def setVol(self, vol):
        print("setVolume")
    
    def setVolDown(self):
        print("setVolDown")

    def setVolUp(self):
        print("setVolUp")
    
    def setProg(self, event):
        print(v.get())
    
    def playAudio(self, event):
        print("Playing audio")
    
    def getMusic(self, event):
        l = musicBox.curselection()
        print(musicBox.get(l))

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