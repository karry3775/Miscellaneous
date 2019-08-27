import matplotlib.pyplot as plt
import math as m
import numpy as np


class Obstacles:
    def __init__(self, x,y,rad):
        self.x = x
        self.y = y
        self.radius = rad

class Source:
    def __init__(self, x,y):
        self.x = x
        self.y = y
"""
defining  Global Obstacles
"""
ob1 = Obstacles(2,2,0.5)
ob2 = Obstacles(5,8,1)
ob3 = Obstacles(8,6,1.5)
ob4 = Obstacles(5,2,0.75)
ob5 = Obstacles(9,1,1)
obs_all = [ob1, ob2, ob3, ob4, ob5]

x_residual = []
y_residual = []

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def plot_setup():
    plt.axis('scaled')
    plt.xlim(0,10)
    plt.ylim(0,10)
    plt.gca().set_facecolor((0.0, 0.0, 0.0))

def plot_obs(ob):
    c1 = plt.Circle((ob.x, ob.y),ob.radius,fc='w',ec='k',fill=True)
    plt.gca().add_patch(c1)

def plot_residual(x_res, y_res):
    for i in range(len(x_res)):
        plt.plot(x_res[i],y_res[i],'r.')

def magic_function(start_x, start_y, angle):
    global x_residual, y_residual
    orig_start_x = start_x
    orig_start_y = start_y
    #find radius
    thresh = 0.05
    best_rad = 999
    while best_rad > thresh:
        best_rad = 999
        for obs in obs_all:
            dist = m.sqrt((start_x - obs.x)**2 + (start_y - obs.y)**2) - obs.radius
            if dist<best_rad:
                best_rad = dist
        #draw a circle
        c = plt.Circle((start_x, start_y), best_rad, ec='w',fill=True,fc='w',alpha=0.5)
        plt.gca().add_patch(c)
        start_x = start_x + best_rad*m.cos(angle)
        start_y = start_y + best_rad*m.sin(angle)
        # plt.pause(0.001)
        if m.sqrt((orig_start_x - start_x)**2 +(orig_start_y- start_y)**2)>14:
            break

    x_residual.append(start_x)
    y_residual.append(start_y)
    return m.sqrt((orig_start_x - start_x)**2 +(orig_start_y- start_y)**2)

def cast_ray(src):
    global x_residual, y_residual
    #lets first define the range of angles
    start_angle = -m.pi/2
    end_angle = 4*m.pi

    #extract the start point
    start_x = src.x
    start_y = src.y

    #create range of theta values
    angles = np.linspace(start_angle, end_angle, 500)
    range = 14
    for angle in angles:
        plt.cla()
        plot_setup()
        range = magic_function(start_x, start_y, angle)
        end_x = start_x + range*m.cos(angle)
        end_y = start_y + range*m.sin(angle)
        plt.plot([start_x, end_x],[start_y, end_y],'w--')
        # plot_residual(x_residual, y_residual)

        # if isclose(angle%10,0,abs_tol=1,rel_tol=0.5):
        #     x_residual = []
        #     y_residual = []
        """
        plotting Obstacles
        """
        plot_obs(ob1)
        plot_obs(ob2)
        plot_obs(ob3)
        plot_obs(ob4)
        plot_obs(ob5)

        plt.pause(0.001)

def main():

    """
    defining Source
    """
    src = Source(5,5)
    plt.plot(src.x,src.y,'go',label='Source')
    cast_ray(src)

    plt.legend()
    plt.show()



if __name__=="__main__":
    main()
