from tkinter import *


def setVol(vol):
    pass

def setProg(prog):
    pass

def playAudio(event):
    print("Playing audio")


root = Tk()
root.minsize(width=500,height=400)
root.maxsize(width=500,height=400)
root.resizable(width=False, height=False)

albumFrame = Frame(root,width=500,height=200, bd = 2, bg = 'black')
toolBar = Frame(root,width=500,height=64, bd = 2)
musicList = Frame(root,width=500,height=50, bd = 2)

vol = Scale(
    toolBar,
    orient = 'horizontal',
    from_ = 0, to = 100,
    showvalue = False,
    command = setVol,
    length = 150
)
vol.grid(row=0,column=1)

volumeIcon = PhotoImage(file='volume.png').subsample(4,4)
playIcon = PhotoImage(file='play.png').subsample(4,4)
pauseIcon = PhotoImage(file='play.png').subsample(4,4)
stopIcon = PhotoImage(file='play.png').subsample(4,4)
lyricIcon = PhotoImage(file='play.png').subsample(4,4)

volLabel = Label(toolBar, image = volumeIcon, width = 20, height = 20)
volLabel.grid(row=0,column=0)

playButton = Label(toolBar, image = playIcon, width = 35, height = 35)
playButton.bind('<Button-1>', playAudio)
playButton.grid(row=0,column=2)

pauseButton = Label(toolBar, image = pauseIcon, width = 35, height = 35)
pauseButton.bind('<Button-1>', playAudio)
pauseButton.grid(row=0,column=3)

stopButton = Label(toolBar, image = stopIcon,width = 35, height = 35)
stopButton.bind('<Button-1>', playAudio)
stopButton.grid(row=0,column=4)

lyricButton = Label(toolBar, image = lyricIcon,width = 35, height = 35)
lyricButton.bind('<Button-1>', playAudio)
lyricButton.grid(row=0,column=5)


prog = Scale(
    toolBar,
    orient = 'horizontal',
    from_ = 0, to = 100,
    showvalue = False,
    command = setProg,
    length = 500
)
prog.grid(row=1,column=0, columnspan = 6)

def callback(name, win):
    print('Change music %d to %s'%(musicBox.curselection()[0], name))
    win.destroy()

def changeName(event):
    changeNameWin = Tk()
    l = Label(changeNameWin, text = 'New name:')
    e = Entry(changeNameWin)
    b = Button(changeNameWin, text = 'Confirm', command = lambda : callback(e.get(), changeNameWin))

    l.grid(row=0, column=0)
    e.grid(row=0, column=1)
    b.grid(row = 1, column = 1)

    changeNameWin.mainloop()


musicBox = Listbox(musicList, width = 80, height = 8, activestyle = 'dotbox')
musicBox.bind('<Button-3>', changeName)
for i in range(1,16):
    musicBox.insert(END, 'Music %d'%i)
musicBox.grid()

toolBar.grid_propagate(False)

albumFrame.grid()
toolBar.grid(rowspan = 2)
musicList.grid()

root.mainloop()