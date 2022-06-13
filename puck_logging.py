import adafruit_logging as logging
import tinys3

log = logging.getLogger("puck")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

if tinys3.get_vbus_present() == False:
    storage.remount("/", False)
    log.addHandler(logging.FileHandler("puck.log"))

def getLogger(log_name = "puck"):
    return logging.getLogger(log_name)

