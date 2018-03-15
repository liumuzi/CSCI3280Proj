import pywintypes
import struct
import win32com.directsound.directsound as ds
from tkinter import *
import itertools as it
import win32api  
import ctypes
import sqlite3
import os

#4char int 4char 4char int short short int int short short 4char int
WAV_HEADER_SIZE = struct.calcsize('<4sl4s4slhhllhh4sl')
BUFFERSIZE = 204800
MINVOLUME = 0
MAXVOLUME = 4294967295

db_conn = sqlite3.connect('app.db')
theCursor = db_conn.cursor()
print("Database Opened")

class MusicPlay(object):
	def __init__(self):
		self.frontbuffer = None
		self.backbuffer = None
		self.currentpos = 0
		self.lastclick = None
		self.volon = True
		self.volume = 15
		self.SetVolume(self.volume)
		self.showlyric = False

		self.filename = None
		self.total_info = None

	def SetVolume(self, volume):
		if volume == 15:
			ctypes.windll.winmm.waveOutSetVolume(0, 0xffffffff)
		elif volume == 14:
			ctypes.windll.winmm.waveOutSetVolume(0, 0xeeeeeeee)
		elif volume == 13:
			ctypes.windll.winmm.waveOutSetVolume(0, 0xdddddddd)
		elif volume == 12:
			ctypes.windll.winmm.waveOutSetVolume(0, 0xcccccccc)
		elif volume == 11:
			ctypes.windll.winmm.waveOutSetVolume(0, 0xbbbbbbbb)
		elif volume == 10:
			ctypes.windll.winmm.waveOutSetVolume(0, 0xaaaaaaaa)
		elif volume == 9:
			ctypes.windll.winmm.waveOutSetVolume(0, 0x99999999)
		elif volume == 8:
			ctypes.windll.winmm.waveOutSetVolume(0, 0x88888888)
		elif volume == 7:
			ctypes.windll.winmm.waveOutSetVolume(0, 0x77777777)
		elif volume == 6:
			ctypes.windll.winmm.waveOutSetVolume(0, 0x66666666)
		elif volume == 5:
			ctypes.windll.winmm.waveOutSetVolume(0, 0x55555555)
		elif volume == 4:
			ctypes.windll.winmm.waveOutSetVolume(0, 0x44444444)
		elif volume == 3:
			ctypes.windll.winmm.waveOutSetVolume(0, 0x33333333)
		elif volume == 2:
			ctypes.windll.winmm.waveOutSetVolume(0, 0x22222222)
		elif volume == 1:
			ctypes.windll.winmm.waveOutSetVolume(0, 0x11111111)
		elif volume == 0:
			ctypes.windll.winmm.waveOutSetVolume(0, 0x00000000)
		print("volume set with level  " + str(self.volume))

	def GetVolume(self):
		vol=ctypes.c_uint()
		res = ctypes.windll.winmm.waveOutGetVolume(0, ctypes.byref(vol))
		return  vol.value/(MAXVOLUME/100)

	def add(self, file):
		f = open(file, 'rb')
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
		self.backbuffersize = size
		self.backbuffer = buffer = d.CreateSoundBuffer(sdesc,None)
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

	def setVol(self):
		if self.volon == True:
			self.volume = 0
			self.SetVolume(self.volume)
			self.volon = False
		elif self.volon == False:
			self.volume = 15
			self.SetVolume(self.volume)
			self.volon = True			

	def setVolDown(self, vol):
		if self.volume >= 1:
			self.volume -= 1
		else:
			self.volume = 0
		self.SetVolume(self.volume)
	
	def setVolUp(self, vol):
		if self.volume <= 14:
			self.volume += 1
		else:
			self.volume = 15
		self.SetVolume(self.volume)
	
	def play(self, event):
		if self.lastclick == 'back':
			self.frontbuffersize = self.backbuffersize
			self.frontbuffer = self.backbuffer
		elif self.lastclick == 'front':
			self.frontbuffer.SetCurrentPosition(self.currentpos)
		self.lastclick = 'front'
		self.frontbuffer.Play(0)

	def pause(self, event):
		play, write = self.frontbuffer.GetCurrentPosition()
		self.currentpos = play
		print(self.currentpos)
		self.lastclick = 'front'
		self.frontbuffer.Stop()

	def stop(self, event):
		self.currentpos = 0
		self.lastclick = 'front'
		self.frontbuffer.Stop()

# playlast havn't implemented
	def playLast(self, event):
		print("play last");

