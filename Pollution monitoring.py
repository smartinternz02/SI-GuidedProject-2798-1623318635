import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import json



#Provide your IBM Watson Device Credentials
organization = "gaxcrt"
deviceType = "iotdevice"
deviceId = "1001"
authMethod = "token"
authToken = "Chinna@9966"




# Initialize the device client.
co2=0
n2=0
la=0
lg=0
loc=[]



def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data['command'])




    if cmd.data['command']=='lighton':
        print("LIGHT ON IS RECEIVED")


    elif cmd.data['command']=='lightoff':
       print("LIGHT OFF IS RECEIVED")

    if cmd.command == "setInterval":
        if 'interval' not in cmd.data:
            print("Error - command is missing required information: 'interval'")
        else:
            interval = cmd.data['interval']
    elif cmd.command == "print":
        if 'message' not in cmd.data:
            print("Error - command is missing required information: 'message'")
        else:
            print(cmd.data['message'])



try:
    deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
    deviceCli = ibmiotf.device.Client(deviceOptions)
#..............................................

except Exception as e:
    print("Caught exception connecting device: %s" % str(e))
    sys.exit()



# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()



while True:
    co2=89
    n2=45
    la=16.0948
    lg=80.1656
    loc="chilakaluripet"
    #Send waterlevel & light intensity to IBM Watson
    data = {"d":{ 'CO2' : co2, 'N2': n2,'LA': la,'LG': lg,"LOC": loc, }}
    #print data
    def myOnPublishCallback():
        print ("Published CO2 = %s units" % co2, "N2 = %s %%" % n2, "LA = %s degrees" % la, "LG = %s degrees %% " % lg,"to IBM Watson")
    success = deviceCli.publishEvent("Data", "json", data, qos=0, on_publish=myOnPublishCallback)
    if not success:
        print("Not connected to IoTF")
    time.sleep(1)
    deviceCli.commandCallback = myCommandCallback



# Disconnect the device and application from the cloud
deviceCli.disconnect()
