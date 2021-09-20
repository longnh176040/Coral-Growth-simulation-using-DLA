from mpl_toolkits.mplot3d.axes3d import get_test_data
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import random as rd
import pprint
from Coral import Coral
from Particle import Particle
import time

x_min = 0
y_min = 0
z_min = 0
x_max = 100
y_max = 100
z_max = 100
tmp = 1

particals = 100000

#Initialize environment
env = np.zeros((x_max, y_max, z_max*tmp))

#Initialize root
#seed = [5,5,0]
x = [] #list for append point for drawing 25, 11, 29, 33, 16 \\ 35, 12, 24, 36, 18
y = []
z = []

forest = []

for i in range(10):
    x.append(rd.randrange(10, x_max-10))
    y.append(rd.randrange(10, y_max-10))
    z.append(0)

    env[x[i]][y[i]][z[i]] = 1
    c = Coral((x[i], y[i], z[i]))
    forest.append(c)

#pprint.pprint(env)

def check_status(point):    #point = x2, y2, z2
    collision = False
    outLimit = False

    pos = point.getNextPosition()

    if pos[0] < 0 or pos[0] > x_max-1 or pos[1] < 0 or pos[1] > y_max-1 or pos[2] < 0:
        outLimit = True        
    elif env[pos[0]][pos[1]][pos[2]] == 1:
        #print(" x2 " + str(xc) + " y2 " + str(yc) + " z2 " + str(zc))
        collision = True
    return [outLimit, collision, pos]

def forestGrowth():
    for tree in forest:
        p = Particle(tree, z_max*tmp)
        while(True):
            p.move()
            status = check_status(p)
            if (status[0] == True):
                break
            elif (status[1] == True ):
                pos = p.getCurPosition()
                env[pos[0]][pos[1]][pos[2]] = 1
                tree.extend(pos)
                
                global particals
                particals -= 1

                x.append(pos[0])
                y.append(pos[1])
                z.append(pos[2])
                break
            else:
                pos = status[2]
                p.x1 = pos[0]
                p.y1 = pos[1]
                p.z1 = pos[2]
        del p
        
start = time.time()

def update_points(num):
    #DLA()
    forestGrowth()
    
    if (particals <= 0):
        #ani.event_source.stop()
        end = time.time()
        print("EXECUTION TIME:", end - start)

    graph._offsets3d = (x, y, z)
    return graph

fig = plt.figure(figsize=(5, 5))

ax = fig.add_subplot(111, projection="3d")
graph = ax.scatter(x, y, z, s = 5, color='m')

ax.set_xlim3d(x_min, x_max)
ax.set_ylim3d(y_min, y_max)
ax.set_zlim3d(z_min, z_max)

while particals > 0:
    update_points(1)
    plt.pause(0.05)
    
#ani = animation.FuncAnimation(fig, update_points, frames=200, interval=100, blit=False)
plt.show()