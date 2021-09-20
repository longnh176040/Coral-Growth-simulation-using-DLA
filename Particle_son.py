import random as rd

class Particle:
    def __init__(self, x_max,y_max,z_max, env):
        self.x1 = rd.randrange(0+1, x_max-1)
        self.y1 = rd.randrange(0+1, y_max-1)
        self.z1 = rd.randrange(0+1, z_max-1)

        while env[self.x1][self.y1][self.z1] == 1:
            self.x1 = rd.randrange(0+1, x_max-1)
            self.y1 = rd.randrange(0+1, y_max-1)
            self.z1 = rd.randrange(0+1, z_max-1)

        self.x2 = self.x1
        self.y2 = self.y1
        self.z2 = self.z1

        self.status=False   

    def resetParticle(self,x_max,y_max, z_max, env):
        self.x1 = rd.randrange(1, x_max-1)
        self.y1 = rd.randrange(1, y_max-1)
        self.z1 = rd.randrange(1, z_max-1)

        while env[self.x1][self.y1][self.z1] == 1:
            self.x1 = rd.randrange(0, x_max)
            self.y1 = rd.randrange(0, y_max)
            self.z1 = rd.randrange(0, z_max)

        self.x2 = self.x1
        self.y2 = self.y1
        self.z2 = self.z1   

    def getCurPosition(self):
        return (self.x1, self.y1, self.z1)

    def getNextPosition(self):
        return (self.x2, self.y2, self.z2)

    def move(self, dist): 
        tmp = rd.random()
        if tmp <= 0.3:   
            self.x2 = self.x1 + dist
        elif tmp > 0.3 and tmp <= 0.6: 
            self.x2 = self.x1 - dist

        tmp = rd.random()
        if tmp <= 0.3:   
            self.y2 = self.y1 + dist
        elif tmp > 0.3 and tmp <= 0.6: 
            self.y2 = self.y1 - dist

        tmp = rd.random()
        if tmp <= 0.3:   
            self.z2 = self.z1 + dist   
        elif tmp > 0.3 and tmp <= 0.6: 
            self.z2 = self.z1 - dist     

        # tmp = rd.random()
        # if tmp <= 0.5:   
        #    self.z2 = self.z1 - dist

    def setBound(self, env, dist,x_max,y_max, z_max):
        if self.x1-dist < 0: x_start = 0
        else: x_start = self.x1-dist 
        if self.x1+dist > x_max: x_end = x_max
        else: x_end = self.x1+dist    

        if self.y1-dist < 0: y_start = 0
        else: y_start = self.y1-dist 
        if self.y1+dist > y_max: y_end = y_max
        else: y_end = self.y1+dist 

        if self.z1-dist < 0: z_start = 0
        else: z_start = self.z1-dist 
        if self.z1+dist > z_max: z_end = z_max
        else: z_end = self.z1+dist 

        for i in range (x_start, x_end):
            for j in range (y_start, y_end):
                for k in range (z_start, z_end):
                    env[i][j][k] = 1
        
        return env