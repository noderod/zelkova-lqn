## Large Quasilinear & Non-Linear PDE Solver
--------

### Introduction

Zelkova-LQN is a numerical solver for PDEs. The project is currently under development and can only solve PDEs of two variables, with the left side being only
a partial derivative of time.






### Data storage
LQN uses both Redis and InfluxDB as auxiliary databases.



### Overview

A comprehensive documentation of each zelkova component is available in the [documentation directory](./docs):
* [User signup, login, and credentials](./docs/user-info.md)




### Installation and setup



### Examples and Solved problem

A variety of solved problems are availble in the directory *./examples*. Each consists of a JSON file for LQN processing
and a python program that solves the same PDE.  
The python program is executed in serial with the numpy library. Speed is not the main concern, rather, it can be used as a validation tool. After being executed, each program will output a text file with its results. Results are ordered from lower to higher 't', per line; and from lower to higher 'x' within
the same line. 

