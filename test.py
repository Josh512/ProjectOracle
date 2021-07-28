#!/usr/bin/env python3

import vulners
#import json
import re
import nmap3

def ip_add():
    #regular expression patter to find correctly formatted IP address
    ip_pattern = '([0-9]{1,3}\.){3}[0-9]{1,3}'
    #ensure an IP address was added properly
    ip = input('Enter Target IP Address: ')
    if not re.match(ip_pattern, ip):
        print('Error: Not a valid IP address.')
        ip_add()
    else:
        nmap_scan(ip)

def nmap_scan(ip):
    #NMAP service scan
    nmap = nmap3.Nmap()
    results = nmap.nmap_version_detection(ip, args='--host-timeout 15')
    data = {}
    try:
        #data = all results generated from the scan
        data = results[ip]['ports']
    except:
        print('Error: Not a valid IP address')
        ip_add()
    services = []
    #iterate through all of the data collected on services running
    for i in data:
        if i['state'] == 'closed':
            continue

        #only grab version number, not excess information
        if 'version' not in i['service']:
            continue
        if ' ' in i['service']['version']:
            vNum = i['service']['version'].find(' ')
        else:
            vNum = len(i['service']['version'])
        '''
        Samba versions are not detected by NMAP and will 
        therefore not yeild worthwile data
        '''
        if 'product' not in i['service']:
            continue
        if i['service']['product'] != 'Samba smbd':
            services.append([i['service']['product'], i['service']['version'][:vNum]])
            #print(i['service']['product'] + ' / ' + i['service']['version'])
        elif i['service']['product'] == 'Samba smbd':
            #still document existence of Samba server
            pass
    print('\n')
    if services != []:
        print(services)
    else:
        print('No open services detected.')
    vulners_lib(services)
#_____________________________________________________________________________________

#Create a variable to input multiple vunerabilities into a list
#library = [["Apache httpd", "2.4.7"], ["OpenSSH", "6.6"]]
#Loop through vulnerability list to output CVE
def vulners_lib(services):
    vulners_api = vulners.Vulners(api_key="DAUGMZHCAXHBC73D5MDIWRGXHLAP9P03QSWBJWXL2MGJ2W0B7GRKI5U8N334XWBQ")
    CVE_List = {}
    for vulnerability in services:
        results = vulners_api.softwareVulnerabilities(vulnerability[0], vulnerability[1])
        exploit_list = results.get('exploit')
        vulnerabilities_list = [results.get(key) for key in results if key not in ['info', 'blog', 'bugbounty']]
        for item in vulnerabilities_list:
            for specific in item:
                i = tuple(specific["cvelist"])
                score = specific["cvss"]["score"]
                title = specific["title"]
                if score == 0.0:
                    continue
                else:
                    #key = CVE number
                    #value = [score, description]
                    CVE_List[i] = [score, title]
                    #print(specific["cvelist"], "Score =", specific["cvss"]["score"], "\n", specific["title"], "\n" )
    testing(CVE_List)

def testing(CVE_List):
    for k in CVE_List:
        try:
            print("{} Score = {} \n {} \n".format(k, CVE_List[k][0], CVE_List[k][1]))
        except:
            continue

def main():
    ip_add()

if __name__ == '__main__':
    main()