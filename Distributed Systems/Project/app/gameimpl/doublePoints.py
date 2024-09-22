MULTIPLIER = 2

class doubleMatch():
    def __init__(self):
        self.multiplier = MULTIPLIER

    def getMultiplier(self):
        return self.multiplier

class DoubleGameBuilder():
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return doubleMatch()
