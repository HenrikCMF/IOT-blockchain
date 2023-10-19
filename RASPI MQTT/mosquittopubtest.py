import time
import paho.mqtt.client as mqtt
import util
import os
import threading
import PI_sensors
msg_mutex=threading.Lock()
msg_received=0
my_name=None
client = mqtt.Client()

sleeptime=0
####client.subscribe("my/topic")
# The callback for when the client receives a CONNACK response from the server.
def set_mutex(inputs):
    global msg_mutex
    global msg_received
    msg_mutex.acquire()
    try:
        msg_received=inputs
    finally:
        msg_mutex.release()
def check_mutex():
    global msg_mutex
    global msg_received
    msg_mutex.acquire()
    try:
        result=msg_received
    finally:
        msg_mutex.release()
    return result

def on_message(client, userdata, msg):
    print("onmessage")
    print(msg.topic+" "+str(msg.payload))
    global msg_received
    global my_name
    if str(msg.topic)=='Name':
        with open("myname.txt", "w", encoding="utf8") as file:
            file.write(str(format(msg.payload.decode("utf-8"))))
        file.close()
        my_name=str(format(msg.payload.decode("utf-8")))
        set_mutex(1)
    elif str(msg.topic)=='Pinger':
        set_mutex(1)
    elif str(msg.topic)=='parameters'+my_name:
        sleeptime=float(format(msg.payload.decode("utf-8")))
    


client.on_connect = util.on_connect

client.on_message = on_message

print(util.server)
client.connect(util.server,1883,60)

client.subscribe('test')
def get_a_name():
    print('getting a new name')
    global msg_received
    client.subscribe('Name')
    client.loop_start()
    topic='New sensor'
    msg='hello'
    client.publish(topic, msg)
    while check_mutex()==0:
        time.sleep(1)
    client.unsubscribe('Name')
    client.loop_stop()
    print("got a name")
    set_mutex(0)

def remember_me():
    client.subscribe('Pinger')
    client.loop_start()
    topic=util.topic+my_name
    msg='hello'
    client.publish(topic, msg)
    time.sleep(1)
    client.unsubscribe('Pinger')
    client.loop_stop()
    if check_mutex()==0:
        get_a_name()
    else:
        set_mutex(0)
    
    
    
if not os.path.exists("myname.txt"):
    print('dont have a name yet')
    get_a_name()
else:
    
    with open("myname.txt", "r", encoding="utf8") as file:
        my_name=file.read()
        print('my name is:',my_name)
    file.close()
    remember_me()
client.subscribe('parameters'+my_name)


counter = 0
arr_size = 1
userid=util.userid
extra_counter=0

# Temperature, pressure and humidty - BME680
data_temp = [0] * arr_size
timestamps_temp = [0] * arr_size

data_humidity = [0] * arr_size
timestamps_humidity = [0] * arr_size

# Air quality - SGP30
data_airquality = [0] * arr_size
timestamps_airquality = [0] * arr_size

data_pos= [0] * arr_size
timestamps_pos = [0] * arr_size



while 1:
    temp_sample, ts_temp = util.rand_sample()

    #data_temp[counter] = temp_sample
    data_temp[counter] = 2
    timestamps_temp[counter] = ts_temp

    airqual_sample, ts_qual = util.rand_sample()
    data_airquality[counter] = airqual_sample
    timestamps_airquality[counter] = ts_qual
    pos_sample, ts_pos = util.rand_sample()
    data_pos[counter] = 1
    timestamps_pos[counter] = ts_pos
    counter+=1
    if counter == arr_size:
        extra_counter+=1
        counter = 0
        client.loop_start()
        data=util.prepare_payload([util.sensors[0]+" "+my_name,
        util.sensors[1]+" "+my_name, util.sensors[2]+" "+my_name], 
        [data_pos,data_temp, data_airquality] ,
        [timestamps_pos, timestamps_temp, timestamps_airquality])
        
        util.send_topics(data,userid,client)

        data_temp = [0] * arr_size 
        timestamps_temp = [0] * arr_size


        data_airquality = [0] * arr_size
        timestamps_airquality = [0] * arr_size

        
        util.send_topics(data,userid,client)
        time.sleep(1)
        client.loop_stop()
        time.sleep(sleeptime)


                    
        
