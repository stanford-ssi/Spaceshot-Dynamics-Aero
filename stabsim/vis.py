import matplotlib.pyplot as plt
import numpy as np

def kinematics(profile, rho=True, show=True):
    end_burn = profile.motor.t[-1]

    fig, (ax1, ax2) = plt.subplots(2, 1)

    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Velocity (m/s)')
    ax1.plot(profile.tt, profile.vel)
    ax1.axvline(end_burn, color='grey')

    ax2.plot(profile.tt, profile.altit, color='tab:blue')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Altitude (m)')
    if rho:
        ax2 = plt.twinx()
        ax2.set_ylabel('Air Density(kg/m^3)')
        ax2.plot(profile.tt, profile.rho(), color='tab:red')

    if show:
        plt.show()
    else:
        return fig

def spin(profile, gyro=True, dynamic=True, label_end=False, show=True):
    fig = plt.figure()
    newplt = fig.add_subplot(111)

    newplt.set_xlabel('Time (s)')
    newplt.set_ylabel('Spin (rad/s)')

    end_burn = profile.motor.t[-1]
    spin = profile.spin()
    spin = spin.reshape(spin.shape[0],)
    newplt.plot(profile.tt, spin, 'k', label='Expected Spin')
    if label_end:
        newplt.axvline(end_burn, color='grey', label='End of Motor Burn')

    if gyro:
        gyro_stab = profile.gyro_stab_crit()
        newplt.plot(profile.tt, gyro_stab, 'tab:blue', label='Gyroscopic Stability Threshold')
        newplt.fill_between(profile.tt, 0, newplt.get_ylim()[1], where=spin<gyro_stab, facecolor='red', alpha=0.5)
    if dynamic:
        dyn_stab = profile.dynamic_stab_crit()
        newplt.plot(profile.tt, dyn_stab, 'tab:green', label='Dynamic Stability Threshold')
        newplt.fill_between(profile.tt, 0, newplt.get_ylim()[1], where=spin<dyn_stab, facecolor='red', alpha=0.5)

    newplt.legend(loc='best')

    if show:
        newplt.show()
    else:
        return fig

def motor(motor, timesteps=100, show=True):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    time = motor.t

    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Mass (kg)')
    ax1.plot(time, [motor.mass(t) for t in time])

    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('I_x (kg*m/s)')
    ax2.plot(time, [motor.ix(t) for t in time])

    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('I_z (kg*m/s)')
    ax3.plot(time, [motor.iz(t) for t in time])

    if show:
        plt.show()
    else:
        return fig

def mass(profile):
    end_burn = profile.motor.t[-1]
    
    plt.xlabel('Time (s)')
    plt.ylabel('Mass (kg)')
    plt.plot(profile.tt, profile.mass)
    plt.axvline(end_burn, color='grey')

    plt.show()

