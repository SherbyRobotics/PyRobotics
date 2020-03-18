# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 20:28:17 2018

@author: Alexandre
"""

import numpy as np

import cProfile as profile
import pstats

from pyro.dynamic  import vehicle
from pyro.planning import discretizer
from pyro.analysis import costfunction, stopwatch
from pyro.planning import valueiteration

sys  = vehicle.Holonomic3DMobileRobotwithObstacles()

# Discrete world 
grid_sys = discretizer.GridDynamicSystem( sys , (41,41,21) , (3,3) )

# Cost Function
cf = costfunction.QuadraticCostFunction(
    q=np.ones(sys.n),
    r=np.ones(sys.m),
    v=np.zeros(sys.p)
)

cf.INF = 1E9

timer = stopwatch.Stopwatch()

# VI algo
vi = valueiteration.ValueIteration_ND( grid_sys , cf )

vi.initialize()
# vi.load_data('holonomic_3d_obstacles_vi_2')
profile.run('vi.compute_steps(400, maxJ=8000, plot=True)', 'profile_2')
vi.plot_cost2go(8000)
vi.assign_interpol_controller()
vi.plot_policy(0)
vi.plot_policy(1)
# vi.save_data('holonomic_3d_obstacles_vi_2')

p = pstats.Stats('profile_2')
p.strip_dirs().sort_stats(-1).print_stats()

# Closed loop
cl_sys = vi.ctl + sys

# Simulation and animation
cl_sys.x0   = np.array([9,0,0])
cl_sys.compute_trajectory(tf=20)
cl_sys.plot_trajectory('xu')
cl_sys.animate_simulation()