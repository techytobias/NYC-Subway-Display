#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
from subprocess import check_output
import csv
import time
import mtacalls2
import os
stops = {}
with open("stops.csv", 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        stops.update({row[0]: row[1]})

class GraphicsTest(SampleBase):
    def __init__(self, packet, servicedata, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)
        self.packet=packet
        self.servicedata=servicedata
    def getcolor(self, trainline):
        white=graphics.Color(255, 255, 255)
        seventh = graphics.Color(255, 0, 0)
        lexington = graphics.Color(0, 146, 66)
        eigth = graphics.Color(0, 57, 163)
        sixth = graphics.Color(255, 99, 32)
        bway=graphics.Color(255,255,0)
        jamaica=graphics.Color(165,42,42)
        nassau=graphics.Color(107,187,78)
        flushing=graphics.Color(185,52,170)
        atlantic=graphics.Color(167,169,172)
        if trainline=="4" or trainline=="5" or trainline=="6":
            color=lexington
        elif trainline=="3" or trainline=="2" or trainline=="1":
            color=seventh
        elif trainline=="J" or trainline=="Z":
            color=jamaica
        elif trainline=="A" or trainline=="C" or trainline=="E" or trainline=="H":
            color=eigth
        elif trainline=="F" or trainline=="M" or trainline=="B" or trainline=="D":
            color=sixth
        elif trainline=="N" or trainline=="Q" or trainline=="R" or trainline=="W":
            color=bway
        elif trainline=="G":
            color=nassau
        elif trainline=="L":
            color=atlantic
        elif trainline=="7":
            color=flushing
        else:
            color=white
        return color
    def run(self):
        canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/5x8.bdf")
        black= graphics.Color(0, 0, 0)
        white=graphics.Color(255, 255, 255)
        canvas.Clear()
        c=0
        for subpacket in self.packet:
            c+=1
            pos = 14
            posi2=14
            northhvalues=[[0, 30],[0,30]]
            southhvalues=[[0, 30],[0,30]]
            t_end = time.time() + 1 * 8  #last values controls display time per station in seconds
            while time.time() < t_end:
                canvas.Clear()
                traincharspacing=7
                b=0
                for train in subpacket:
                    if train[2][3] == "N":
                        if b<2:
                            color=self.getcolor(train[0])
                            try:
                                textstring=str(train[0])
                            except:
                                textstring="textfail"
                            len2=(len(str(stops[train[2]]))*5)
                            if len2>40:
                                northhvalues[b][0]=10-len2+42
                                posi2=northhvalues[b][1]
                                if northhvalues[b][1]<=northhvalues[b][0]-20:
                                    northhvalues[b][1]=30
                                    posi2=northhvalues[b][1] 
                                if posi2<=northhvalues[b][0] and posi2>=northhvalues[b][0]-20:
                                    posi2=northhvalues[b][0]
                                if northhvalues[b][1]>=10:
                                    posi2=10
                            else:
                                posi2=10
                            len3 = graphics.DrawText(canvas, font, posi2, traincharspacing, color, str(stops[train[2]]))
                            for i in range(9):
                                    graphics.DrawLine(canvas, i, traincharspacing-7, i, traincharspacing, graphics.Color(0, 0, 0))
                            for i in range(52,64):
                                    graphics.DrawLine(canvas, i, traincharspacing-7, i, traincharspacing, graphics.Color(0, 0, 0))
                            graphics.DrawText(canvas, font, 0, traincharspacing, color, textstring)
                            graphics.DrawText(canvas, font, 55, traincharspacing, color, str(train[1]))
                            traincharspacing+=8
                            northhvalues[b][1]-=1
                            b+=1
                traincharspacing=23
                b=0
                destinations=[]
                for train in subpacket:
                    if train[2][3] == "S":
                        if b<2:
                            color=self.getcolor(train[0])
                            try:
                                textstring=str(train[0])
                            except:
                                textstring="textfail"
                            len2=(len(str(stops[train[2]]))*5)
                            if len2>40:
                                southhvalues[b][0]=10-len2+42
                                posi2=southhvalues[b][1]
                                if southhvalues[b][1]<=southhvalues[b][0]-20:
                                    southhvalues[b][1]=30
                                    posi2=southhvalues[b][1] 
                                if posi2<=southhvalues[b][0] and posi2>=southhvalues[b][0]-20:
                                    posi2=southhvalues[b][0]
                                if southhvalues[b][1]>=10:
                                    posi2=10
                            else:
                                posi2=10
                            len3 = graphics.DrawText(canvas, font, posi2, traincharspacing, color, str(stops[train[2]]))
                            for i in range(9):
                                    graphics.DrawLine(canvas, i, traincharspacing-7, i, traincharspacing, graphics.Color(0, 0, 0))
                            for i in range(52,64):
                                    graphics.DrawLine(canvas, i, traincharspacing-7, i, traincharspacing, graphics.Color(0, 0, 0))
                            graphics.DrawText(canvas, font, 0, traincharspacing, color, textstring)
                            graphics.DrawText(canvas, font, 55, traincharspacing, color, str(train[1]))
                            traincharspacing+=8
                            southhvalues[b][1]-=1
                            b+=1
                time.sleep(0.05)
                canvas = self.matrix.SwapOnVSync(canvas)
            if c<3:
                print("sleeping")
            elif c==3:
                canvas.Clear()
                graphics.DrawText(canvas, font, 0, 8, white, "Disruptions:")
                print("servicedata showing")
                charspace=0
                vertspace=17
                trainnum=1
                for problemtrain in self.servicedata:
                    color=self.getcolor(problemtrain)
                    graphics.DrawText(canvas, font, charspace, vertspace, color, problemtrain)
                    charspace +=7
                    trainnum+=1
                    if trainnum >= 10:
                        vertspace+=8
                        trainnum=1
                        charspace=0
                    #Add ip to disruptions screen
                    ipaddr=str(check_output(['hostname', '-I']))[9:]
                    
                    ipaddr2="IP: " + ipaddr[:-3]
                    graphics.DrawText(canvas, font, 0, 32, graphics.Color(10,169,172), ipaddr2)
                canvas = self.matrix.SwapOnVSync(canvas)
            else:
                print("fetching data")      

while True:
    if __name__ == "__main__":
        worked=0
        while worked==0:
            try:
                packet=mtacalls2.totalstationtimes(["423", "A41", "232"])
                servicedata=mtacalls2.procservicedata()
                worked=1
            except:
                print("rebooting in 30 seconds")
                time.sleep(30)
                subprocess.Popen('sudo reboot -n', shell=True)              
        for timegroup in packet:
            for singletime in timegroup:
                if singletime[1]<2:
                    timegroup.remove(singletime)
        
        graphics_test = GraphicsTest(packet, servicedata)

        if (not graphics_test.process()):
            print("isrunning")
            graphics_test.print_help()
            