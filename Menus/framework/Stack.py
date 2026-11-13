class stack:
    def __init__(self):
        self.array = []

    def push(self, item):
        self.array.append(item)

    def peak(self):
        return self.array[-1]

    def pop(self):
        if self.isEmpty():
            return None
        return self.array.pop()

    def isEmpty(self):
        return len(self.array) == 0

    def length(self):
        return len(self.array)

    def clear(self):
        self.array = []
