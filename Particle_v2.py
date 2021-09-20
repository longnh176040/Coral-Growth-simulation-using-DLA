import random as rd

class Particle:
    def __init__(self, z_max):
        self.x1 = rd.randrange(0, z_max)
        self.y1 = rd.randrange(0, z_max)
        self.z1 = z_max

        self.x2 = self.x1
        self.y2 = self.y1
        self.z2 = self.z1       

    def getCurPosition(self):
        return (self.x1, self.y1, self.z1)

    def getNextPosition(self):
        return (self.x2, self.y2, self.z2)

    def move(self): 
        self.z2 = self.z1 - 1

        tmp2 = rd.random()
        if tmp2 > 0.8:   
            self.x2 = self.x1 + 1
        elif tmp2 > 0.6: 
            self.x2 = self.x1 - 1
        elif tmp2 > 0.4: 
            self.y2 = self.y1 + 1
        elif tmp2 > 0.2: 
            self.y2 = self.y1 - 1
        