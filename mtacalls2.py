import google.transit
from google.transit import gtfs_realtime_pb2
import requests
import time # imports module for Epoch/GMT time conversion
import os # imports package for dotenv
from protobuf_to_dict import protobuf_to_dict
import subprocess

def getdata():
    realtime_data1=[]
    links=["https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace","https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm", "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"]
    for link in links:
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(link, headers={"x-api-key": 'YOUR_API_KEY_HERE_KEEP_APOSTORPHES'})
        feed.ParseFromString(response.content)
        subway_feed = protobuf_to_dict(feed) # subway_feed is a dictionary
        realtime_data = subway_feed['entity'] # train_data is a list
        for element in realtime_data:
            realtime_data1.append(element)
    return realtime_data1


def gettimes(data, station):
    arrivaldata=[]
    trainletters=[]
    ctimes=station_time_lookup(data, station)
    ctimes.sort(key=lambda row: (row[1], row[0]), reverse=False)
    return ctimes[:6]


def station_time_lookup(train_data, station):
    ctimes=[]
    for trains in train_data: # trains are dictionaries
        if trains.get('trip_update', False) != False:
            unique_train_schedule = trains['trip_update'] # train_schedule is a dictionary with trip 
            try:
                unique_arrival_times = unique_train_schedule['stop_time_update'] # arrival_times is a list of arrivals
                for scheduled_arrivals in unique_arrival_times: #arrivals are dictionaries with time data and stop_ids
                    if scheduled_arrivals.get('stop_id', False) == station:
                        s1=unique_train_schedule
                        trainletter=s1['trip']['route_id']

                        test5=unique_arrival_times[-1]
                        stop=test5['stop_id']

                        time_data = scheduled_arrivals['arrival']
                        unique_time = time_data['time']
                        
                        if unique_time != None:
                            mintoarrival=mintoarrival=int(((unique_time - int(time.time())) / 60))
                            if mintoarrival > 2: #only displays trains 3 or more mins away
                                ctimes.append([trainletter, mintoarrival, stop])
            except:
                pass
    return ctimes

def totalstationtimes(stationlist):
    finaldata=[]
    try:
        data=getdata()
    except:
        print("datafail")
        time.sleep(30)
        subprocess.Popen('sudo reboot -n', shell=True)
    print("datagot")
    for station in stationlist:
        stations=[(station + "N"), (station + "S")]
        newdata=[]
        for station1 in stations:
            arrd=gettimes(data,station1)
            for element in arrd:
                newdata.append(element)
        newdata.sort(key=lambda row: (row[1], row[0]), reverse=False)
        finaldata.append(newdata)
    return finaldata

def getservicedata():
    realtime_data1=[]
    links=["https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts"]
    for link in links:
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(link, headers={"x-api-key": 'YOUR-API-KEY-KEEP-THE-APOSTROPHES'})
        feed.ParseFromString(response.content)
        subway_feed = protobuf_to_dict(feed) # subway_feed is a dictionary
        realtime_data = subway_feed['entity'] # train_data is a list
        for element in realtime_data:
            realtime_data1.append(element)
    return realtime_data1


def procservicedata():
    problemtrains=[]
    mainlist=getservicedata()[:10]
    mainlist2=[]
    for element in mainlist:
        if element["id"][4]=="a": #seperates active alerts from planned service changes
            mainlist2.append(element["alert"]["informed_entity"])

    for element4 in mainlist2:
        for element5 in element4:
            try:
                if element5["route_id"] not in problemtrains:
                    if "S" not in element5["route_id"]:
                        problemtrains.append(element5["route_id"])
            except:
                pass
    if len(problemtrains)==0:
        problemtrains=["None"]
    problemtrains.sort()
    return problemtrains
#print(totalstationtimes(["232", "A41"]))
print(procservicedata())
