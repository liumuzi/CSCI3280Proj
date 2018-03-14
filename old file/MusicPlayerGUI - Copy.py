from tkinter import *
import itertools as it

def setVol(vol):
    print("setVolume")

def setProg(event):
    print(v.get())

def playAudio(event):
    print("Playing audio")

def getMusic(event):
    l = musicBox.curselection()
    print(musicBox.get(l))


root = Tk()
root.title('Music Player')
root.minsize(width=500,height=400)
root.maxsize(width=500,height=400)
root.resizable(width=False, height=False)

albumFrame = Frame(root,width=500,height=145, bd = 3,bg='lightblue')
toolBar = Frame(root,width=500,height=115, bd = 2,bg='white')
musicList = Frame(root,width=500,height=100, bd = 2)



volumeIcon = PhotoImage(file='volume.png').subsample(2,2)
volumeUpIcon = PhotoImage(file='volume_up.png').subsample(3,3)
volumeDownIcon = PhotoImage(file='volume_down.png').subsample(3,3)
playLastIcon = PhotoImage(file='play_last.png').subsample(2,2)
playNextIcon = PhotoImage(file='play_next.png').subsample(2,2)
playIcon = PhotoImage(file='play.png').subsample(1,1)
pauseIcon = PhotoImage(file='pause.png').subsample(1,1)
stopIcon = PhotoImage(file='stop.png').subsample(1,1)
lyricIcon = PhotoImage(file='lyric.png').subsample(2,2)


volumeButton = Button(toolBar, image = volumeIcon, width = 35, height = 35,relief="solid",bd=0,bg='white')
volumeButton.bind('<Button-1>', setVol)
volumeButton.place(x=15,y=23)

volumeDownButton = Button(toolBar, image = volumeDownIcon, width = 35, height = 35,relief="solid",bd=0,bg='white')
volumeDownButton.bind('<Button-1>', setVol)
volumeDownButton.place(x=59,y=41)

volumeUpButton = Button(toolBar, image = volumeUpIcon, width = 35, height = 35,relief="solid",bd=0,bg='white')
volumeUpButton.bind('<Button-1>', setVol)
volumeUpButton.place(x=59,y=6)

playLastButton = Button(toolBar, image = playLastIcon, width = 35, height = 35,relief="solid",bd=0,bg='white')
playLastButton.bind('<Button-1>', playAudio)
playLastButton.place(x=115,y=25)

pauseButton = Button(toolBar, image = pauseIcon, width = 50, height = 50,relief="solid",bd=0,bg='white')
pauseButton.bind('<Button-1>', playAudio)
pauseButton.place(x=165,y=16)

playButton = Button(toolBar, image = playIcon, width = 50, height = 50,relief="solid",bd=0,bg='white')
playButton.bind('<Button-1>', playAudio)
playButton.place(x=235,y=16)

stopButton = Button(toolBar, image = stopIcon,width = 50, height = 50,relief="solid",bd=0,bg='white')
stopButton.bind('<Button-1>', playAudio)
stopButton.place(x=305,y=16)

playNextButton = Button(toolBar, image = playNextIcon, width = 35, height = 35,relief="solid",bd=0,bg='white')
playNextButton.bind('<Button-1>', playAudio)
playNextButton.place(x=383,y=25)

lyricButton = Button(toolBar, image = lyricIcon,width = 35, height = 35,relief="solid",bd=0,bg='white')
lyricButton.bind('<Button-1>', playAudio)
lyricButton.place(x=447,y=24)


v = StringVar()
prog = Scale(
    toolBar,
    orient = 'horizontal',
    from_ = 0, to = 100,
    showvalue = False,
    command = setProg,
    length = 490,
    bg = 'lightblue',
    variable = v
)
prog.place(x=1,y=80)
musiclist=['music 1','music 2','music 3','music 4']
musicBox = Listbox(musicList, width = 80, height = 8, activestyle = 'dotbox')
for item in musiclist:
    musicBox.insert(END,item)
musicBox.bind('<Double-Button-1>',getMusic)
musicBox.grid()

toolBar.grid_propagate(False)

albumFrame.grid()
toolBar.grid(rowspan = 2)
musicList.grid()

root.mainloop()
