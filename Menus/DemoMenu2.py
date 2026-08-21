import sys
classPath = __file__.split("Menus")[0]
sys.path.append(classPath + "Menus\\framework")
from Menu import menu

class demoMenu2(menu):
    variable = "different thing"

    def assignIconFunctions(self):
        self.icons["button 1"].bindFunction(lambda : self.main.changeMenu(0))

    def initialise(self):
        print("DemoMenu2 initialised")

    def doThing(self):
        print("Doing thing differently!")
