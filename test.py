#!/usr/bin/env python3
import vulners
import json
import re

vulners_api = vulners.Vulners(api_key="DAUGMZHCAXHBC73D5MDIWRGXHLAP9P03QSWBJWXL2MGJ2W0B7GRKI5U8N334XWBQ")
#results = vulners_api.searchExploit("Apache httpd 2.4.7")

#print(json.dumps(results, indent=4))

#_____________________________________________________________________________________

results = vulners_api.softwareVulnerabilities("Apache httpd", "2.4.7")
exploit_list = results.get('exploit')
vulnerabilities_list = [results.get(key) for key in results if key not in ['info', 'blog', 'bugbounty']]
#print(json.dumps(vulnerabilities_list, indent=4))

for item in vulnerabilities_list:
    for thing in item:
        print(thing["cvelist"], thing["cvss"]["score"], thing["description"] + "\n" )
        #if re.search("2\.4\.[7-9]", thing["title"]):
            #print(json.dumps(thing, indent=4))
            #print(thing["cvelist"])
        #print(json.dumps(thing, indent=4))
