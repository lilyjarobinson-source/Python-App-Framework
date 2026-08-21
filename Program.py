import sys
classPath = __file__.split(__file__.split("\\")[-1])[0]
sys.path.append(classPath + "Menus\\framework")
sys.path.append(classPath + "Menus")
from Main import main
from DemoMenu1 import demoMenu1
from DemoMenu2 import demoMenu2

main = main("test", "800x500")
main.fullscreen()

demoMenu1 = demoMenu1()
demoMenu2 = demoMenu2()

demoMenu1.setRunable()

#'''
main.assignMenus([demoMenu1, demoMenu2])
main.assignIconFileLocation(classPath + "Menus")
main.activate()
main.root.mainloop()
#'''
