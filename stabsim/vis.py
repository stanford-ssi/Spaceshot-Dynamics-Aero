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
        ax2.plot(profile.tt, profile.rho, color='tab:red')

    if show:
        plt.show()
    else:
        return fig

def spin(profile, gyro=True, dynamic=True, label_end=False, label_mach=False, show=True):
    fig = plt.figure()

    plt.xlabel('Time (s)')
    plt.ylabel('Spin (rad/s)')

    spin = profile.spin()
    spin = spin.reshape(spin.shape[0],)
    plt.plot(profile.tt, spin, 'k', label='Expected Spin')

    if label_end:
        end_burn = profile.motor.t[-1]
        plt.axvline(end_burn, color='rosybrown', label='End of Motor Burn')
    if label_mach:
        mach = profile.tt[np.abs(profile.mach - 1).argmin()]
        plt.axvline(mach, color='burlywood', label='Mach')

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
        return fig

def rocket(profile, label_mach=False, show=True):
    fig = plt.figure()
    plt.xlabel('Times (s)')
    plt.ylabel('Coeffs (non-dimensionalized)')

    plt.plot(profile.tt, profile.rocket.get_cd(), label=r'$C_D$')
    plt.plot(profile.tt, profile.rocket.get_cm_alpha(), label=r'$C_{M_\alpha}$')
    plt.plot(profile.tt, profile.rocket.get_cl_alpha(), label=r'$C_{L_\alpha}$')

    if label_mach:
        mach_trans = profile.tt[np.abs(profile.mach - 1).argmin()]

        plt.axvline(mach_trans, color='burlywood', label='Mach')
        plt.fill_between(profile.tt, 0, plt.ylim()[1], where=np.logical_and(profile.mach>0.8, profile.mach<1.2), facecolor='k', alpha=0.3)
    
    plt.legend()

    plt2 = plt.twinx()
    plt2.plot(profile.tt, profile.rocket.get_cm_dot(), 'tab:red', label=r'$|C_{M_{\dot{\alpha}}}+C_{M_{\dot{q}}}|$')
    plt.legend()

    if show:
        plt.show()
    else:
        return fig

def motor(motor, show=True):
    fig = plt.figure()

    time = motor.t

    plt.xlabel('Time (s)')
    plt.ylabel('Mass (kg)')
    plt.plot(time, [motor.mass(t) for t in time], color='tab:blue', label='Mass')
    plt.legend(loc='lower left')

    plt2 = plt.twinx()
    plt2.set_ylabel('Thrust (N)')
    plt2.plot(time, [motor.thrust(t) for t in time], color='tab:red', label='Thrust')
    plt.legend(loc='upper right')

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