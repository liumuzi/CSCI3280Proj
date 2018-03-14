import pywintypes
import struct
import win32com.directsound.directsound as ds
from tkinter import *
import itertools as it

#4char int 4char 4char int short short int int short short 4char int
WAV_HEADER_SIZE = struct.calcsize('<4sl4s4slhhllhh4sl')
BUFFERSIZE = 204800

class Window(object):
	def __init__(self):
		self.root = root = Tk()
		root.title('Music Player')
		root.minsize(width=500,height=400)
		root.maxsize(width=500,height=400)
		root.resizable(width=False, height=False)
		
		self.albumFrame = Frame(root,width=500,height=145, bd = 3,bg='lightblue')
		self.toolBar = Frame(root,width=500,height=115, bd = 2,bg='white')
		self.musicList = Frame(root,width=500,height=100, bd = 2)
		
		self.volumeIcon = PhotoImage(file='./src/volume.png').subsample(2,2)
		self.volumeUpIcon = PhotoImage(file='src/volume_up.png').subsample(3,3)
		self.volumeDownIcon = PhotoImage(file='src/volume_down.png').subsample(3,3)
		self.playLastIcon = PhotoImage(file='src/last_song.png').subsample(2,2)
		self.playNextIcon = PhotoImage(file='src/next_song.png').subsample(2,2)
		self.playIcon = PhotoImage(file='src/play.png').subsample(1,1)
		self.pauseIcon = PhotoImage(file='src/pause.png').subsample(1,1)
		self.stopIcon = PhotoImage(file='src/stop.png').subsample(1,1)
		self.lyricIcon = PhotoImage(file='src/lyric.png').subsample(2,2)
		
		
		volumeButton = Button(toolBar, image=self.volumeIcon, width = 35, height = 35,relief="solid",bd=0,bg='white')
		volumeButton.bind('<Button-1>', self.setVol)
		volumeButton.place(x=15,y=23)
		
		volumeDownButton = Button(toolBar, image=self.volumeDownIcon, width = 35, height = 35,relief="solid",bd=0,bg='white')
		volumeDownButton.bind('<Button-1>', self.setVol)
		volumeDownButton.place(x=59,y=41)
		
		volumeUpButton = Button(toolBar, image=self.volumeUpIcon, width = 35, height = 35,relief="solid",bd=0,bg='white')
		volumeUpButton.bind('<Button-1>', self.setVol)
		volumeUpButton.place(x=59,y=6)
		
		playLastButton = Button(toolBar, image=self.playLastIcon, width = 35, height = 35,relief="solid",bd=0,bg='white')
		playLastButton.bind('<Button-1>', self.playAudio)
		playLastButton.place(x=115,y=25)
		
		pauseButton = Button(toolBar, image=self.pauseIcon, width = 50, height = 50,relief="solid",bd=0,bg='white')
		pauseButton.bind('<Button-1>', self.playAudio)
		pauseButton.place(x=165,y=16)
		
		playButton = Button(toolBar, image=self.playIcon, width = 50, height = 50,relief="solid",bd=0,bg='white')
		playButton.bind('<Button-1>', self.playAudio)
		playButton.place(x=235,y=16)
		
		stopButton = Button(toolBar, image=self.stopIcon,width = 50, height = 50,relief="solid",bd=0,bg='white')
		stopButton.bind('<Button-1>', self.playAudio)
		stopButton.place(x=305,y=16)
		
		playNextButton = Button(toolBar, image=self.playNextIcon, width = 35, height = 35,relief="solid",bd=0,bg='white')
		playNextButton.bind('<Button-1>', self.playAudio)
		playNextButton.place(x=383,y=25)
		
		lyricButton = Button(toolBar, image=self.lyricIcon,width = 35, height = 35,relief="solid",bd=0,bg='white')
		lyricButton.bind('<Button-1>', self.playAudio)
		lyricButton.place(x=447,y=24)
		
		
		v = StringVar()
		prog = Scale(
		    toolBar,
		    orient = 'horizontal',
		    from_ = 0, to = 100,
		    showvalue = False,
		    command = self.setProg,
		    length = 490,
		    bg = 'lightblue',
		    variable = v
		)
		prog.place(x=1,y=80)
		musiclist=['music 1','music 2','music 3','music 4']
		musicBox = Listbox(musicList, width = 80, height = 8, activestyle = 'dotbox')
		for item in musiclist:
		    musicBox.insert(END,item)
		musicBox.bind('<Double-Button-1>',self.getMusic)
		musicBox.grid()
		
		toolBar.grid_propagate(False)
		
		albumFrame.grid()
		toolBar.grid(rowspan = 2)
		musicList.grid()		


	def setVol(self, vol):
	    print("setVolume")
	
	def setProg(self, event):
	    print(v.get())
	
	def playAudio(self, event):
	    print("Playing audio")

	def getMusic(self, event):
	    l = musicBox.curselection()
	    print(musicBox.get(l))

	def MainLoop(self):
		self.root.mainloop()

window = Window()
window.MainLoop()