# playnext havn't implemented
	def playNext(self, event):
		print("play next");

	def setProg(self, event):
	    self.frontbuffer.Stop()
	    perc = int(v.get())

	    if perc < 100:
	    	self.currentpos = int(perc / 100 * self.frontbuffersize)
	    else:
	    	self.currentpos = int(self.frontbuffersize)
	    self.frontbuffer.SetCurrentPosition(self.currentpos)
	    self.frontbuffer.Play(0)
	
	def showLyric(self):
		if self.showlyric == False:
			self.showlyric = True
		elif self.showlyric == True:
			self.showlyric = False
		print("show lyric")

	def getMusic(self, event):
	    l = musicBox.curselection()
	    self.filename = musicBox.get(l)
	    #Read info
	    theCursor.execute("SELECT name FROM song WHERE file_name = '%s'" %(self.filename))
	    info_name = self.shortInfo(str(theCursor.fetchall()))
	    theCursor.execute("SELECT singer FROM song WHERE file_name = '%s'" %(self.filename))
	    info_singer = self.shortInfo(str(theCursor.fetchall()))
	    theCursor.execute("SELECT album FROM song WHERE file_name = '%s'" %(self.filename))
	    info_album = self.shortInfo(str(theCursor.fetchall()))
	    self.total_info = info_name + ", " + info_singer + ", " + info_album
	    #infoBox.insert(END,self.total_info)
	    text_info.set(self.total_info)

	    self.filename = "wav/" + self.filename
	    print(self.filename)
	    self.lastclick = 'back'
	    self.add(self.filename)

	def shortInfo(self, info):
		song_info = info
		song_info = str(song_info).replace("[('", "")
		song_info = str(song_info).replace("',)]", "")
		return str(song_info)

	def doSearch(self):
		input = search_text.get()
		theCursor.execute("SELECT song_id FROM song WHERE file_name = '%s'" %(input))
		tmp = theCursor.fetchall()
		a = self.searchTest(tmp)
		if a!=0:
			self.searchResult(a)
			return

		theCursor.execute("SELECT song_id FROM song WHERE name = '%s'" %(input))
		tmp = theCursor.fetchall()
		a = self.searchTest(tmp)
		if a!=0:
			self.searchResult(a)
			return

		theCursor.execute("SELECT song_id FROM song WHERE singer = '%s'" %(input))
		tmp = theCursor.fetchall()
		a = self.searchTest(tmp)
		if a!=0:
			self.searchResult(a)
			return

		theCursor.execute("SELECT song_id FROM song WHERE album = '%s'" %(input))
		tmp = theCursor.fetchall()
		a = self.searchTest(tmp)
		self.searchResult(a)
		return


	def searchTest(self, temp):
		if str(temp) != "[]":
			tmpid = str(temp)
		else:
			tmpid = "[(0,)]"
		tmpid = tmpid.replace("[(", "")
		tmpid = tmpid.replace(",)]", "")
		return(int(tmpid))

	def searchResult(self, songid):
		if songid == 0:
			text_info.set("No Result")
			return
		theCursor.execute("SELECT name FROM song WHERE song_id = '%d'" %(songid))
		info_name = self.shortInfo(str(theCursor.fetchall()))
		theCursor.execute("SELECT singer FROM song WHERE song_id = '%d'" %(songid))
		info_singer = self.shortInfo(str(theCursor.fetchall()))
		theCursor.execute("SELECT album FROM song WHERE song_id = '%d'" %(songid))
		info_album = self.shortInfo(str(theCursor.fetchall()))
		self.total_info = info_name + ", " + info_singer + ", " + info_album
		text_info.set(self.total_info)





myplayer = MusicPlay()
root = Tk()
root.title('Music Player')
root.minsize(width=500,height=400)
root.maxsize(width=500,height=400)

albumFrame = Frame(root,width=500,height=145, bd = 3,bg='lightblue')
toolBar = Frame(root,width=500,height=115, bd = 2,bg='white')
searchList = Frame(root,width=500,height=20, bd = 2)
musicList = Frame(root,width=500,height=100, bd = 2)

def setVol():
	if myplayer.volon == True:
		volumeButton.config(image = muteIcon)
	elif myplayer.volon == False:
		volumeButton.config(image = volumeIcon)
	myplayer.setVol()

def setLyric():
	if myplayer.showlyric == False:
		lyricButton.config(image = lyricIcon)
	elif myplayer.showlyric == True:
		lyricButton.config(image=infoIcon)
	myplayer.showLyric()

