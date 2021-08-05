#!/usr/bin/env python3

import vulners
import re
import nmap3
import socket
import webbrowser
import os
import requests
import sys
import warnings

def ip_add():
    '''Checks that you entered a correct IP address or converts a URL into an IP address to be used by NMAP'''
    #regular expression patter to find correctly formatted IP address
    ip_pattern = '([0-9]{1,3}\.){3}[0-9]{1,3}'
    url_pattern = '([a-zA-Z0-9]+)(\.[a-zA-Z]{2,5})'
    #ensure an IP address was added properly
    ip = input('Enter Target IP or URL Address: ')
    if re.match(url_pattern, ip):
        try:
            ip = socket.gethostbyname(ip)
            nmap_scan(ip)
        except:
            print('Error: Not a valid target.')
            ip_add()
    elif re.match(ip_pattern, ip):
        nmap_scan(ip)
    elif not re.match(ip_pattern, ip) or not re.match(url_pattern, ip):
        print('Error: Not a valid target.')
        ip_add()

def nmap_scan(ip):
    '''NMAP service scan that identifies all running services and versions.'''
    nmap = nmap3.Nmap()
    results = nmap.nmap_version_detection(ip, args='--host-timeout 20')
    data = {}
    try:
        #data = all results generated from the scan
        data = results[ip]['ports']
    except:
        print('Error: Not a valid IP address')
        ip_add()
    global services
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
        elif i['service']['product'] == 'Samba smbd':
            pass
    print('\n')
    if services != []:
        print(f'Services found: {services}')
        vulners_lib()
    else:
        print('No open services detected.')
        clean_exit()

def vulners_lib():
    '''Identifies what CVEs are associated with all running services, if any.'''
    warnings.simplefilter('ignore')
    if os.path.exists('./apiKey'):
        key = open('apiKey', 'r')
        key_contents = key.readline().strip()
        key.close()
        if key_contents != '':
            try:
                vulners_api = vulners.Vulners(api_key=key_contents)
            except:
                fixed_key = input('Incorrect API key used. Re enter key: ')
                f = open('apiKey', 'w')
                f.write(fixed_key)
                f.close()
                vulners_lib()
        elif key_contents == '' or key_contents == 'Enter your Vulners API key here.':
            new_key = input('Enter vulners api key: ')
            try:
                vulners_api = vulners.Vulners(api_key=new_key)
                f = open('apiKey', 'w')
                f.write(new_key)
                f.close()
            except:
                fixed_key = input('Incorrect API key used. Re enter key: ')
                f = open('apiKey', 'w')
                f.write(fixed_key)
                f.close()
                vulners_lib()
    else:
        new_key = input('Enter vulners api key: ')
        try:
            vulners_api = vulners.Vulners(api_key=new_key)
            f = open('apiKey', 'w')
            f.write(new_key)
            f.close()
        except:
            fixed_key = input('Incorrect API key used. Re enter key: ')
            f = open('apiKey', 'w')
            f.write(fixed_key)
            f.close()
            vulners_lib()
    CVE_List = {}
    for vulnerability in services:
        results = vulners_api.softwareVulnerabilities(vulnerability[0], vulnerability[1])
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
    if len(CVE_List) != 0:       
        result(CVE_List)
    else:
        print('No CVEs Detected.')
        clean_exit()

def result(CVE_List):
    '''Outputs the list of CVEs that were detected in vulners_lib.'''
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
    browser()

def browser():
    '''Will take user to the webpage of specific CVEs of their choosing.'''
    question = input('Do you want more information on a specific CVE? :) [y/n]: ')
    if question.lower() == 'n':
        clean_exit()
    elif question.lower() == 'y':
        cve_name = input("Which CVE? ('CVE-1234-1234'): ")
        webbrowser.open_new_tab('https://cve.mitre.org/cgi-bin/cvename.cgi?name=' + cve_name)
        browser()
    else:
        browser()

def main():
    '''Art Header'''
    font = 'graffiti'
    text = 'Project Oracle'
    r = requests.get(f'http://artii.herokuapp.com/make?text={text}&font={font}')
    print(r.text)
    print('\n')
    ip_add()

def clean_exit():
    '''Just a clean way to exit the script.'''
    sys.exit(0)

if __name__ == '__main__':
    main()