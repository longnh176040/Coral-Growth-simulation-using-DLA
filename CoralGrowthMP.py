from mpl_toolkits.mplot3d.axes3d import get_test_data
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import random as rd
import pprint
from Coral import Coral
from Particle_v2 import Particle
import time
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

x_min = 0
y_min = 0
z_min = 0
x_max = 100
y_max = 100
z_max = 100

numPos = 3
dist = 10

data = None
tree = np.empty(numPos) 

sendBuf = np.empty(numPos)
recvBuf = None

particals = 100000

if rank == 0:
    #Initialize environment
    env = np.zeros((x_max+1, y_max+1, z_max+1))
    x = []              #list for append point for drawing
    y = []
    z = []
    #forest = []

    #data = np.empty(size*numPos)

    for i in range(size):
        x.append(rd.randrange(x_min + dist, x_max - dist))
        y.append(rd.randrange(y_min + dist, y_max - dist))
        z.append(0)

        env[x[i]][y[i]][z[i]] = 1
        #c = Coral((x[i], y[i], z[i], x[i], y[i]))
        #forest.append(c)
else:
    env = None

def sendEnvironment():
    # if rank == 0:
    #     for i in range (0, size*numPos, numPos):
    #         data[i] = forest[int(i/numPos)].getXmax()
    #         data[i+1] = forest[int(i/numPos)].getYmax()
    #         data[i+2] = forest[int(i/numPos)].getZmax() 
    #         data[i+3] = forest[int(i/numPoint)].getXmin() 
    #         data[i+4] = forest[int(i/numPoint)].getYmin() 

    global env
    env = comm.bcast(env, root=0)    
    #comm.Scatter(data, tree, root=0)

def check_status(point):    #point = x2, y2, z2
    collision = False
    outLimit = False

    pos = point.getNextPosition()

    if pos[0] < 0 or pos[0] > x_max-1 or pos[1] < 0 or pos[1] > y_max-1 or pos[2] < 0:
        outLimit = True        
    elif env[int(pos[0])][int(pos[1])][int(pos[2])] == 1:
        collision = True
    return [outLimit, collision, pos]

def forestGrowth():
    global sendBuf
    p = Particle(z_max)

    while(True):
        p.move()
        status = check_status(p)
        if (status[0] == True):
            for i in range (numPos):
                sendBuf[i] = -1
            break
        elif (status[1] == True ):
            pos = p.getCurPosition()
            for i in range (numPos):
                sendBuf[i] = pos[i]
            break
        else:
            pos = status[2]
            p.x1 = pos[0]
            p.y1 = pos[1]
            p.z1 = pos[2] 
    del p

def gatherData():
    if rank == 0:
        global recvBuf
        recvBuf = np.empty(numPos*size)  

    comm.Gather(sendBuf, recvBuf, root=0)

    if (rank == 0):
        #print('Rank: ',rank, ', recvbuf received: ',recvBuf)
        for i in range (0, recvBuf.size, numPos):
            if recvBuf[i] == -1: 
                continue
            else:
                env[int(recvBuf[i])][int(recvBuf[i+1])][int(recvBuf[i+2])] = 1
                x.append(recvBuf[i])
                y.append(recvBuf[i+1])
                z.append(recvBuf[i+2])

                print(" x2 " + str(recvBuf[i]) + " y2 " + str(recvBuf[i+1]) + " z2 " + str(recvBuf[i+2]))

                global particals
                particals -= 1

def update_points():
    global x, y, z
    graph._offsets3d = (x, y, z)
    return graph

if rank == 0:
    fig = plt.figure(figsize=(5, 5))

    ax = fig.add_subplot(111, projection="3d")
    graph = ax.scatter(x, y, z, s = 5, color='m')

    ax.set_xlim3d(x_min, x_max)
    ax.set_ylim3d(y_min, y_max)
    ax.set_zlim3d(z_min, z_max)

while (particals > 0):
    sendEnvironment()
    forestGrowth()
    gatherData()

    if rank == 0:
        update_points()
        plt.pause(0.05)

plt.show()