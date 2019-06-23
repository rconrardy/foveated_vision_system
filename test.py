import fvs

myfvs = fvs.System()

myfvs["Capture Device 0"] = fvs.Device(0)
myfvs["Capture Device 0"]["peripheral 0"] = fvs.Vision(4/6, 32)
myfvs["Capture Device 0"]["perifoveal 0"] = fvs.Vision(3/6, 32)
myfvs["Capture Device 0"]["parafoveal 0"] = fvs.Vision(2/6, 32)
myfvs["Capture Device 0"]["mainfoveal 0"] = fvs.Vision(1/6, 32)

myfvs["Capture Device 1"] = fvs.Device(1)
myfvs["Capture Device 1"]["peripheral 1"] = fvs.Vision(4/6, 32)
myfvs["Capture Device 1"]["perifoveal 1"] = fvs.Vision(3/6, 32)
myfvs["Capture Device 1"]["parafoveal 1"] = fvs.Vision(2/6, 32)
myfvs["Capture Device 1"]["mainfoveal 1"] = fvs.Vision(1/6, 32)

myapp = fvs.Application(myfvs)

myapp.update()
myapp.mainloop()
