#!/usr/bin/env python3
import math
from sympy import Matrix, pretty_print

pi = round(math.pi, 2)
#convert_to_rad = pi/180

# Function that converts input joint angle degrees to radians
def convert_to_rad(theta):
    theta = theta*pi/180
    return theta

#Function that calculates the final transformation matrix for given joint angles
def calculate(theta_1, theta_2, theta_3, theta_4, theta_5, theta_6):

    A1 = Matrix([[round(math.cos(theta_1)), 0, round(math.sin(theta_1)), 0],
                [round(math.sin(theta_1)), 0, -round(math.cos(theta_1)), 0],
                [0, 1, 0, 0.1625],
                [0, 0, 0, 1]])

    A2 = Matrix([[round(math.cos(theta_2)), -round(math.sin(theta_2)), 0, -0.425*round(math.cos(theta_2))],
                [round(math.sin(theta_2)), round(math.cos(theta_2)), 0, -0.425*round(math.sin(theta_2))],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])

    A3 = Matrix([[round(math.cos(theta_3)), -round(math.sin(theta_3)), 0, -0.3922*round(math.cos(theta_3))],
                [round(math.sin(theta_3)), round(math.cos(theta_3)), 0, -0.3922*round(math.sin(theta_3))],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])
    
    A4 = Matrix([[round(math.cos(theta_4)), 0, round(math.sin(theta_4)), 0],
                [round(math.sin(theta_4)), 0, -round(math.cos(theta_4)), 0],
                [0, 1, 0, 0.1333],
                [0, 0, 0, 1]])

    A5 = Matrix([[round(math.cos(theta_5)), 0, -round(math.sin(theta_5)), 0],
                [round(math.sin(theta_5)), 0, round(math.cos(theta_5)), 0],
                [0, -1, 0, 0.0997],
                [0, 0, 0, 1]])

    A6 = Matrix([[round(math.cos(theta_6)), -round(math.sin(theta_6)), 0, 0],
                [round(math.sin(theta_6)), round(math.cos(theta_6)), 0, 0],
                [0, 0, 1, 0.0996],
                [0, 0, 0, 1]])
                
    # Final transformation matrix (T) = Product of all individual transformations A1-A6            
    T = A1*A2*A3*A4*A5*A6
    pretty_print(T)

# Calculating the transformation matrices for Home and Spawn configurations
print("Spawn Configuration: ")
calculate(0, -1.5708, 1.5708, -1.5708, 1.5708, 0) # Home configuration
print('\n')

print("Home Configuration")
calculate(0, 0, 0, 0, 0, 0) # Configuration 1
print('\n')