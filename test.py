#!/usr/bin/env python3
import vulners
import json
import re

vulners_api = vulners.Vulners(api_key="DAUGMZHCAXHBC73D5MDIWRGXHLAP9P03QSWBJWXL2MGJ2W0B7GRKI5U8N334XWBQ")

#print(json.dumps(results, indent=4))

#_____________________________________________________________________________________

#Create a variable to input multiple vunerabilities into a list
library = [["Apache httpd", "2.4.7"], ["OpenSSH", "6.6"]]
#Loop through vulnerability list to output CVE
for vulnerability in library:
    results = vulners_api.softwareVulnerabilities(vulnerability[0], vulnerability[1])
    exploit_list = results.get('exploit')
    vulnerabilities_list = [results.get(key) for key in results if key not in ['info', 'blog', 'bugbounty']]
    for item in vulnerabilities_list:
        for specific in item:
            print(specific["cvelist"], "Score =", specific["cvss"]["score"], "\n", specific["title"], "\n" )



       

