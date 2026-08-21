import random, time
from tkinter import *
hexDigits = "0123456789abcdef"


class menu:
    def __init__(self):
        self.icons = {}
        self.theme = {}
        self.runable = False
        self.running = False
        self.main = None
        self.root = None
        self.name = self.__class__.__name__

    # Ran to set up the menu
    def activate(self, main, theme):
        self.main = main
        self.root = main.root
        self.theme = theme
        for i in self.icons.values():
            i.activate(self.root, theme)
        self.assignIconFunctions()
        self.initialise()

    def assignIcons(self, icons):
        self.icons = {}
        for i in icons.keys():
            self.icons.update({i : icons[i]})

    def addIcons(self, icons):
        for i in icons.keys():
            self.icons.update({i : icons[i]})

    # Ran to teardown the menu
    def deactivate(self):
        self.running = False
        for i in self.icons.values():
            i.deactivate()
        self.unitialise()

    def assignIconFunctions(self):
        pass

    # custom code for startup goes here
    def initialise(self):
        pass

    # custom code for teardown goes here
    def unitialise(self):
        pass

    # code for reloading data goes here
    def reload(self):
        pass

    def setRunable(self, runable=True):
        self.runable = runable

    def run(self):
        self.update()

    def updateScreen(self):
        self.root.update()

    def startRunning(self):
        if self.runable:
            self.running = True
            self.runInitialisation()
            while self.running:
                self.run()

    def stopRunning(self):
        if self.runable:
            self.running = False
            self.runDeinitialisation()

    # custom code for starting running goes here
    def runInitialisation(self):
        pass
    
    # custom code for ending running goes here
    def runDeinitialisation(self):
        pass
    
    # code for updating the menu goes here
    def update(self):
        pass
    

class obj:
    def __init__(self, pos, dimensions):
        self.pos = pos
        self.obj = None
        self.dimensions = dimensions
        self.active = False
        self.isMenuActiveFunction = None
        self.name = self.__class__.__name__

    def activate(self, root, theme):
        if not self.active:
            self.setColour(theme)
            self.initialise(root)
            self.active = True
        
    def deactivate(self):
        if self.active:
            self.active = False
            self.obj.destroy()

    def initialise(self, root):
        pass

    def place(self, pos=None, dimensions=None):
        if pos != None:
            self.pos = pos.copy()
        if dimensions != None:
            self.dimensions = dimensions.copy()
        self.obj.place(x=self.pos[0], y=self.pos[1], width=self.dimensions[0], height=self.dimensions[1])

    def raiseObj(self):
        self.obj.tkraise()

    def setColour(self, theme):
        colour = theme[self.name + "Bg"]
        notHex = False
        for i in colour:
            if i.lower() not in hexDigits:
                notHex = True
                break
        if not notHex:
            colour = "#" + colour
        self.colour = colour
        
        colour = theme[self.name + "Tx"]
        notHex = False
        for i in colour:
            if i.lower() not in hexDigits:
                notHex = True
                break
        if not notHex:
            colour = "#" + colour
        self.textColour = colour

    def updateBgColour(self, colour):
        self.obj.config(bg=colour)
        
    def updateTxColour(self, colour):
        self.obj.config(fg=colour)
        

class button(obj):
    colour = "#e0e0e0"
    textColour = "#000000"
    def __init__(self, pos, dimensions, text):
        super().__init__(pos, dimensions)
        self.text = str(text)[:]
        self.fun = None

    def initialise(self, root):
        self.obj = Button(root, text=self.text, command=self.checkToRunFunction, borderwidth=1, relief="solid", bg=self.colour, fg=self.textColour)
        self.place()

    def bindFunction(self, fun):
        self.fun = fun

    def checkToRunFunction(self):
        if self.fun != None:
            self.fun()

    def set(self, text):
        self.text = str(text)[:]
        self.obj.config(text=text)

    def get(self):
        return self.text

    def clear(self):
        self.text = ""

class label(obj):
    name = "label"
    colour = "SystemButtonFace"
    textColour = "#000000"
    def __init__(self, pos, dimensions, text, textAlign="c"):
        super().__init__(pos, dimensions)
        self.text = str(text)[:]
        self.textAlign = textAlign
        match textAlign:
            case "w":
                self.textJustify = "left"
            case "e":
                self.textJustify = "right"
            case _:
                self.textJustify = "center"   

    def initialise(self, root):
        self.obj = Label(root, text=self.text, borderwidth=1, relief="solid", bg=self.colour, fg=self.textColour, anchor=self.textAlign, justify=self.textJustify)
        self.place()
        
    def set(self, text):
        self.text = str(text)[:]
        self.obj.config(text=self.text)

    def get(self):
        return self.text

    def clear(self):
        self.text = ""
        self.obj.config(text=self.text)

class entry(obj):
    colour = "#000000"
    textColour = "#000000"
    def __init__(self, pos, dimensions):
        super().__init__(pos, dimensions)
        self.fun = None
        self.contents = None
        self.suppressChanges = False

    def initialise(self, root):
        self.suppressChanges = True
        if self.contents == None:
            self.contents = StringVar()
        self.obj = Entry(root, textvariable=self.contents, borderwidth=1, relief="solid", bg=self.colour, fg=self.textColour)
        self.obj.bind("<KeyRelease>", lambda *args : self.checkToRunFunction())
        self.place()
        self.suppressChanges = False

    def get(self):
        return self.contents.get()

    def set(self, contents):
        self.suppressChanges = True
        self.contents.set(str(contents)[:])
        self.obj.config(textvariable=self.contents)
        self.suppressChanges = False

    def clear(self):
        self.suppressChanges = True
        self.contents.set("")
        self.obj.config(textvariable=self.contents)
        self.suppressChanges = False

    def bindFunctionToKeypress(self, fun):
        self.fun = fun

    def checkToRunFunction(self):
        if not self.suppressChanges:
            if self.fun != None:
                self.fun()

