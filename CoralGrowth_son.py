from mpl_toolkits.mplot3d.axes3d import get_test_data
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import random as rd
from Particle_son import Particle
import time

x_min = 0
y_min = 0
z_min = 0
x_max = 30
y_max = 50
z_max = 100

particles = 5000

dist = 1

#Initialize environment
env = np.zeros((x_max, y_max, z_max))
 
d_env= np.zeros((x_max, y_max, z_max))

#Initialize root
x = []                  #list for append point for drawing
y = []
z = []
particles_list = []  
treeOnly_list=[]   
    #list of particles' status: appended or not

for i in range(10):
    p = Particle(x_max,y_max,z_max, d_env)

    #p.x1=int(x_max/2)
    #p.y1=int(y_max/2)
    #p.z1=int(z_max/2)

    #p.x1=rd.randrange(int(x_max/5),int(x_max*4/5))
    #p.y1=rd.randrange(int(y_max/5),int(y_max*4/5))
    p.z1=1

    p.x2=p.x1
    p.y2=p.y1
    p.z2=p.z1
    p.status=True

    particles_list.append(p)
    treeOnly_list.append(p)
    env[p.x1][p.y1][p.z1] = 1

    d_env=p.setBound(d_env,dist,x_max,y_max,z_max)
#print ("hey\n")

def addPoint():
    p = Particle(x_max,y_max,z_max, d_env)
    particles_list.append(p)

for i in range(3, particles):
    addPoint()

def check_status(point):    #point = x2, y2, z2
    collision = False
    outLimit = False

    pos = point.getNextPosition()
    pos2 = point.getCurPosition()

    if pos[0] < 0 or pos[0] > x_max-1 or pos[1] < 0 or pos[1] > y_max-1 or pos[2] < 0 or pos[2] > z_max-1:
        outLimit = True        
    elif env[pos[0]][pos[1]][pos[2]] == 1:
        print(" x1 " + str(pos2[0]) + " y1 " + str(pos2[1]) + " z1 " + str(pos2[2]))
        collision = True
    return [outLimit, collision, pos]

def forestGrowth():
    global d_env
    for p in particles_list:
        i = p.status
        
        if i == False:
            p.move(1)
            status = check_status(p)
            if (status[0] == True):
                p.resetParticle(x_max,y_max,z_max, d_env)

            elif (status[1] == True ):
                p.status = True

                pos = p.getCurPosition()
                env[pos[0]][pos[1]][pos[2]] = 1
                
                treeOnly_list.append(p)
                d_env=p.setBound(d_env, dist,x_max,y_max, z_max)
                
                global particles
                particles -= 1
                
            else:
                pos = status[2]
                p.x1 = pos[0]
                p.y1 = pos[1]
                p.z1 = pos[2]
        else: continue

        
        
def update_points():
    forestGrowth()
    #draw()
    drawTreeOnly()
    graph._offsets3d = (x, y, z)
    return graph

def draw():
    global x,y,z
    x = []                  #list for append point for drawing
    y = []
    z = []
    for a in particles_list:
        
        x.append(a.x1)
        y.append(a.y1)
        z.append(a.z1)

def drawTreeOnly():
    global x,y,z
    x = []                  #list for append point for drawing
    y = []
    z = []
    for a in treeOnly_list:
        
        x.append(a.x1)
        y.append(a.y1)
        z.append(a.z1)

fig = plt.figure(figsize=(5, 5))

ax = fig.add_subplot(111, projection="3d")
graph = ax.scatter(x, y, z, s = 5, color='c') #, edgecolor='black', linewidth=3, hatch='|'

ax.set_xlim3d(x_min, x_max)
ax.set_ylim3d(y_min, y_max)
ax.set_zlim3d(z_min, z_max)

# some number > 1 that stretches z axis as you desire
ax.set_box_aspect((x_max, y_max, z_max))  # xy aspect ratio is 1:1, but stretches z axis

while particles > 0:
    update_points()
    plt.pause(0.0001)
    
plt.show()