volumeIcon = PhotoImage(file='volume.png').subsample(2,2)
muteIcon = PhotoImage(file = 'mute.png').subsample(2,2)
volumeUpIcon = PhotoImage(file='volume_up.png').subsample(3,3)
volumeDownIcon = PhotoImage(file='volume_down.png').subsample(3,3)
playLastIcon = PhotoImage(file='last_song.png').subsample(2,2)
playNextIcon = PhotoImage(file='next_song.png').subsample(2,2)
playIcon = PhotoImage(file='play.png').subsample(1,1)
pauseIcon = PhotoImage(file='pause.png').subsample(1,1)
stopIcon = PhotoImage(file='stop.png').subsample(1,1)
lyricIcon = PhotoImage(file='lyric.png').subsample(2,2)
infoIcon = PhotoImage(file='song_info.png').subsample(3,3)

volumeButton = Button(toolBar, image = volumeIcon, command = setVol, width = 35, height = 35,relief="solid",bd=0,bg='white')
volumeButton.place(x=15,y=23)

volumeDownButton = Button(toolBar, image = volumeDownIcon, width = 35, height = 35,relief="solid",bd=0,bg='white')
volumeDownButton.bind('<Button-1>', myplayer.setVolDown)
volumeDownButton.place(x=59,y=41)

volumeUpButton = Button(toolBar, image = volumeUpIcon, width = 35, height = 35,relief="solid",bd=0,bg='white')
volumeUpButton.bind('<Button-1>', myplayer.setVolUp)
volumeUpButton.place(x=59,y=6)

playLastButton = Button(toolBar, image = playLastIcon, width = 35, height = 35,relief="solid",bd=0,bg='white')
playLastButton.bind('<Button-1>', myplayer.playLast)
playLastButton.place(x=115,y=25)

pauseButton = Button(toolBar, image = pauseIcon, width = 50, height = 50,relief="solid",bd=0,bg='white')
pauseButton.bind('<Button-1>', myplayer.pause)
pauseButton.place(x=165,y=16)

playButton = Button(toolBar, image = playIcon, width = 50, height = 50,relief="solid",bd=0,bg='white')
playButton.bind('<Button-1>', myplayer.play)
playButton.place(x=235,y=16)

stopButton = Button(toolBar, image = stopIcon,width = 50, height = 50,relief="solid",bd=0,bg='white')
stopButton.bind('<Button-1>', myplayer.stop)
stopButton.place(x=305,y=16)

playNextButton = Button(toolBar, image = playNextIcon, width = 35, height = 35,relief="solid",bd=0,bg='white')
playNextButton.bind('<Button-1>', myplayer.playNext)
playNextButton.place(x=383,y=25)

lyricButton = Button(toolBar, image = lyricIcon,width = 35, command = setLyric, height = 35,relief="solid",bd=0,bg='white')
#lyricButton.bind('<Button-1>', setLyric)
lyricButton.place(x=447,y=24)


v = StringVar()
prog = Scale(
    toolBar,
    orient = 'horizontal',
    from_ = 0, to = 100,
    showvalue = False,
    command = myplayer.setProg,
    length = 490,
    bg = 'lightblue',
    variable = v
)
prog.place(x=1,y=80)

#Search Box
search_text = StringVar()
searchBox = Entry(searchList, textvariable = search_text, width = 70)
searchBox.place(x = 0, y  =0)

#Search Button
searchButton = Button(searchList, text = "Search", width = 8, height = 1, command = myplayer.doSearch)
searchButton.place(x = 425, y = 0)

#Song Information
text_info = StringVar()
text_info.set("")
infoLabel = Label(musicList, textvariable = text_info)
infoLabel.grid()



#Music List
music=['1.wav','2.wav','3.wav','4.wav','5.wav','6.wav','7.wav','8.wav','9.wav','10.wav','11.wav','12.wav','13.wav','14.wav','15.wav']

musicBox = Listbox(musicList, width = 80, height = 8, activestyle = 'dotbox', listvariable = music)
for item in music:
    musicBox.insert(END,item)
musicBox.bind('<ButtonRelease-1>',myplayer.getMusic)
musicBox.grid()


toolBar.grid_propagate(False)

albumFrame.place(x = 0, y = 0)
toolBar.place(x = 0, y = 145)
searchList.place(x = 0, y = 260)
musicList.place(x = 0, y = 280)

root.mainloop()
db_conn.close()
print("Database Closed")