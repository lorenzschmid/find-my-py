import socket
import machine
import network
import time

print("Main: Setup Netwok: AP")

# Setup Network
u_id = machine.unique_id()
my_essid = "find_my_py" + str(u_id[0]+u_id[1]+100*(u_id[2]+u_id[3]))
beacon_pw = "micropythoN"


ap = network.WLAN(network.AP_IF)
ap.active(True)
# Set WiFi access point name (formally known as ESSID) and WiFi channel
ap.config(essid=my_essid, channel=11)
#ap.config(authmode=3, password='hello')


# Query params one by one
print(ap.config('essid'))
print(ap.config('channel'))

print("Done AP setup")


while(True):

    has_client = ap.isconnected()
    print("Client connected: " + str(has_client))
    time.sleep(1)

# Reconfigure to client

print("Reconfigure to client: sta_if status")
sta_if = network.WLAN(network.STA_IF)

print("sta_if.active: " + str(sta_if.active()) )
print("ap.active: " + str(ap.active()) )

sta_if.active(True)
print("sta_if.active: " + str(sta_if.active()) )
print("ap.active: " + str(ap.active()) )


print("Is connected: " + str(sta_if.isconnected()) )