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
import os

x_min = 0
y_min = 0
z_min = 0
x_max = 20
y_max = 20
z_max = 20
tmp = 1

#particals = 100000

#Initialize environment
env = np.zeros((x_max+1, y_max+1, z_max*tmp+1))

#Initialize root
#seed = [5,5,0]
x = [] #list for append point for drawing
y = []
z = []

forest = []

for i in range(10):
    x.append(rd.randrange(0, x_max))
    y.append(rd.randrange(0, y_max))
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
        collision = True
    return [outLimit, collision, pos]

def forestGrowth(gif):

    if not os.path.isdir("images"):
        os.mkdir("images")
    if gif:
        import imageio

    randomWalkerCount = 0
    usedInterval = []

    while (True):
        for tree in forest:
            #print("======TREE GROWING=======")
            p = Particle(tree, z_max*tmp)
            while(True):
                p.move()
                status = check_status(p)
                if (status[0] == True):
                    print("======OUT LIMIT=======")
                    break
                elif (status[1] == True ):
                    randomWalkerCount += 1
                    pos = p.getCurPosition()
                    print("========COLLIDED========")
                    env[pos[0]][pos[1]][pos[2]] = 1
                    tree.extend(pos)
                    break
                else:
                    pos = status[2]
                    p.x1 = pos[0]
                    p.y1 = pos[1]
                    p.z1 = pos[2]
            del p

            intervalSavePic = range(0, 100, 20)
            if gif:
                if randomWalkerCount in intervalSavePic:
                    print("save picture")
                    # append to the used count
                    if (randomWalkerCount not in usedInterval):
                        usedInterval.append(randomWalkerCount)
                    label = str(randomWalkerCount)
                    filename = "images/cluster"+label+".png"
                    # print(filename)
                    plt.title("DLA Cluster", fontsize=20)
                    plt.figure()
                    ax = plt.subplot(projection='3d')
                    ax.voxels(env)
                    # plt.cm.Blues) #ocean, Paired
                    # plt.matshow(mat, interpolation='nearest', cmap=colorMap)
                    # plt.xlabel("direction, $x$", fontsize=15)
                    # plt.ylabel("direction, $y$", fontsize=15)
                    plt.savefig(filename, dpi=200)
                    plt.close()

            if randomWalkerCount >= 500:
                break

        if randomWalkerCount >= 500:
            print("========FINISH========")
            break
        

    plt.title("DLA Cluster", fontsize=20)
    # plt.cm.Blues) #ocean, Paired
    plt.figure()
    ax = plt.subplot(projection='3d')
    ax.voxels(env)
    # plt.ylabel("direction, $y$", fontsize=15)
    plt.savefig("images/cluster.png", dpi=200)
    plt.close()
    print(usedInterval)
    if gif:
        with imageio.get_writer('images/movie.gif', mode='I') as writer:
            for i in usedInterval:
                filename = "images/cluster"+str(i)+".png"
                image = imageio.imread(filename)
                writer.append_data(image)
                os.remove(filename)
            image = imageio.imread("images/cluster.png")
            writer.append_data(image)

    return(env)

forestGrowth(True)
# start = time.time()
# def update_points(num):
#     #DLA()
#     forestGrowth()
    
#     if (particals <= 0):
#         ani.event_source.stop()
#         end = time.time()
#         print("EXECUTION TIME:", end - start)

#     graph._offsets3d = (x, y, z)
#     return graph

# fig = plt.figure(figsize=(5, 5))

# ax = fig.add_subplot(111, projection="3d")
# graph = ax.scatter(x, y, z, s = 5, color='m')

# ax.set_xlim3d(x_min, x_max)
# ax.set_ylim3d(y_min, y_max)
# ax.set_zlim3d(z_min, z_max)

# ani = animation.FuncAnimation(fig, update_points, frames=200, interval=100, blit=False)
# plt.show()