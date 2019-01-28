"""
BASICS

Solves a complicated non-linear heat equation
"""


import finite_difference as fd
import math
import numpy.linalg as LA
import numpy as np



k = 0.001
h = 0.5
xmax = 7000
xmin = 0
tmax = 0.3
tmin = 0
a = 0.1256637
Te = 273
sigma = 5.670373E-8
R = 0.4


# Added one to include the ending
x_resolution = int((xmax-xmin)/h)+1
t_resolution = int((tmax-tmin)/k)+1

# Creates the bases
bu_x = fd.finite_difference_coefficients(1, 2, h)
bu_xx = fd.finite_difference_coefficients(2, 2, h)
bu_xxx = fd.finite_difference_coefficients(3, 6, h)


u_x = fd.partial_matrix(bu_x, x_resolution)
u_xx = fd.partial_matrix(bu_xx, x_resolution)
u_xxx = fd.partial_matrix(bu_xxx, x_resolution)



#####################################################
# EQUATION
#####################################################


U = np.zeros((x_resolution, 1))

#### Initial Conditions

for nvnv in range(0, x_resolution):
    U[nvnv][0] = 273


# Finds the step corresponding to a certain x
def step_from_x(one_x):
    return int(one_x/h)

special_IC = [[0, 50, 150, 230, 7000], [8200, 800, 3200, 4000, 3]]


for idid in range(0, len(special_IC[0])):
    U[step_from_x(special_IC[0][idid])][0] = special_IC[1][idid]




##### Boundary Conditions

BC = {
    0:{
        50:8200,
        230:4000,
        7000:3
    },

    1:{
        15:240
    }
}



# Iteratively solving the PDE
# ad-hoc approach for simplicity in reading

for tsep in range(0, t_resolution):

    tnow = tsep*k

    ##### Computes the appropriate derivatives

    # 0
    Z_0 = np.dot(u_xx, U)

    #1
    Z_1 = U

    # 2
    Z_2 = np.dot(u_x, U)

    # 3
    Z_3 = np.dot(u_xxx, U)


    #### Updates according to each derivative BC
    Z_2[step_from_x(15)][0] = 240


    #### Applies non-linear function

    # 3
    for wawa in range(0, x_resolution):
        Z_3[wawa][0] = math.log10(0.0001+abs(Z_3[wawa][0]))



    #### Applies quasilinear function
    # 0
    for ll in range(0, x_resolution):
        Z_0[ll][0] *= a*ll*h


    # 1
    for pop in range(0, x_resolution):
        Z_1[pop][0] *= sigma*a*(Te - Z_1[pop])    

    # 2
    for jkl in range(0, x_resolution):
        Z_2[jkl][0] *= R

    # 3
    for taj in range(0, x_resolution):
        Z_3[taj][0] *= (math.sqrt(tnow)*(taj*h)**2 )/Z_3[taj][0]


    #### Computes final U
    dU = np.add(np.add(Z_0, Z_1), np.add(Z_2, Z_3))

    U = np.add(U, k*dU)


    # Changes U according to BC in U 
    U[step_from_x(50)][0] = 8200
    U[step_from_x(230)][0] = 4000
    U[step_from_x(7000)][0] = 3


    # Stores result into a text file for further viewing
    with open("test-heat.txt", "a") as heatfile:
        # t; u(x1), u(x2), ..., u(xn)
        heatfile.write(str(tnow)+";")
        for qq in range(0, x_resolution-1):
            heatfile.write(str(U[qq][0])+",")
        else:
            heatfile.write(str(U[-1][0])+"\n")



    print("t = "+str(tnow)+" s")

