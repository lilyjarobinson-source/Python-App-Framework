class keylogger:
    def __init__(self):
        self.pressedKeys = []

    def isKeyPressed(self, key):
        return key in self.pressedKeys

    def onKeyEvent(self, event):
        character = event.char.lower()
        if event.type == "2":
            if not self.isKeyPressed(character):
                self.pressedKeys.append(character)
        elif event.type == "3":
            if self.isKeyPressed(character):
                self.pressedKeys.remove(character)
