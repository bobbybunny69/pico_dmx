from secret import wifi
import network
import time
from artnet_rs import ArtnetServer

REFRESH_MS = 40

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi['ssid'], wifi['pw'])
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
ip_addr = wlan.ifconfig()[0]
print("Connected to Wi-Fi. My IP Address:", ip_addr)

a = ArtnetServer(ip_addr,20)

try:
    while True:
        tic = time.ticks_ms()
        time.sleep_ms(10)
        data = a.recv_data()
        time_elapsed = time.ticks_ms()-tic
        time.sleep_ms(REFRESH_MS-time_elapsed)
        toc = time.ticks_ms()
        if data != None:
            print(data)
        print("Time stamp [ms]: ", toc-tic)
finally:
    print("Finishing....")
    a.close()
