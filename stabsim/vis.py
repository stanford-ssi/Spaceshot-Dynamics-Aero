import matplotlib.pyplot as plt
import numpy as np

def kinematics(profile, rho=True, show=True):
    end_burn = profile.motor.t[-1]

    plt.subplot(311)
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.plot(profile.tt, profile.vel)
    plt.axvline(end_burn, color='grey')

    plt.subplot(313)
    plt.plot(profile.tt, profile.altit, color='tab:blue')
    plt.xlabel('Time (s)')
    plt.ylabel('Altitude (m)')
    if rho:
        plt2 = plt.twinx()
        plt2.set_ylabel('Air Density(kg/m^3)')
        plt2.plot(profile.tt, profile.rho(), color='tab:red')

    if show:
        plt.show()
    else:
        return plt

def spin(profile, gyro=True, dynamic=True, label_end=False, show=True):
    plt.xlabel('Time (s)')
    plt.ylabel('Spin (rad/s)')

    end_burn = profile.motor.t[-1]
    spin = profile.spin()
    spin = spin.reshape(spin.shape[0],)
    plt.plot(profile.tt, spin, 'k', label='Expected Spin')
    if label_end:
        plt.axvline(end_burn, color='grey', label='End of Motor Burn')

    if gyro:
        gyro_stab = profile.gyro_stab_crit()
        plt.plot(profile.tt, gyro_stab, 'tab:blue', label='Gyroscopic Stability Threshold')
        plt.fill_between(profile.tt, 0, plt.ylim()[1], where=spin<gyro_stab, facecolor='red', alpha=0.5)
    if dynamic:
        dyn_stab = profile.dynamic_stab_crit()
        plt.plot(profile.tt, dyn_stab, 'tab:green', label='Dynamic Stability Threshold')
        plt.fill_between(profile.tt, 0, plt.ylim()[1], where=spin<dyn_stab, facecolor='red', alpha=0.5)

    plt.legend(loc='best')

    if show:
        plt.show()
    else:
        return plt

def motor(motor, timesteps=100, show=True):
    time = motor.t

    plt.subplot(311)
    plt.xlabel('Time (s)')
    plt.ylabel('Mass (kg)')
    plt.plot(time, [motor.mass(t) for t in time])

    plt.subplot(312)
    plt.xlabel('Time (s)')
    plt.ylabel('I_x (kg*m/s)')
    plt.plot(time, [motor.ix(t) for t in time])

    plt.subplot(313)
    plt.xlabel('Time (s)')
    plt.ylabel('I_z (kg*m/s)')
    plt.plot(time, [motor.iz(t) for t in time])

    if show:
        plt.show()
    else:
        return plt

def mass(profile):
    end_burn = profile.motor.t[-1]
    
    plt.xlabel('Time (s)')
    plt.ylabel('Mass (kg)')
    plt.plot(profile.tt, profile.mass)
    plt.axvline(end_burn, color='grey')

    plt.show()

