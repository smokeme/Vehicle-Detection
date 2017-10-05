
from filterpy.kalman import KalmanFilter
import numpy as np
    
# #define constant velocity model
# kf = KalmanFilter(dim_x=7, dim_z=4)
# kf.F = np.array([[1,0,0,0,1,0,0],[0,1,0,0,0,1,0],[0,0,1,0,0,0,1],[0,0,0,1,0,0,0],  [0,0,0,0,1,0,0],[0,0,0,0,0,1,0],[0,0,0,0,0,0,1]])
# kf.H = np.array([[1,0,0,0,0,0,0],[0,1,0,0,0,0,0],[0,0,1,0,0,0,0],[0,0,0,1,0,0,0]])
# 
# kf.R[2:,2:] *= 10.
# kf.P[4:,4:] *= 1000. #give high uncertainty to the unobservable initial velocities
# kf.P *= 10.
# kf.Q[-1,-1] *= 0.01
# kf.Q[4:,4:] *= 0.01
# 
# print(kf.R)
# print(kf.P)
# print(kf.Q)

n_measurements = 2
kf = KalmanFilter(dim_x=4, dim_z=n_measurements)
kf.F = np.array([[1,0,1,0],
                 [0,1,0,1],
                 [0,0,1,0],
                 [0,0,0,1]])
kf.H = np.array([[1,0,0,0],
                 [0,1,0,0]])
Q_std = 0.01
Q = np.zeros_like(kf.F)
Q[1,1] = Q_std**2
Q[3,3] = Q_std**2

R_std = 10.0
R = np.eye(n_measurements) * R_std**2

kf.Q = Q
kf.R = R
kf.x = np.array([0, 0, 0, 0]).reshape(-1,1)

import matplotlib.pyplot as plt
def demo_kalman_xy():
    N = 100
    true_x = np.linspace(0.0, 1000.0, N)
    true_y = true_x
    observed_x = true_x + 10*np.random.random(N)
    observed_y = true_y + 10*np.random.random(N)
    plt.plot(observed_x, observed_y, 'ro')
    result = []

    
    for meas in zip(observed_x, observed_y):
        kf.predict()
        z = np.array([meas[0], meas[1]]).reshape(-1,1)
        kf.update(z)
        result.append(kf.x[0:2])
        print(meas, kf.x[0], kf.x[1])
        
    kalman_x, kalman_y = zip(*result)
    plt.plot(kalman_x, kalman_y, 'g-')
    plt.show()
 
demo_kalman_xy()