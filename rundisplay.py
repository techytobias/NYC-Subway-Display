#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
from pandas import pandas as pd
import time
import mtacalls
#import pandas as pd

df=pd.read_csv("stops.csv")
df.head()
stops=pd.Series(df.stop_name.values,index=df.stop_id).to_dict()



def cycler(mtacalls, station):
    packet=[]
    #2,3
    times=mtacalls.totalstationtimes(station)
    while len(packet)<5:
        for time in times:
            if time[1]>2:
                packet.append(time)
    print(packet)
    return packet



class GraphicsTest(SampleBase):
    def __init__(self, packet, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)
        self.packet=packet

    def run(self):
        canvas = self.matrix
        font = graphics.Font()
        font.LoadFont("../../../fonts/5x8.bdf")
        white=graphics.Color(255, 255, 255)
        seventh = graphics.Color(255, 0, 0)
        lexington = graphics.Color(0, 146, 66)
        eigth = graphics.Color(0, 57, 163)
        sixth = graphics.Color(255, 99, 32)
        black= graphics.Color(0, 0, 0)
      
        for i in range(63):
            graphics.DrawLine(canvas, 0, i, 64, i, black)
        c=0
        for subpacket in self.packet:
            c+=1
            for i in range(63):
                graphics.DrawLine(canvas, 0, i, 64, i, black)
            
            traincharspacing=7
            b=0
            for train in subpacket:
                if train[2][3] == "N":
                    if b<2:
                        if train[0]=="4" or train[0]=="5":
                            color=lexington
                        elif train[0]=="3" or train[0]=="2":
                            color=seventh
                        elif train[0]=="A" or train[0]=="C":
                            color=eigth
                        elif train[0]=="F" or train[0]=="M":
                            color=sixth
                        else:
                            color=white
                        try:
                            textstring=str(train[0]+" "+str(stops[train[2]][:8]))
                        except:
                            textstring="textfail"
                        graphics.DrawText(canvas, font, 0, traincharspacing, color, textstring)
                        graphics.DrawText(canvas, font, 53, traincharspacing, color, str(train[1]))
                        traincharspacing+=8
                        b+=1
            traincharspacing=23
            b=0
            for train in subpacket:
                if train[2][3] == "S":
                    if b<2:
                        if train[0]=="4" or train[0]=="5":
                            color=lexington
                        elif train[0]=="3" or train[0]=="2":
                            color=seventh
                        elif train[0]=="A" or train[0]=="C":
                            color=eigth
                        elif train[0]=="F" or train[0]=="M":
                            color=sixth
                        else:
                            color=white
                        try:
                            textstring=str(train[0]+" "+str(stops[train[2]][:8]))
                        except:
                            textstring="textfail"
                        graphics.DrawText(canvas, font, 0, traincharspacing, color, textstring)
                        graphics.DrawText(canvas, font, 53, traincharspacing, color, str(train[1]))
                        traincharspacing+=8
                        b+=1
            if c<3:
                print("sleeping")
                time.sleep(10)
            else:
                print("not sleeping")      
        #time.sleep(10)
                
        
        
        
        #graphics.DrawLine(canvas, 0, 8, 64, 8, white)

#        green = graphics.Color(0, 255, 0)
#        graphics.DrawCircle(canvas, 15, 15, 10, green)

        
        #graphics.DrawText(canvas, font, 0, 7, lexington, "Eastchester-Dyre Av")
        #graphics.DrawText(canvas, font, 0, 16, seventh, "Flatbush Av")

        
        #time.sleep(10)  # show display for 10 seconds before exit
        

# Main function
while True:
    if __name__ == "__main__":
        packet1=cycler(mtacalls, "232")
        packet2=cycler(mtacalls, "A41")
        packet3=cycler(mtacalls, "423")
        packet=[packet1, packet2, packet3]
        graphics_test = GraphicsTest(packet)
        #packet=cycler(mtacalls, "423")
#        time.sleep(14)
#        #packet=[[2, "F06S", 8],["F", "D43S", 10],["A", "A03N", 13],[4, "232N", 16]]
        #graphics_test = GraphicsTest(packet)
#        packet=cycler(mtacalls, "A41")
#        time.sleep(14)
#        #packet=[[2, "F06S", 8],["F", "D43S", 10],["A", "A03N", 13],[4, "232N", 16]]
#        graphics_test = GraphicsTest(packet)
        if (not graphics_test.process()):
            print("isrunning")
            graphics_test.print_help()
