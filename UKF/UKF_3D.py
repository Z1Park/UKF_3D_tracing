"""Copyright 2021 Z1 Park.
FilterPy library.
http://github.com/rlabbe/filterpy
This is licensed under an MIT license. See the readme.MD file
for more information.
"""

from math import radians, atan2, sin, cos
from numpy import array
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from filterpy.kalman import UnscentedKalmanFilter as UKF
from filterpy.kalman import JulierSigmaPoints
from numpy.random import randn
    

def convert_to_scs(x, y, z):
    '''
    r       radial distance of spherical coordinate system
    theta   polar angle(theta) of spherical coordinate system
    phi     azimuthal angle(phi) of spherical coordinate system
    '''
    r = (x**2+y**2+z**2)**.5
    theta = atan2((x**2+y**2)**.5, z)
    phi = atan2(y, x)
    return ([r, theta, phi])

def convert_to_ocs(r, theta, phi):
    '''
    x       x distance from zero point in orthogonal coordinate system
    y       y distance from zero point in orthogonal coordinate system
    z       z distance from zero point in orthogonal coordinate system
    '''
    x = r*sin(theta)*cos(phi)
    y = r*sin(theta)*sin(phi)
    z = r*cos(theta)
    return ([x, y, z])



def hx(x):
    return (x)

def fx(x, dt):
    return (x)

dt = 1/10

sp = JulierSigmaPoints(n=3, kappa=1)
kf = UKF(dim_x=3, dim_z=3, dt=dt, hx=hx, fx=fx, points=sp)

kf.x = array([0, 0, 0])

'''
R : Measurement noise matrix
Q : process noise matrix
P : Current state covariance matrix
'''
kf.R *= 5
kf.Q *= 1
kf.P *= 0.1

func = kf


fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111, projection='3d') # Axe3D object

raw_data = []

for i in range(200):
    raw_data.append([75+randn()*2, radians(90)+radians(randn()*2), radians(i*3)+radians(randn()*2)])

    if i % 15 == 10:
        raw_data[-1][0] += 50

x_p = []
y_p = []
z_p = []

def animate(i):
    if len(raw_data) > 0:
        z = raw_data[0]
        del raw_data[0]

        if True:
            func.predict()
            func.update(z)
            
            tmp_x, tmp_y, tmp_z = convert_to_ocs(func.x[0], func.x[1], func.x[2])

        else:       
            [tmp_x, tmp_y, tmp_z] = convert_to_ocs(*z)

        if len(x_p) > 10:
            # del x_p[0]
            # del y_p[0]
            # del z_p[0]
            x_p.append(tmp_x)
            y_p.append(tmp_y)
            z_p.append(tmp_z)
        else:
            x_p.append(tmp_x)
            y_p.append(tmp_y)
            z_p.append(tmp_z)

    plt.cla()
    ax.scatter(0,0,0,color='b',marker='o',s=30,alpha=0.9)
    ax.scatter(x_p[-1],y_p[-1],z_p[-1],color='k',marker='o',s=50,alpha=0.8)
    ax.plot(x_p, y_p, z_p, color='r', marker='o', alpha=0.4)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim3d(-100, 100)
    ax.set_ylim3d(-100, 100)
    ax.set_zlim3d(-100, 100)


ani = FuncAnimation(fig, animate, interval=50)

plt.show()
