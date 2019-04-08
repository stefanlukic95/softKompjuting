class TrackableObject:
    def __init__(self, objectId, x, y, vreme, kraj):
        self.x = x
        self.y = y
        self.objectId = objectId
        self.vreme = vreme
        self.kraj = kraj

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    # how long is the object in the video
    def getVreme(self):
        return self.vreme

    def setVreme(self):
        self.vreme += 1

        # how long since the object is not in the video

    def getKraj(self):
        return self.kraj

    def setKraj(self):
        self.kraj += 1

    def updateCoords(self, xn, yn):
        self.x = xn
        self.y = yn