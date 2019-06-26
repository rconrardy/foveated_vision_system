import fvs

# Create a new system
myfvs = fvs.System()

# Set up the device at camera index 0 with 4 types of visions
myfvs["Capture Device 0"] = fvs.Device(0)
print(myfvs["Capture Device 0"])
myfvs["Capture Device 0"]["4"] = fvs.Vision(1/16, 64)
myfvs["Capture Device 0"]["3"] = fvs.Vision(1/8, 64)
myfvs["Capture Device 0"]["2"] = fvs.Vision(1/4, 64)
myfvs["Capture Device 0"]["1"] = fvs.Vision(1/2, 64)

# Set up the device at camera index 1 with 4 types of visions
myfvs["Capture Device 1"] = fvs.Device(1)
myfvs["Capture Device 1"]["3"] = fvs.Vision(3/3, 64)
myfvs["Capture Device 1"]["2"] = fvs.Vision(2/3, 64)
myfvs["Capture Device 1"]["1"] = fvs.Vision(1/3, 64)

# Create a new application and start it
myapp = fvs.Application(myfvs)
myapp.mainloop()
