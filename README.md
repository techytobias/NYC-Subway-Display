# NYC Subway Time LED Matrix Display
## Overview
#### Capabilities
- Display times for arriving trains at any NYC subway station
- Rotate through time displays for multiple stations
- [Image of display](https://github.com/techytobias/NYC-Subway-Display/blob/main/Display.JPG)
## Materials
- Raspberry Pi (Pi 3 Model B or later recommended)
- SD Card (8GB Class 10 or better)
- LED Matrix. I used [this Adafruit one, which is 64 x 32 with a 5mm led spacing](https://www.adafruit.com/product/2277)
- Adafruit RGB Matrix driver. I used [this one with the RTC](https://www.adafruit.com/product/2345), but you should be able to use the regular one
- Adequate power for the display and Pi. [This adapter](https://www.adafruit.com/product/1466) should work great.
    - It's worth noting that my display is configured with 2A to the hat and 500mA to the Pi over USB. It works, but there is some flicker.
-Appropriate peripherals (Display, keyboard, mouse, etc) or SSH enabled by default.

## Before You Begin This Guide
- Install Raspbian (No desktop environment needed)
- Enable SSH
- Follow [this Adafruit guide](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices) to get the examples running on your display.
    - Ensure that you are able to run example 0 (the rotating cube) before continuing.
    - If the display works for a second and then shuts off, you may not have sufficient power.
    - If there is severe aliasing or continous flickering, experiment with different values for --led-gpio-slowdown. I used --led-gpio-slowdown=2

## Creating the display
- At this point, I'm assuming that you have the rotating cube demo file working. Your file structure should look like /home/pi/rpi-rgb-led-matrix/bindings/python/samples/
- We will be keeping this file structure during this guide for the sake of simplicity.




