import google.transit
from google.transit import gtfs_realtime_pb2
import requests
import time # imports module for Epoch/GMT time conversion
import os # imports package for dotenv
from protobuf_to_dict import protobuf_to_dict

def getdata():
    realtime_data1=[]
    links=["https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace","https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm", "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"]
    for link in links:
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(link, headers={"x-api-key": 'I1y5ts3GAB6J7AtSeIHva8eJIX1zv7t43heX6hRv'})
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
            unique_train_schedule = trains['trip_update'] # train_schedule is a dictionary with trip and stop_time_update
#            if (unique_train_schedule['trip']['route_id']) != train:
#              continue
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
                            ctimes.append([trainletter, int(((unique_time - int(time.time())) / 60)), stop])
            except:
                pass
    return ctimes

def totalstationtimes(station):
    stations=[(station + "N"), (station + "S")]
    data=getdata()
    newdata=[]
    for station1 in stations:
        arrd=gettimes(data,station1)
        for element in arrd:
            newdata.append(element)
    newdata.sort(key=lambda row: (row[1], row[0]), reverse=False)
    return newdata
