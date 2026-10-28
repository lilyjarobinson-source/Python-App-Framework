from tkinter import *
from IconFileParser import iconFileParser
from Keylogger import keylogger
import threading
from time import time
class main:
    hexDigits = "0123456789abcdef"
    
    def __init__(self, title, geometry):
        self.title = title
        self.geometry = geometry
        self.menus = {}
        self.currentMenuKey = 0
        self.currentMenu = None
        self.menuWasRunning = False
        self.root = None
        self.theme = {}
        self.lookForIconFile = True
        self.iconFileParser = iconFileParser()
        self.keylogger = keylogger()
        self.runableMenuThread = None
        self.isFullscreen = False

    def initialise(self):
        if self.lookForIconFile:
            self.iconFileParser.assignIconsToMenus(self.menus)
        self.root = Tk()
        self.root.title(self.title)
        self.root.geometry(self.geometry)
        
        if self.isFullscreen:
            self.root.state("zoomed")
                
        self.root.update()
        self.screenWidth = self.root.winfo_width()
        self.screenHeight = self.root.winfo_height()
        self.screenX = self.root.winfo_x()
        self.screenY = self.root.winfo_y()

        self.root.bind("<KeyPress>", self.keylogger.onKeyEvent)
        self.root.bind("<KeyRelease>", self.keylogger.onKeyEvent)

    def ignoreIconFile(self, look=False):
        self.lookForIconFile = look

    def assignIconFileLocation(self, location):
        self.iconFileParser.assignIconFileLocaion(location)

    def addMenus(self, menus):
        if isinstance(menus, dict):
            for i in menus:
                self.menus.update({i : menus[i]})
        elif isinstance(menus, list):
            for i in menus:
                self.menus.update({i.name : i})
        else:
            self.menus.update({menus.name : menus})

    def activate(self, startingMenuKey):
        self.initialise()
        self.loadTheme()
        self.currentMenuKey = startingMenuKey
        self.currentMenu = self.menus[self.currentMenuKey]
        self.currentMenu.activate(self, self.theme)
        self.startMenuRunning()
        self.root.mainloop()

    def startMenuRunning(self):
        if self.currentMenu.runable:
            self.runableMenuThread = threading.Thread(target=self.currentMenu.startRunning)
            self.runableMenuThread.start()

    def stopMenuRunning(self):
        if self.currentMenu.runable:
            self.currentMenu.stopRunning()

    def reloadMenu(self):
        self.loadTheme()
        self.stopMenuRunning()
        self.currentMenu.deactivate()
        self.currentMenu.activate(self, self.theme)
        self.startMenuRunning()

    def changeMenu(self, targetMenu):
        self.loadTheme()
        self.stopMenuRunning()
        self.currentMenu.deactivate()
        self.currentMenuKey = targetMenu
        self.currentMenu = self.menus[targetMenu]
        self.currentMenu.activate(self, self.theme)
        self.startMenuRunning()

    def loadTheme(self):
        try:
            file = open("SELECTEDTHEMELOCATION", "r")
            theme = file.read()
            file.close()
            
            file = open("THEMELOCATION", "r")
            content = file.read()
            file.close()
            
            self.theme = {
                "name" : "",
                "bg" : "",
                "buttonBg" : "",
                "buttonTx" : "",
                "labelBg" : "",
                "labelTx" : "",
                "entryBg" : "",
                "entryTx" : "",
                "optionBoxBg" : "",
                "optionBoxTx" : "",
                "listBoxBg" : "",
                "listBoxTx" : "",
                "canvasBg" : "",
                "canvasTx" : "",
            }
            
            content = content.split("\n")
            keys = list(self.theme.keys())
            for i in range(len(content)):
                self.theme[keys[i]] = content[i]
        except:
            self.theme = {
                "name" : "default",
                "bg" : "SystemButtonFace",
                "buttonBg" : "#e0e0e0",
                "buttonTx" : "#000000",
                "labelBg" : "SystemButtonFace",
                "labelTx" : "#000000",
                "entryBg" : "#ffffff",
                "entryTx" : "#000000",
                "optionBoxBg" : "SystemButtonFace",
                "optionBoxTx" : "#000000",
                "listBoxBg" : "#ffffff",
                "listBoxTx" : "#000000",
                "canvasBg" : "#ffffff",
                "canvasTx" : "#000000",
            }
        self.changeBgColour(self.theme["bg"])

    def changeBgColour(self, colour):
        notHex = False
        for i in colour:
            if i.lower() not in self.hexDigits:
                notHex = True
                break
        if not notHex:
            colour = "#" + colour
        self.root.config(bg=colour)

    def fullscreen(self, fullscreen=True):
        self.isFullscreen = fullscreen
        if self.root != None:
            if self.isFullscreen:
                self.root.state("zoomed")

        
    
