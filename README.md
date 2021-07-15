## Overview
this is unofficial Anker Soundcore Life Q Headphone api


## Process of controlling Soundcore life headphones
I used Oneplus 7T which it had buildin OnePlus Logkit by opening phone app and dial `*#800#`
and let it capture whatever the Anker soundcore app was sending to the Headphone once this is done
I Disable the Log and disconnect Headphone and go on my PC connect to the phone via USB to get the log
which for Oneplus 7T one is located at `This PC\HD1907\Internal shared storage\Android\data\oem_log\btsnoop`
and i used another software called [WireShark](https://www.wireshark.org/) and read those data
Notes those data for Ambient Sound length is 28 and the name starts with `Fantasia` channel(port) 12
for EQs they are bit different the length is 34 and Protocol is `SPP` here are the example what it looks like
I hope this helps you to control your type of Headphone such as Sony and other brands of Bluetooth headphone
![image](https://user-images.githubusercontent.com/55416314/125717315-00466cf3-78d9-4141-987e-96d4af34914d.png)


## the Script
ive made a little script that you can use to control your Anker Soundcore life Q headphone it can change your headphone Modes to Transparency, Normal,
ANC, Transport, Indoor, and Outdoor and Even it can control EQ. Sadly I wasnt able to figure out how the custom EQ thing work i tired using same method
it just creates a new Custom presets which i dont want also the Script requires Python 3.9.6 because any older then that does not have `AF_Bluetooth` and RFCOMM Protocol there are also some Libraries for Bluetooth such as PyBluez but that didnt work too well for me so i decided to use Python buildin Bluetooth which is Sockets


## Bugs
If theres are any bugs, Issues or if you need help feel free use Issue tab

## Contribute
Feel Free to suggest a pull request or Fork
