# NYC Subway Time LED Matrix Display
## Overview
#### Capabilities
- Display times for arriving trains at any NYC subway station
- Rotate through time displays for multiple stations
- [Image of display](https://github.com/techytobias/NYC-Subway-Display/blob/main/Display.JPG)
- [Video of display](https://github.com/techytobias/NYC-Subway-Display/blob/main/DisplayVideo.MOV)
## Materials
- Raspberry Pi (Pi 3 Model B or later recommended)
- SD Card (8GB Class 10 or better)
- LED Matrix. I used [this Adafruit one, which is 64 x 32 with a 5mm led spacing](https://www.adafruit.com/product/2277)
- Adafruit RGB Matrix driver. I used [this one with the RTC](https://www.adafruit.com/product/2345), but you should be able to use the regular one
- Adequate power for the display and Pi. [This adapter](https://www.adafruit.com/product/1466) should work great.
    - It's worth noting that my display is configured with 2A to the hat and 500mA to the Pi over USB. It works using lower brightness, but there is some flicker.
-Appropriate peripherals (Display, keyboard, mouse, etc) or SSH enabled by default.

## Before You Begin This Guide
- Install Raspbian (No desktop environment needed)
- Enable SSH
- Get an MTA API key [here](https://api.mta.info).
- Install PIP and Python on the Raspberry Pi (For retrieving packages)
- Follow [this Adafruit guide](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices) to get the examples running on your display.
    - Ensure that you are able to run example 0 (the rotating cube) before continuing.
    - If the display works for a second and then shuts off, you may not have sufficient power.
    - If there is severe aliasing or flickering, experiment with different values for --led-gpio-slowdown. I used --led-gpio-slowdown=2

## Creating the display
- At this point, I'm assuming that you have the rotating cube demo file working. Your file structure should look like /home/pi/rpi-rgb-led-matrix/bindings/python/samples/
- We will be keeping this file structure during this guide for the sake of simplicity.
#### Transferring Files
- Move the files rundisplay.py , mtacalls.py (be sure to add your API key) , stops.csv , and packageinst.sh to /home/pi/rpi-rgb-led-matrix/bindings/python/samples/
    -Using FileZilla over SFTP is the reccommended way to do this.
#### Installing Python dependencies
- In your SSH window, change directory to our main directory
    - cd /home/pi/rpi-rgb-led-matrix/bindings/python/samples/
- Run packageinst.sh (You may need to make the file executable using the )
    - sudo chmod +x packageinst.sh
    - sudo ./packageinst.sh
- Check your work. You should see lots of new folders in the /home/pi/rpi-rgb-led-matrix/bindings/python/ directory.
### Running the code
- First, make rundisplay.py executable
    - sudo chmod +x rundisplay.py
- Then, run the code (Modify this code as needed for your display).
    - sudo ./rundisplay.py --led-rows=32 --led-cols=64 --led-slowdown-gpio=2 -b=30
- You should see train times appear after a few minutes of the code running. You should see the times appear on your terminal window as they are loaded by the API as well.
- If this works, jump to the customization section. If not, follow the troubleshooting section.

## Troubleshooting
#### Basic Troubleshooting
- Ensure whatever file you are trying to run is executable
    - sudo chmod +x filename.abc
- Ensure all python packages are loaded
- Ensure you entered your API key probably
- Recheck whether you can run the rotating cube demo file

#### More Advanced Troubleshooting
- edit mtacalls.py using nano to add the below line:
    - print(totalstationtimes("A41"))
- then, run mtacalls.py
    - sudo python3 mtacalls.py
- you should see train times print out after a few seconds. If you don't, and you see a python error, search the error on stack exchange.

## Customization
- Use stops.csv to find the code for your desired station(s). Use only the first three letters.
    - e.g, 232 for Borough Hall, or A41 for Jay-St Metrotech.
    - Note that the station names for some stations in stops.csv have been shortened to fit better on the display.
    
    



