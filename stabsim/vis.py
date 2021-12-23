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

def spin(profile, gyro=True, dynamic=True, label_end=False, label_mach=False, show=True):
    fig = plt.figure()
    newplt = fig.add_subplot(111)

    newplt.set_xlabel('Time (s)')
    newplt.set_ylabel('Spin (rad/s)')

    spin = profile.spin()
    spin = spin.reshape(spin.shape[0],)
    plt.plot(profile.tt, spin, 'k', label='Expected Spin')

    if label_end:
        end_burn = profile.motor.t[-1]
        plt.axvline(end_burn, color='rosybrown', label='End of Motor Burn')
    if label_mach:
        mach = profile.tt[np.abs(profile.vel - 343).argmin()]
        plt.axvline(mach, color='burlywood', label='Mach')

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

def rocket(profile, label_mach=False):
    plt.xlabel('Times (s)')
    plt.ylabel('Coeffs (non-dimensionalized)')

    plt.plot(profile.tt, profile.rocket.get_cd(), label=r'$C_D$')
    plt.plot(profile.tt, profile.rocket.get_cm_alpha(), label=r'$C_{M_\alpha}$')
    plt.plot(profile.tt, profile.rocket.get_cl_alpha(), label=r'$C_{L_\alpha}$')

    if label_mach:
        temp = profile.temp()
        mach = 343 * np.sqrt(temp / 300)
        mach_trans = profile.tt[np.abs(profile.vel - mach).argmin()]

        plt.axvline(mach_trans, color='burlywood', label='Mach')
        plt.fill_between(profile.tt, 0, plt.ylim()[1], where=np.logical_and(profile.vel>0.6*mach, profile.vel<1.4*mach), facecolor='k', alpha=0.3)

    plt.legend()

    plt2 = plt.twinx()
    plt2.plot(profile.tt, profile.rocket.get_cm_dot(), 'tab:red', label=r'$|C_{M_{\dot{\alpha}}}+C_{M_{\dot{q}}}|$')

    plt.legend()
    plt.show()

def motor(motor, timesteps=100, show=True):
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