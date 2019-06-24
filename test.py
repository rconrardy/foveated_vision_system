import fvs

# Create a new system
myfvs = fvs.System()

# Set up the device at camera index 0 with 4 types of visions
myfvs["Capture Device 0"] = fvs.Device(0)
print(myfvs["Capture Device 0"])
myfvs["Capture Device 0"]["peripheral 0"] = fvs.Vision(4/6, 64)
myfvs["Capture Device 0"]["perifoveal 0"] = fvs.Vision(3/6, 64)
myfvs["Capture Device 0"]["parafoveal 0"] = fvs.Vision(2/6, 64)
myfvs["Capture Device 0"]["mainfoveal 0"] = fvs.Vision(1/6, 64)

# Set up the device at camera index 1 with 4 types of visions
myfvs["Capture Device 1"] = fvs.Device(1)
myfvs["Capture Device 1"]["peripheral 1"] = fvs.Vision(4/5, 64)
myfvs["Capture Device 1"]["perifoveal 1"] = fvs.Vision(3/5, 64)
myfvs["Capture Device 1"]["parafoveal 1"] = fvs.Vision(2/5, 64)
myfvs["Capture Device 1"]["mainfoveal 1"] = fvs.Vision(1/5, 64)

# Create a new application and start it
myapp = fvs.Application(myfvs)
myapp.mainloop()
