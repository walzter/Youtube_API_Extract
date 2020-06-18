#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 18:55:25 2020

@author: Eric W

"""
from googleapiclient.discovery import build
from time import sleep
from random import randint
import pandas as pd
import time

save_path = YOUR PATH HERE

#our API Key 
api_key = YOUR API KEY

#initating the service 
youtube = build('youtube','v3',developerKey=api_key)

#list of channel ID's 
chan_id = ['UC4YOFVk_s7iSqyTWyGK_cMg', 
           'UCQruJDvxfM3b4-qNVIuarSQ',
           'UC-xSFGtsLN0kiZGoPYEhzMg',
           'UCcJAeaMvWQp8Czpz31S7ptQ']

chan_data = []

def yt_data():
    
    '''Making two api calls, one for getting 
    the title of the channel and the other 
    to get the data'''
    
    #iterate over the channel ids we want 
    for channel in chan_id: 
        #ask the request for the snippet 
        request = youtube.channels().list(
            part = 'snippet', 
            id = channel 
        )
        #excecute response
        response = request.execute()
        #get the title from the json file 
        title = response['items'][0]['snippet']['title']
        #random sleep for not calling too quickly
        sleep(randint(2,10))
        #second request for statistics about the channel 
        request_2 = youtube.channels().list(
            part = 'statistics', 
            id = channel 
        )
        #executing the second call 
        response_2 = request_2.execute()
        #getting subscribers, total views, and number of videos 
        Subs = response_2['items'][0]['statistics']['subscriberCount']
        tot_view = response_2['items'][0]['statistics']['viewCount']
        vid_count = response_2['items'][0]['statistics']['videoCount']
        print('')
        print(f'Getting data for: {title},', '\n', f'with ChannelID: {channel}')
        print('')
        data_dict = {
                'Channel':title,
                'Subs':Subs,
                'Videos':vid_count,
                'Views':tot_view,
                'Channel_ID':channel
                }
        chan_data.append(data_dict)
    
    #convert list of dictionaries to data frame
    date_time = time.strftime("%d%m%Y")
    df_acc = pd.DataFrame(chan_data)
    df_acc.to_csv(save_path + 'AccountData_' + date_time + '_.csv')
    
    print("Files have succesfully been saved as CSV in the Data Folder")

    return chan_data

yt_data()
