import random as rd

class Particle:
    def __init__(self, coral, z_max):
        x_max = coral.getXmax()
        y_max = coral.getYmax()

        # self.x1 = rd.randrange(x_max-10, x_max+10)
        # self.y1 = rd.randrange(y_max-10, y_max+10)

        self.x1 = rd.randrange(0, 100)
        self.y1 = rd.randrange(0, 100)

        # if (coral.getZmax() + 10 < z_max):
        #     self.z1 = coral.getZmax() + 10
        # else: 
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
        