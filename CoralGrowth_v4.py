from mpl_toolkits.mplot3d.axes3d import get_test_data
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import random as rd
import pprint
from Particle_v3 import Particle
import time

x_min = 0
y_min = 0
z_min = 0
x_max = 30
y_max = 30
z_max = 60

particles = 5000

seed = 10
dist = 1
speed = 1

#Initialize environment
env = np.zeros((x_max, y_max, z_max))
d_env = np.zeros((x_max, y_max, z_max))

#Initialize root
x = []                  #list for append point for drawing
y = []
z = []
particles_list = []     

for i in range(seed):
    p = Particle(x_max, y_max, z_max, d_env, True)
    x.append(p.x1)
    y.append(p.y1)
    z.append(p.z1)
    env[x[i]][y[i]][z[i]] = 1
    particles_list.append(p)

    for h in range(x[i]-dist, x[i]+dist):
        for j in range(y[i]-dist, y[i]+dist):
            for k in range(z[i]-dist, z[i]+dist):
                d_env[h][j][k] = 1

for i in range(1, particles):
    p = Particle(x_max, y_max, z_max, d_env, False)
    particles_list.append(p)

    x.append(p.x1)
    y.append(p.y1)
    z.append(p.z1)

def check_status(point):    
    collision = False
    outLimit = False

    pos = point.getNextPosition()

    if pos[0] < 0 or pos[0] > x_max-1 or pos[1] < 0 or pos[1] > y_max-1 or pos[2] < 0 or pos[2] > z_max-1:
        outLimit = True        
    elif env[pos[0]][pos[1]][pos[2]] == 1:
        print(" x2 " + str(pos[0]) + " y2 " + str(pos[1]) + " z2 " + str(pos[2]))
        collision = True
    return [outLimit, collision, pos]

def forestGrowth():
    for p in range (seed, len(particles_list), 1):
        if particles_list[p].stat == False:
            particles_list[p].move(speed)
            status = check_status(particles_list[p])

            if (status[0] == True):
                particles_list[p].resetParticle(x_max, y_max, z_max, d_env)
            elif (status[1] == True ):
                particles_list[p].stat = True

                pos = particles_list[p].getCurPosition()
                env[pos[0]][pos[1]][pos[2]] = 1
                
                particles_list[p].setBound(d_env, dist, z_max)
                
                global particles
                particles -= 1
            else:
                pos = status[2]
                particles_list[p].x1 = pos[0]
                particles_list[p].y1 = pos[1]
                particles_list[p].z1 = pos[2]

                x[p] = pos[0]
                y[p] = pos[1]
                z[p] = pos[2]
        else: 
            continue
        
def update_points():
    graph._offsets3d = (x, y, z)
    return graph

fig = plt.figure(figsize=(5, 5))

ax = fig.add_subplot(111, projection="3d")
graph = ax.scatter(x, y, z, s = 5, color ='m') #, edgecolor='pink', facecolor='green',linewidth=1)

ax.set_xlim3d(x_min, x_max)
ax.set_ylim3d(y_min, y_max)
ax.set_zlim3d(z_min, z_max)

ax.set_box_aspect((x_max, y_max, z_max))
while particles > 0:
    forestGrowth()
    update_points()
    plt.pause(0.0001)
    
plt.show()