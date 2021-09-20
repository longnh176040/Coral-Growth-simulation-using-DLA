class Coral:
    def __init__(self, seed):
        self.tree = [(seed[0], seed[1], seed[2])]
        self.Xmax =  seed[0]
        self.Ymax =  seed[1]
        self.Zmax =  seed[2]

    def getXmax(self):
        return self.Xmax

    def getYmax(self):
        return self.Ymax

    def getZmax(self):
        return self.Zmax    

    def extend(self, particle):
        self.tree.append(particle)
        #find max
        if self.Xmax < particle[0]:
            self.Xmax = particle[0]
        if self.Ymax < particle[1]:
            self.Ymax = particle[1]   
        if self.Zmax < particle[2]:
            self.Zmax = particle[2]         