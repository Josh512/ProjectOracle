#!/usr/bin/env python3

import vulners
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
        if 'product' not in i['service']:
            continue
        if i['service']['product'] != 'Samba smbd':
            services.append([i['service']['product'], i['service']['version'][:vNum]])
            #print(i['service']['product'] + ' / ' + i['service']['version'])
        elif i['service']['product'] == 'Samba smbd':
            pass
    print('\n')
    if services != []:
        print(services)
    else:
        print('No open services detected.')
    vulners_lib(services)
#_____________________________________________________________________________________

#Create a variable to input multiple vunerabilities into a list
#Loop through vulnerability list to output CVE
def vulners_lib(services):
    vulners_api = vulners.Vulners(api_key="DAUGMZHCAXHBC73D5MDIWRGXHLAP9P03QSWBJWXL2MGJ2W0B7GRKI5U8N334XWBQ")
    global CVE_List
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
                    
    result()

def result():
    #sort through list to organize output by CVE score highest to lowest
    CVE_ListSorted = dict(sorted(CVE_List.items(), key=lambda item: item[1], reverse = True))
    Score = input("Enter minimum CVE score (1-10) or 'all': ")
    numCheck = "([0-9]{1}|[0-9]{1}\.[0-9]{1})"
    #Print CVE by score
    if str.lower(Score) == "all" or Score.strip() == '':
        for k in CVE_ListSorted:
            try:
                print("{} Score = {} \n {} \n".format(k, CVE_ListSorted[k][0], CVE_ListSorted[k][1]))
            except:
                continue
    elif re.match(numCheck, Score):
        for k in CVE_ListSorted:
            if float(CVE_ListSorted[k][0]) >= float(Score):
                try:
                    print("{} Score = {} \n {} \n".format(k, CVE_ListSorted[k][0], CVE_ListSorted[k][1]))
                except:
                    continue
            else:
                continue
    else:
        print('Invalid input.')
        result()
    # if "9" in Score:
    #     for k in CVE_ListSorted:
    #         if float(CVE_ListSorted[k][0]) >= float(9):
    #             try:
    #                 print("{} Score = {} \n {} \n".format(k, CVE_ListSorted[k][0], CVE_ListSorted[k][1]))
    #             except:
    #                 continue
    #         else:
    #             continue
    # if "8" in Score:
    #     for k in CVE_ListSorted:
    #         if float(CVE_ListSorted[k][0]) >= float(8):
    #             try:
    #                 print("{} Score = {} \n {} \n".format(k, CVE_ListSorted[k][0], CVE_ListSorted[k][1]))
    #             except:
    #                 continue
    #         else:
    #             continue
    # if "7" in Score:
    #     for k in CVE_ListSorted:
    #         if float(CVE_ListSorted[k][0]) >= float(7):
    #             try:
    #                 print("{} Score = {} \n {} \n".format(k, CVE_ListSorted[k][0], CVE_ListSorted[k][1]))
    #             except:
    #                 continue
    #         else:
    #             continue
    # if "6" in Score:
    #     for k in CVE_ListSorted:
    #         if float(CVE_ListSorted[k][0]) >= float(6):
    #             try:
    #                 print("{} Score = {} \n {} \n".format(k, CVE_ListSorted[k][0], CVE_ListSorted[k][1]))
    #             except:
    #                 continue
    #         else:
    #             continue
    # if "5" in Score:
    #     for k in CVE_ListSorted:
    #         if float(CVE_ListSorted[k][0]) >= float(5):
    #             try:
    #                 print("{} Score = {} \n {} \n".format(k, CVE_ListSorted[k][0], CVE_ListSorted[k][1]))
    #             except:
    #                 continue
    #         else:
    #             continue
    #for k in CVE_ListSorted:
        #try:
            #print("{} Score = {} \n {} \n".format(k, CVE_ListSorted[k][0], CVE_ListSorted[k][1]))
        #except:
            #continue

def main():
    ip_add()

if __name__ == '__main__':
    main()