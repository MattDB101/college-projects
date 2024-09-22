MULTIPLIER = 1

class standardMatch():
    def __init__(self):
        self.multiplier = MULTIPLIER

    def getMultiplier(self):
        return self.multiplier

class StandardGameBuilder():
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return standardMatch()
