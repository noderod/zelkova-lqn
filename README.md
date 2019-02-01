## Large Quasilinear & Non-Linear PDE Solver
--------

### Introduction

Zelkova-LQN is a numerical solver for PDEs.  




### Data storage
LQN uses both Redis and InfluxDB as auxiliary databases. However, these databases are only used for storage after each step and once the PDE has been solved.
All information transfer between steps is done directly netwrok in order to improve performance.



### Overview

A comprehensive documentation of each zelkova component is available in the [documentation directory](./docs):
* [User signup, login, and credentials](./docs/user-info.md)
* [Main server, front-end](./docs/mainserver-info.md)





### Installation and setup



### Examples and Solved problem

A variety of solved problems are availble in the directory *./examples*. Each consists of a JSON file for LQN processing
and a python program that solves the same PDE.  
The python program is executed in serial with the numpy library. Speed is not the main concern, rather, it can be used as a validation tool. After being executed, each program will output a text file with its results. Results are ordered from lower to higher 't', per line; and from lower to higher 'x' within
the same line. 



### Current Status

Zelkova-LQN is currently under devlopment and still far from its final objective.  
The followibng roadmap reflects the intended progress:
1. 1 variable (PDE (t, x)) - 1 external node
2. 1 variable - N external nodes
3. Stochastic variables (uniform, normal)




