# Write your code here :-)
import tinys3
import time
import random
import wifi
import socketpool
import adafruit_requests
from secrets import secrets
import ssl
import ipaddress
import alarm
import board

def connect_wifi():
    wifi.radio.enabled = True
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    print(wifi.radio.ipv4_address)
    return

def disconnect_wifi():
    wifi.radio.enabled = False
    return

def report_status(voltage, water_detected):
    connect_wifi()
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    report = f"Battery voltage is {voltage}v. {water_detected if 'Water detected.' else 'No water detected.'}"
    print(report)
    try:
        response = requests.post("http://michaelwmac:3030/", data=report)
        print(response.text)
        response.close()
    except RuntimeError as e:
        print(e)
    disconnect_wifi()

def deep_sleep(t):
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + t)
    pin_alarm = alarm.pin.PinAlarm(pin=board.IO0, value=False, pull=True)
    alarm.exit_and_deep_sleep_until_alarms(time_alarm, pin_alarm)
    return
# returns [battery_is_low, battery_voltage]
def check_battery():
    voltage = tinys3.get_battery_voltage()
    s = f"{voltage},{time.monotonic()}\n"
    print(s)
    try:
        with open("/batterylog.txt", "a") as fp:
            fp.write(s)

    except OSError as e:
        print(e)
    return voltage

# returns True if water detected
def check_water_sensor():
    return random.random() < 0.5


def main_loop():
    print("I'm Alive")
    report_status(0, False)
    while True:
        voltage = check_battery()
        water_detected = check_water_sensor()

        if voltage < 2.9 or water_detected:
            report_status(voltage, water_detected);

        print("Going to sleep")
        # deep_sleep(1)
        time.sleep(1)


