#!/usr/bin/env python3
import vulners
import json
import re
import nmap3

vulners_api = vulners.Vulners(api_key="DAUGMZHCAXHBC73D5MDIWRGXHLAP9P03QSWBJWXL2MGJ2W0B7GRKI5U8N334XWBQ")

#print(json.dumps(results, indent=4))

#regular expression patter to find correctly formatted IP address
ip_pattern = '([0-9]{1,3}\.){3}[0-9]{1,3}'
#loop to ensure an IP address was added properly
while True:
    ip = input('Enter Target IP Address: ')
    if not re.match(ip_pattern, ip):
        print('Error: Not a valid IP address.')
    else:
        break

#NMAP service scan
nmap = nmap3.Nmap()
results = nmap.nmap_version_detection(ip)

services = []
data = {}
'''
This while loop ensures the IP address given is valid: 
if no data is able to be collected, user is prompted to re enter IP
'''
while True:
    try:
        #data = all results generated from the scan
        data = results[ip]['ports']
        break
    except:
        print('Error: Not a valid IP address')
        while True:
            ip = input('Enter Target IP Address: ')
            if not re.match(ip_pattern, ip):
                print('Error: Not a valid IP address.')
            else:
                break
        break

#iterate through all of the data collected on services running
for i in data:
    if i['state'] == 'closed':
        continue
    try:
        #only grab version number, not excess information
        if ' ' in i['service']['version']:
            vNum = i['service']['version'].find(' ')
        '''
        Samba versions are not detected by NMAP and will 
        therefore not yeild worthwile data
        '''
        if i['service']['product'] != 'Samba smbd':
            services.append([i['service']['product'], i['service']['version'][:vNum]])
            # print(i['service']['product'] + ' / ' + i['service']['version'])
        elif i['service']['product'] == 'Samba smbd':
            #still document existence of Samba server
            pass
    except:
        pass

print('\n')
if services != []:
    print(services)
else:
    print('No open services detected.')
#_____________________________________________________________________________________

#Create a variable to input multiple vunerabilities into a list
#library = [["Apache httpd", "2.4.7"], ["OpenSSH", "6.6"]]
#Loop through vulnerability list to output CVE
for vulnerability in services:
    results = vulners_api.softwareVulnerabilities(vulnerability[0], vulnerability[1])
    exploit_list = results.get('exploit')
    vulnerabilities_list = [results.get(key) for key in results if key not in ['info', 'blog', 'bugbounty']]
    for item in vulnerabilities_list:
        for specific in item:
            print(specific["cvelist"], "Score =", specific["cvss"]["score"], "\n", specific["title"], "\n" )



       

