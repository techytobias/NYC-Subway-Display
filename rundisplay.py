from samplebase import SampleBase
from rgbmatrix import graphics
from pandas import pandas as pd
import time
import mtacalls2

df=pd.read_csv("stops.csv")
df.head()
stops=pd.Series(df.stop_name.values,index=df.stop_id).to_dict()

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
            if c<(len(self.packet)):
                print("sleeping")
                time.sleep(10)
            else:
                print("not sleeping")      
        

# Main function
while True:
    if __name__ == "__main__":
        packet=mtacalls.totalstationtimes(["232", "A41", "423"])
        graphics_test = GraphicsTest(packet)
        if (not graphics_test.process()):
            print("isrunning")
            graphics_test.print_help()
