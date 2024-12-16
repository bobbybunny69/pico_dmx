from secret import wifi
import network
import time
from artnet_rs import ArtnetServer
from neopixel import Neopixel

REFRESH_MS = 50

np = Neopixel(50,0,0)
np.clear()
np.show()

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi['ssid'], wifi['pw'])
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
ip_addr = wlan.ifconfig()[0]
print("Connected to Wi-Fi. My IP Address:", ip_addr)

a = ArtnetServer(ip_addr,1000)   # 1 second timeout

try:
    while True:
        tic = time.ticks_ms()
        data = a.recv_data()
        #while time.ticks_ms()-tic < REFRESH_MS:
        if data != None:
            print(data)
            np.set_pixel_line(0,11,(data[0:3]))
            np.set_pixel_line(13,24,(data[3:6]))
            np.set_pixel_line(25,36,(data[6:9]))
            np.set_pixel_line(38,49,(data[9:12]))
            np.show()
        toc = time.ticks_ms()
        print("Time stamp [ms]: ", toc-tic)
finally:
    print("Finishing....")
    a.close()
