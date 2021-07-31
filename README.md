# Project Oracle
Uses NMAP along with the vulners library to find common vulnerabilities on a machine.
___
### Obtaining Vulners API key

Go to the [Vulners website](https://vulners.com) and click on "Get Started" in the top right corner. Once you've registered, click on your name in the top corner and
under the "API KEYS" tab, generate an API key with scope "api".
___
### REQUIRMENTS
* NMAP is required in order to run.
```bash
sudo apt-get install nmap
```
```bash
pip install python3-nmap
```
```bash
pip install -U vulners
```
```bash
echo 'enter vulners API key' > /path/to/ProjectOracle/apiKey
```
___
### TROUBLESHOOTING
If you are using Firefox and get the following error messages:

![image](https://user-images.githubusercontent.com/64572574/127598904-71dba5a8-2d18-4c9b-8615-496e958128b6.png)

1. Open Firefox and type 'about:config' into the URL bar.
1. Enter 'sandbox' into the search bar.
1. Change the value of 'security.sandbox.content.level' to 0.
1. Close Firefox.

![image](https://user-images.githubusercontent.com/64572574/127601514-43c4193b-dfb7-477d-8613-6230e02f3227.png)
