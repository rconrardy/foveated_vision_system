import tkinter
import fvs
import utils

myfvs = fvs.FoveatedVisionSystem()


myfvs[0] = fvs.Device(0)
myfvs[0]["peripheral"] = fvs.Vision(4/4, 32)
myfvs[0]["perifoveal"] = fvs.Vision(3/4, 32)
myfvs[0]["parafoveal"] = fvs.Vision(2/4, 32)
myfvs[0]["mainfoveal"] = fvs.Vision(1/4, 32)




myapp = fvs.Application(myfvs)

myapp.update()
myapp.mainloop()


#
# print(myfvs)
# print(myfvs[0])
# print(myfvs[0]["mainfoveal"])
