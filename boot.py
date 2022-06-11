import storage
import tinys3

print("boot.py running")

if tinys3.get_vbus_present() == False:
    storage.remount("/", False)

    with open("/bootlog.txt", "a") as fp:
        fp.write(f"vbus {tinys3.get_vbus_present()}\n")
