from Menu import button, label, entry, optionBox, listBox, canvas, image
class iconFileParser:
    def __init__(self):
        self.fileLocation = ""
        self.iconStore = {}
        self.menus = []

    def assignIconFileLocaion(self, location):
        self.fileLocation = location

    def assignIconsToMenus(self, menus):
        self.parseFile()
        for i in self.iconStore:
            for x in i.split(","):
                menuReference = None
                for m in menus:
                    if m.name == x:
                        menuReference = m
                if menuReference == None:
                    print(f"{i} is not an assigned menu!")
                else:
                    menuReference.addIcons(self.iconStore[i])
        self.iconStore = None

    def parseFile(self):
        try:
            file = open(self.fileLocation + "/Icon file.txt", "r")
            contents = file.read()
        except:
            print("No icon file path supplied!")
            return None
        finally:
            file.close()
        contents = contents.split("\n")
        for i in contents:
            self.parseLine(i)

    def parseLine(self, line):
        if len(line) > 0:
            if line.startswith("M:"):
                self.currentMenu = line[2:]
                self.iconStore.update({self.currentMenu : {}})
            else:
                self.parseIcon(line)

    def parseIcon(self, line):
        for i in range(len(line)-1):
            if line[i] + line[i+1] == "::":
                break
        colonPosition = i
        
        if colonPosition == len(line):
            print(f"Issue with line:\n{line}\nNo double colon present!")
        elif colonPosition == len(line)-1:
            print(f"Issue with line:\n{line}\nNo icon data present!")
        elif colonPosition == 0:
            print(f"Issue with line:\n{line}\nNo icon name present!")
        
        name, data = line.split("::")
        data = data.split(",,")
        try:
            match data[0]:
                case "label":
                    icon = label([int(data[1]), int(data[2])], [int(data[3]), int(data[4])], data[5])
                case "button":
                    icon = button([int(data[1]), int(data[2])], [int(data[3]), int(data[4])], data[5])
                case "optionBox":
                    icon = optionBox([int(data[1]), int(data[2])], [int(data[3]), int(data[4])], data[5], data[6:])
                case "entry":
                    icon = entry([int(data[1]), int(data[2])], [int(data[3]), int(data[4])])
                case "listBox":
                    icon = listBox([int(data[1]), int(data[2])], [int(data[3]), int(data[4])])
                case "canvas":
                    icon = canvas([int(data[1]), int(data[2])], [int(data[3]), int(data[4])])
                case "image":
                    icon = image([int(data[1]), int(data[2])], [int(data[3]), int(data[4])])
        except:
            print(line)
            print(data)
        self.iconStore[self.currentMenu].update({name : icon})

