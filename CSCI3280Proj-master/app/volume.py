import ctypes
import struct
 
 
waveOutGetVolume = (
  ctypes.windll.winmm.waveOutGetVolume)
 
waveOutSetVolume = (
  ctypes.windll.winmm.waveOutSetVolume)
 
MINIMUM_VOLUME = 0     # fader control (MSDN Library)
MAXIMUM_VOLUME = 4294967295 # fader control (MSDN Library)

def SetVolume(volume):

    ret = waveOutSetVolume(0, 0xffff)
 
    return
if __name__ == '__main__':
    #最大音量
    SetVolume(100)