class optionBox(obj):
    colour = "SystemButtonFace"
    textColour = "#000000"
    def __init__(self, pos, dimensions, defaultOption, options):
        super().__init__(pos, dimensions)
        self.defaultOption = defaultOption
        self.selectedOption = None
        self.fun = None
        self.options = options
        self.suppressChanges = False
    
    def initialise(self, root):
        self.suppressChanges = True
        if self.selectedOption == None:
            self.selectedOption = StringVar(value=self.defaultOption)
        else:
            self.setSelectedOption(self.defaultOption)
        self.obj = OptionMenu(root, self.selectedOption, *self.options)
        self.obj.config(bg=self.colour, borderwidth=1, relief="solid", highlightthickness=0, fg=self.textColour)
        self.selectedOption.trace_add("write", lambda *args : self.checkToRunFunction())
        self.place()
        self.suppressChanges = False

    def get(self):
        return self.selectedOption.get()

    def setSelectedOption(self, option):
        self.suppressChanges = True
        self.selectedOption.set(str(option)[:])
        self.suppressChanges = False

    def setOptions(self, root, theme, options):
        self.options = options
        self.deactivate()
        self.activate(root, theme, self.checkToRunFunction)

    def bindFunctionToKeypress(self, fun):
        self.fun = fun

    def checkToRunFunction(self):
        if not self.suppressChanges:
            if self.fun != None:
                self.fun()

class listBox(obj):
    colour = "#000000"
    textColour = "#000000"
    def __init__(self, pos, dimensions):
        super().__init__(pos, dimensions)
        self.items = []
        self.fun = None
        self.suppressChanges = False

    def initialise(self, root):
        self.suppressChanges = True
        self.obj = Listbox(root, borderwidth=1, relief="solid", bg=self.colour, highlightthickness=0, fg=self.textColour)
        self.clear()
        self.obj.bind("<<ListboxSelect>>", lambda *args : self.checkToRunFunction())
        self.place()
        self.suppressChanges = False

    def bindFunctionToChange(self, fun):
        self.fun = fun

    def checkToRunFunction(self):
        if not self.suppressChanges:
            if self.fun != None:
                self.fun()

    def getIndex(self):
        return self.obj.curselection()

    def getValue(self):
        index = self.obj.curselection()
        if len(index) > 0:
            index = index[0]
            return self.items[index]

    def getItems(self):
        return self.items.copy()

    def insert(self, index, item):
        self.items.insert(index, item)
        self.obj.insert(index, item)

    def append(self, item):
        self.items.append(item)
        self.obj.insert(len(self.items)-1, item)

    def delete(self, index):
        self.items.pop(index)
        self.obj.delete(index)

    def clear(self):
        self.items = []
        self.obj.delete(0, END)

    def getItemAtIndex(self, index):
        return self.items[index]

class canvas(obj):
    name = "canvas"
    colour = "#ffffff"
    textColour = "#000000"
    def __init__(self, pos, dimensions):
        super().__init__(pos, dimensions)
        self.suppressChanges = False
        self.boundFunctions = {}
    
    def initialise(self, root):
        self.suppressChanges = True
        self.obj = Canvas(root, borderwidth=1, relief="solid", bg=self.colour, highlightthickness=0)
        self.place()
        self.suppressChanges = False

    def dot(self, x, y, colour="black"):
        self.obj.create_oval(x-3, y-3, x+3, y+3, fill=colour, outline=colour)

    def circle(self, x, y, radius, colour="black"):
        self.obj.create_oval(x-radius, y-radius, x+radius, y+radius, fill=colour, outline=colour)

    def line(self, x1, y1, x2, y2, arrow="none", colour="black"):
        self.obj.create_line(x1, y1, x2, y2, arrow=arrow, fill=colour)

    def image(self, x, y, image, anchor="center"):
        self.obj.create_image(x, y, image=image, anchor=anchor)
        
    def write(self, x, y, text, anchor="center", font="TkDefaultFont"):
        self.obj.create_text(x, y, text=text, fill=self.textColour, anchor=anchor, font=font)

    def clear(self):
        self.obj.delete("all")

    def bindFuncitonToMouseEvent(self, event, fun):
        self.bindFunction(event, fun)
        self.obj.bind(event, lambda *args : self.checkForFunction(event))

    def bindFunction(self, event, fun):
        self.boundFunctions.update({event : fun})

    def checkForFunction(self, event):
        if not self.suppressChanges and event in self.boundFunctions:
            if self.boundFunctions[event] != None:
                self.boundFunctions[event]()


class image(obj):
    colour = "SystemButtonFace"
    textColour = "#000000"
    def __init__(self, pos, dimensions, image=None):
        super().__init__(pos, dimensions)
        self.image = image
        self.name = "label"
                
    def initialise(self, root):
        if self.image == None:
            self.obj = Label(root, text="image", borderwidth=1, relief="solid", bg=self.colour, fg=self.textColour)
        else:
            self.obj = Label(root, image=self.image, borderwidth=1, relief="solid")
        self.place()
        
    def set(self, image):
        if self.image == None:
            self.obj.config(text="")
        self.image = image
        self.obj.config(image=self.image)
