#!/bin/sh

green='\e[0;32m'
blue='\e[1;36m'
red='\e[0;31m'
purple='\e[0;35m'
clear='\e[0m'

ColorGreen () {
	echo $green$1$clear
}

ColorBlue () {
	echo $blue$1$clear
}

ColorRed () {
    echo $red$1$clear
}

ColorPurple () {
    echo $purple$1$clear
}

packages () {
    echo "$(ColorGreen 'Updating packages...')"
    apt-get update > /dev/null
    echo "$(ColorGreen 'Installing Python 3...')"
    apt-get install -y python3 > /dev/null
    echo "$(ColorGreen 'Installing NMAP...')"
    apt-get install -y nmap > /dev/null
    echo "$(ColorGreen 'Installing pip...')"
    apt-get install -y python3-pip > /dev/null
    echo "\n $(ColorBlue 'Necessary packages installed. \n')"
}

libraries () {
    echo "$(ColorGreen 'Installing nmap3 library...')"
    pip install python3-nmap > /dev/null
    echo "$(ColorGreen 'Installing vulners library...')"
    pip install -U vulners > /dev/null
    echo "\n $(ColorBlue 'Necessary Python libraries installed.')"
}

api () {
    read -p "Do you already have a vulners API key? [y/n]: " KEY_ANSWER
    case "$KEY_ANSWER" in
        [yY] | [yY][eE][sS])
            read -p "Enter the key now: " KEY
            echo $KEY > apiKey
            echo "$(ColorGreen 'Key entered.')"
            ;;
        [nN] | [nN][oO])
            echo "Go to https://vulners.com to register and obtain a key."
            ;;
    esac
}

menu () {
    read -p "
    $(ColorPurple 'What do you need help with?')
    $(ColorGreen '1)') Packages (NMAP + pip)
    $(ColorGreen '2)') Python Libraries (nmap3 + vulners)
    $(ColorGreen '3)') API key
    $(ColorGreen '4)') All of the above
    $(ColorGreen '0)') Exit
    $(ColorBlue 'Choose an option: ')" INPUT
    case $INPUT in
        1) echo "" ; packages ; sleep 1 ; menu
        ;;
        2) echo "" ; libraries ; sleep 1 ; menu
        ;;
        3) echo "" ; api ; sleep 1 ; menu
        ;;
        4) echo "" ; packages ; sleep 1 ; libraries ; sleep 1 ; api ; sleep 1 ; exit 0
        ;;
        0) exit 0
        ;;
        *) echo "    $(ColorRed 'Wrong option.')" ; sleep 1 ; menu
        ;;
    esac
}

if [ "$(id -u)" -ne 0 ]
    then echo "$(ColorRed 'Please run as sudo.')"
    exit
else
    menu
fi