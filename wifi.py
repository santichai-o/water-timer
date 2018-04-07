"""WiFi configuration."""
import network
from utime import ticks_ms, ticks_diff, sleep
import config

WIFI_DELAY = 20
CHECK_INTERVAL = 0.2


def connect():
    """Connect to WiFi."""
    connected = False
    start = ticks_ms()

    print('Connecting to network...')

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(config.WIFI_SSID, config.WIFI_PASSPHRASE)

    secs = WIFI_DELAY
    while secs >= 0 and not sta_if.isconnected():
        sleep(CHECK_INTERVAL)
        secs -= CHECK_INTERVAL
    if sta_if.isconnected():
        print('Network, address: %s in %d ms' %
              (sta_if.ifconfig()[0], ticks_diff(ticks_ms(), start)))
        connected = True

    return connected


def disconnect():
    """Disconnect from WiFi."""
    sta_if = network.WLAN(network.STA_IF)
    if sta_if.isconnected():
        sta_if.disconnect()

    secs = WIFI_DELAY
    while secs >= 0 and sta_if.isconnected():
        sleep(CHECK_INTERVAL)
        secs -= CHECK_INTERVAL