#!/usr/bin/python2.7
import transmissionrpc
import time 
import requests 

def getTransmissionData():
    tc = getTransmissionClient()
    torrents = tc.get_torrents()
    
    download = calculateTotalDownload(torrents)
    upload = calculateTotalUpload(torrents)
    sendData(download, upload)
def sendData(download, upload):
    url = 'http://localhost:8086/write?db=grafanadata'
    payload = "transmission,host=HomeServer download=" + str(download) + ",upload=" + str(upload)
    res = requests.post(url=url, data=payload)
    print res.text

def getTransmissionClient():
    return transmissionrpc.Client('localhost', port=8080)

def calculateTotalDownload(torrents):
    download = 0
    for torrent in torrents:
        download += torrent.rateDownload
    return download

def calculateTotalUpload(torrents):
    upload = 0
    for torrent in torrents:
        upload += torrent.rateUpload
    return upload

interval = 5

while True:
    start = time.clock()
    getTransmissionData()
    end = time.clock()
    time_to_sleep = interval - end - start
    time_to_sleep = 0 if time_to_sleep < 0 else time_to_sleep
    time.sleep(time_to_sleep)
