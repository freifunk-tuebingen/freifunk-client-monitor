#!/usr/bin/env python
from subprocess import call
from subprocess import check_output
import re
from datetime import date
from datetime import datetime

import time
from time import sleep

# Networkmanager muss aus

SSID = "Freifunk"


def writeCSVLine(logstring):
    text_file = open(SSID + ".log", "a")
    text_file.write(logstring + '\n')    
    text_file.close()
    pass


if __name__ == '__main__':
        # TODO wait
    logstring = str(datetime.now()) + ';'
    logstring += SSID + ';'
    
    print "flusching...."
    
    call(["ip","addr","flush","dev","wlan0"])
    call(["ip","-6","addr","flush","dev","wlan0"])

    print "block wlan..."

    call(["rfkill", "block", "wlan"])
    
    sleep(5)
    
    print "unblock wlan..."

    call(["rfkill", "unblock", "wlan"])

    sleep(5)
    
    print "ifconfig wlan0 up..."

    call(["ifconfig", "wlan0", "up"])
    
    sleep(5)
    
    scanres = check_output(['iwlist', 'wlan0', 'scan'])
    m = re.search(SSID, scanres)
    #print scanres
    if m:
        logstring += SSID + ' ist sichtbar;'
        print 'SSID ' + SSID + ' ist sichtbar;'
    else:
        logstring = logstring + 'SSID ist nicht sichtbar;';
        writeCSVLine(logstring)
        exit
        
    
    print 'Verbinde mit ' + SSID + '.. '
    #connectwlan_output = check_output(['iwconfig', 'wlan0','essid', SSID])

    #networkID = check_output(["wpa_cli", "add_network"])
    #call(["wpa_cli", "set_network", networkID, "ssid", "\'\"" + SSID + "\"\'"])
    #call(["wpa_cli", "set_network", networkID, "scan_ssid", "1"])
    #call(["wpa_cli", "enable_network", networkID])
    
    starttime = time.time()
    connectwlan_output = check_output(['dhclient', 'wlan0'])
    dhcpduration = time.time()-starttime
    logstring += str(dhcpduration)+';'

    print "sleep 20s nach dhclient weil IPv6 laenger dauern kann..."    
    sleep(20)
    
    
    ifconfig_output = check_output(['ifconfig', 'wlan0'])
    m = re.search('.*wlan.*inet (?:Adresse|inet addr):(.*?) .*$',ifconfig_output,flags=re.MULTILINE+re.DOTALL)
    if m:
        print 'IPv4 = '+m.group(1)
        logstring += m.group(1) + ';'
    else:
        logstring += ';'
    m = re.search('.*wlan.*?(?:inet6-Adresse|inet6 addr): (fd21:b4dc:4b.*?)/.*$',ifconfig_output,flags=re.MULTILINE+re.DOTALL)
    if m:
        print 'IPv6 = '+m.group(1)
        logstring += m.group(1) + ';'
    else:
        logstring += ';'
        
    print logstring
    writeCSVLine(logstring)
    
