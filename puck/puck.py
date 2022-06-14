import tinys3
import time
import alarm
import board
import analogio
import digitalio
import puck_logging
import puck_network

water_enable = digitalio.DigitalInOut(board.A0)
water_enable.switch_to_output()
water_sensor = analogio.AnalogIn(board.A1)

voltage = None
water_level = None

log = puck_logging.getLogger()

def setup():
    log.info("setup")

    puck_network.connect_wifi()

    puck_network.post("http://michaelwmac:3030", "setup")


def main_loop():
    while True:
        voltage = get_battery_voltage()
        water_level = get_water_level()

        report = f"voltage = {voltage}, water level = {water_level}"

        log.info(report)

        if voltage < 2.9 or water_level > 10000:
            try:
                puck_network.connect_wifi()
                puck_network.post("http://michaelwmac:3030/", report)
            except RuntimeError as e:
                puck_network.disconnect_wifi()
                log.error(e)

        time.sleep(2)


def deep_sleep(t):
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + t)
    pin_alarm = alarm.pin.PinAlarm(pin=board.IO0, value=False, pull=True)
    alarm.exit_and_deep_sleep_until_alarms(time_alarm, pin_alarm)
    return

# returns [battery_is_low, battery_voltage]
def get_battery_voltage():
    return tinys3.get_battery_voltage()

def get_water_level():
    total = 0
    count = 5
    water_enable.value = True
    for count in range(1, count):
        total = total + water_sensor.value
        time.sleep(0.01)

    water_enable.value = False

    return total / count

