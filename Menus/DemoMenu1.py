import sys
classPath = __file__.split("Menus")[0]
sys.path.append(classPath + "Menus\\framework")
from Menu import menu

class demoMenu1(menu):
    variable = "thing"

    def assignIconFunctions(self):
        self.icons["button 1"].bindFunction(lambda : self.main.changeMenu(1))

    def initialise(self):
        print("DemoMenu1 initialised")

    def doThing(self):
        print("Doing thing!")

    def update(self):
        #self.icons["label 3"].set(self.main.keylogger.pressedKeys)
        self.icons["label 3"].set(self.main.root.winfo_pointerx())
        self.updateScreen()
