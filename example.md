Example of Project Oracle

For running Project Oracle, the user will need to have nmap and python installed on their machine.

```bash
sudo apt-get install nmap
```
```bash
sudo apt-get install python3 
```
The user will need the nmap3 and vulners python libraries installed.
```bash
pip install python3-nmap
```
```bash
pip install -U vulners
```
Lastly, make sure to add your vulners API key to the apiKey file.

Go to the [Vulners website](https://vulners.com) and click on "Get Started" in the top right corner. Once you've registered, click on your name in the top corner and under the "API KEYS" tab, generate an API key with scope "api".
```bash
echo 'enter vulners API key' > /path/to/ProjectOracle/apiKey
```
After downloading Project Oracle, run the executable ‘Oracle.py’ in the package.

<img width="808" alt="Screen Shot 2021-07-31 at 12 12 07 PM" src="https://user-images.githubusercontent.com/78869645/127751253-b19d13e9-9ceb-4155-b15a-8804c82721aa.png">


You will be prompted to enter your target IP address or URL address.

<img width="825" alt="Screen Shot 2021-07-31 at 12 28 19 PM" src="https://user-images.githubusercontent.com/78869645/127751296-d2efefa0-1204-4bc9-a90a-e18a62eea3c4.png">


The first output will show the user the open ports and services on the target machine.

Next, the user will be prompted to enter their minimum CVE score desired by typing in a number from 1 - 10 or to get all CVE output, type in ‘all’.

<img width="907" alt="Screen Shot 2021-07-31 at 12 41 16 PM" src="https://user-images.githubusercontent.com/78869645/127751304-859aa990-673f-4af1-8540-90b94f0ddcda.png">



After inputting the minimum score, you will see the CVE number, score and title for the vulnerability on the machine within the given range.

The next question will ask if you would like to find out more about a specific vulnerability.  Type in ‘y’ for yes or ‘n’ for no.  If you type in ‘n’, the program will exit.  If you type ‘y’, you will then be prompted to type in the specific CVE you are looking to learn more about.

<img width="929" alt="Screen Shot 2021-07-31 at 12 43 24 PM" src="https://user-images.githubusercontent.com/78869645/127751315-249a0cba-a3cf-4d88-99a8-99613be491eb.png">


Typing in a specific CVE will open your browser to cve.mitre.org to find out more information on the vulnerability selected.  You can continue looking up CVE’s through the program after exiting the browser.
