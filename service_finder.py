#!/usr/bin/env python3

import nmap3

ip = input('Enter Target IP Address: ')
nmap = nmap3.Nmap()
results = nmap.nmap_version_detection(ip)

for i in results[ip]['ports']:
    try:
        print(i['service']['product'] + ' / ' + i['service']['version'])
    except:
        pass