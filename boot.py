import storage
import tinys3
import puck_logging

print("boot.py running")

log = puck_logging.getLogger()

if tinys3.get_vbus_present() == False:
    log.info("running on battery, mounting filesystem for read/write")
    storage.remount("/", False)
else:
    log.info("running on USB power, mounting filesystem for read only")
    storage.remount("/", True)

log.info("boot finished")
