# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 17:01:48 2017
Waterloop halbach wheel model
@author: Geoffrey
"""

import numpy as np
import matplotlib.pyplot as plt
import decimal as dc

z = 0.00412 #distance of magnet from rail
mu = 4*np.pi*10**(-7) #magnetic permeability
#m = 7.210324 * 1.75 #magnetic moment of 1 magnet
m = 4.916*1.75
railThickness = 0.005
railResistivity = 2.92E-8
w =  (2*railResistivity)/(mu*railThickness)#
#radius = 0.117#radius of the halbach wheel
radius = 0.05#radius of the small scale model
maxVelocity = 10
podMass = 250

#variables for damping
#magnetRadius = 0.0127#radius of cylindrical model of magnet
magnetRadius = 0.009525#small scale model

sigma = 1/(railResistivity)

#calculation of new equilibrium point
for displacement in range(0, int(z*100000)):
    absDisplacement = displacement/100000
    z1 = z - absDisplacement
    z1Opposite = z + absDisplacement
    insideLift = (3*mu*m**2)/(32*np.pi*z1**4)*(1-w/(25**2+w**2)**0.5)*0.8
    outsideLift = (3*mu*m**2)/(32*np.pi*z1Opposite**4)*(1-w/(25**2+w**2)**0.5)*0.8
    if insideLift - (outsideLift + 300) >= 0:
        break

#calculation of initial deflection
meanDeflectionAcceleration = 150 / podMass #average net force divided by mass
equilibriumVelocity = (2*meanDeflectionAcceleration * absDisplacement)**0.5 #initial velocity going away from equilibrium

deflectionTime = equilibriumVelocity/(insideLift/podMass)#deflection time from reference
deflection = equilibriumVelocity*deflectionTime - 0.5*(insideLift/podMass)*deflectionTime**2
##DOUBLE CHECKED TO THIS POINT##

#flux density through the rail
phi = mu/2*m*((magnetRadius**2/(magnetRadius**2+(z1-deflection)**2)**1.5)-magnetRadius**2/((magnetRadius**2+z**2)**1.5))
dampingCoefficient = railThickness*np.pi*sigma*phi**2/(2*(deflection)**2)
#paper for damping coefficient:  doi:10.1088/0022-3727/39/18/002

magnetSpringConstant = 4*(3*mu*m**2)/(32*np.pi*z**5)*(1-w/(8**2+w**2)**0.5)

lambdaOne = (-dampingCoefficient + (abs(dampingCoefficient**2-4*podMass*magnetSpringConstant))**0.5)/(2*podMass)
lambdaTwo = (-dampingCoefficient - (abs(dampingCoefficient**2-4*podMass*magnetSpringConstant))**0.5)/(2*podMass)
omega = (0.5*(abs(dampingCoefficient**2 - 4*magnetSpringConstant*podMass)**0.5))/podMass
#arbitrary constants
A = 1
B = 1
"""
Sources for damping

https://www.ncsu.edu/crsc/events/ugw05/slides/root_harmonic.pdf
https://ocw.mit.edu/courses/mathematics/18-03sc-differential-equations-fall-2011/unit-ii-second-order-constant-coefficient-linear-equations/damped-harmonic-oscillators/MIT18_03SCF11_s13_2text.pdf

DRIVEN OSCILLATION:
https://www.princeton.edu/~wbialek/intsci_web/dynamics2.6.pdf
http://web.physics.ucsb.edu/~fratus/phys103/LN/DHM.pdf

