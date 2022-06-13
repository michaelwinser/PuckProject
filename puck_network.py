# Network related services
# wifi connection /disconnection
# OTA updates of the software
# NTP time
# Sending notifications to the server

import wifi
import socketpool
import ssl
import ipaddress
import adafruit_ntp
import adafruit_requests
import adafruit_logging as logging
from secrets import secrets

# the socket pool
pool = None
requests = None
log = logging.getLogger("puck")
log.debug("puck_network initialized")

def connect_wifi():
    log.debug("Connecting wifi")
    global pool
    global requests

    if  not wifi.radio.enabled or pool == None or requests == None:
        wifi.radio.enabled = True
        try:
            wifi.radio.connect(secrets["ssid"], secrets["password"])
            log.info(f"connected as {wifi.radio.ipv4_address}")

            pool = socketpool.SocketPool(wifi.radio)
            requests = adafruit_requests.Session(pool, ssl.create_default_context())

        except ConnectionError as e:
            log.error(e)
            pool = None
            requests = None


        log.debug("connect_wifi requests %s", requests)

def disconnect_wifi():
    log.info("Disconnecting wifi")
    wifi.radio.enabled = False
    log.debug("pool %s requests %s", pool, requests)
    pool = None
    requests = None


def post(URL, data):
    try:
        log.debug("pool %s requests %s", pool, requests)
        response = requests.post(URL, data=data)
        text = response.text
        response.close()
    except RuntimeError as e:
        log.error(e)

    return text
