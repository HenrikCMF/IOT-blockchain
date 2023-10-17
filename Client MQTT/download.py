import requests
import paho.mqtt.client as mqtt
import sys
import util
import os
import time
import numpy as np
userid=util.userid
data_to_download="all"

def write_to_file(name, rawdata):
	
	directory=os.getcwd()
	f= open(directory + "/" + name+".csv", 'w')
	data=rawdata.rsplit("\n")
	length=np.shape(data)[0]
	for index in data:
		if util.sensors[0] in index:
			sensor0=index
		elif util.sensors[1] in index:
			sensor1=index	
		elif util.sensors[2] in index:
			sensor2=index
	#for index in range(length-2, length):
	#	f.write(data[index])
	#	f.write("\n")
	f.write(sensor0)
	f.write("\n")
	f.write(sensor1)
	f.write("\n")
	f.write(sensor2)
	f.write("\n")
	f.flush()
def download(userid):
	server= util.server # if hosted remotely on a different # if #"130.225.57.224"
	#server="172.20.0.21" # If hosted locally on a computer via docker
	port="9080"
	#port="8080"
	res = requests.get("http://"+server+":"+port+"/"+userid+".csv")
	print(res.text)
	write_to_file(userid, res.text)

def on_message():
	print("got_something")

client = mqtt.Client("Listener")
client.connect(util.server,1883,60)
client.on_connect = util.on_connect
client.on_message = on_message
#client.loop_forever()
print(str(util.topic[:-1]))
if len(sys.argv)>1:
		output=str(sys.argv[1])+","+data_to_download
		client.publish(util.topic+"download",output) # identifier
		download(sys.argv[1])
	
else:
	output=str(userid)+","+data_to_download
	client.publish(util.topic+"download",output) # identifier
	time.sleep(2)
	download(userid)