"""
#function for linear velocity to rpm conversion
def rpm (velocity, radius):
    return (60*velocity/(radius*2*np.pi))
    
if __name__ == '__main__':
    liftForce = [0]*maxVelocity
    dragForce = [0]*maxVelocity
    velocity = [0]*maxVelocity
    revolutionsPerMinute = [0]*maxVelocity
    testRadius = [0]*30
    revOfMax = [0]*30
    torque = [0]*30
    
    #calculation of lift to drag forces
    for v in range(1,maxVelocity):
            liftForce[v] = (3*mu*m**2)/(32*np.pi*z**4)*(1-w/(v**2+w**2)**0.5)*0.8
            dragForce[v] = w*liftForce[v]/v*0.8
            velocity[v] = v
            revolutionsPerMinute[v] = rpm(v, radius)
    
    plt.plot (velocity, liftForce)
    plt.plot (velocity, dragForce)
    plt.title('Lateral/Thrust Force Per Wheel vs Relative Velocity')
    plt.ylabel('Force (N)')
    plt.xlabel('Relative Velocity (m/s)')
    plt.legend(['Lateral Force', 'Thrust Force'], loc='upper left')
    plt.show()

    plt.plot (revolutionsPerMinute, liftForce)
    plt.plot (revolutionsPerMinute, dragForce)
    plt.title("Lateral/Thrust Force Per Wheel vs RPM While Stationary")
    plt.ylabel('Force (N)')
    plt.xlabel('Revolutions Per Minute')
    plt.legend(['Lift Force', 'Drag Force'], loc='upper left')
    plt.show() 
       
    plt.plot (velocity, revolutionsPerMinute)
    plt.ylabel('Revolutions Per Minute')
    plt.xlabel('Velocity')
    plt.show()
    
    #iterative rpm calculation for desired velocity
    initV = 70
    rpms = [0] * 50
    for v2 in range (71,120 ):
        x = 0
        t = 0
        prevV = initV
        while prevV < 80:
            t = t + 0.1
            newVelocity = prevV + (3*mu*m)/(32*np.pi*z**4)*(1-w/((v2-prevV)**2+w**2)**0.5)*w/(v2-prevV)*0.8*t
            x = x + (prevV + newVelocity)/2*0.1
            if x > 700:
                break
            prevV = newVelocity
        if x <= 700:
            rpms[v2-71] = rpm(v2, radius)
            

    
    #calculation of lift, drag, and torque for varying radii
    for r in range(1, 30):
        for v in range(1,maxVelocity):
            liftForce[v] = (3*mu*m**2)/(32*np.pi*z**4)*(1-w/(v**2+w**2)**0.5)*0.8
            dragForce[v] = w*liftForce[v]/v*0.8
            velocity[v] = v
            revolutionsPerMinute[v] = rpm(v, r/100)
        testRadius[r] = r/100
        revOfMax[r] = revolutionsPerMinute[dragForce.index(max(dragForce))] + rpm(100, r/100)
        torque[r] = (r/100)*max(dragForce)

    
    plt.plot(testRadius, revOfMax)
    plt.plot(testRadius, torque)
    plt.ylabel("Revolutions Per Minute")
    plt.xlabel("Radius (m)")
    plt.show()
    
    
    fig, ax1 = plt.subplots()
    ax1.plot(testRadius, revOfMax, 'b-')
    ax1.set_ylabel('Revolutions Per Minute', color='b')
    ax1.set_xlabel("Radius")
    # Make the y-axis label, ticks and tick labels match the line color.
    
    ax2 = ax1.twinx()
    ax2.plot(testRadius, torque, 'r.')
    ax2.set_ylabel('Torque (N*m/s)', color='r')
    fig.tight_layout()
    plt.show()
       
    
    #damping calculations
    time = [0]*10000
    x = [0]*10000
    for t in range(0,10000):
        timer = t/5000
        time[t] = timer
        #Under Damped
        #x[t] = (deflection**2+(dampingCoefficient*deflection/(2*podMass*omega))**2)**0.5*np.exp(-dampingCoefficient*timer/(2*podMass))*(np.cos(omega*timer-np.arctan(A/B)))
        #x[t] = np.e**(-dampingCoefficient*timer/(2*podMass))*(A*np.sin(omega*timer)+B*np.cos(omega*timer))
        
        #Over Damped
        A = -deflection*(lambdaTwo/lambdaOne)/(1-lambdaTwo/lambdaOne)
        B = deflection - A
        x[t] = A*np.exp(lambdaOne*timer)+B*np.exp(lambdaTwo*timer)
    plt.plot (time, x)
    plt.title('Damping of 300N Forced Oscillation')
    plt.ylabel('X Displacement from Equilibrium (m)')
    plt.xlabel('Time(s)')
    plt.show() 