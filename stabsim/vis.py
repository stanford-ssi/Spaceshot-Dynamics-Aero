import matplotlib.pyplot as plt
import numpy as np

def kinematics(profile, rho=True):
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
        plt2.plot(profile.tt, profile.rho, color='tab:red')

    plt.show()

def spin(profile, gyro=True, dynamic=True, label_end=False, label_mach=False):
    plt.xlabel('Time (s)')
    plt.ylabel('Spin (rad/s)')

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
        plt.plot(profile.tt, gyro_stab, 'tab:blue', label='Gyroscopic Stability Threshold')
        plt.fill_between(profile.tt, 0, plt.ylim()[1], where=spin<gyro_stab, facecolor='red', alpha=0.5)
    if dynamic:
        dyn_stab = profile.dynamic_stab_crit()
        plt.plot(profile.tt, dyn_stab, 'tab:green', label='Dynamic Stability Threshold')
        plt.fill_between(profile.tt, 0, plt.ylim()[1], where=spin<dyn_stab, facecolor='red', alpha=0.5)

    plt.legend(loc='best')
    plt.show()

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

def motor(motor, timesteps=100):
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

    plt.show()

def mass(profile):
    end_burn = profile.motor.t[-1]
    
    plt.xlabel('Time (s)')
    plt.ylabel('Mass (kg)')
    plt.plot(profile.tt, profile.mass)
    plt.axvline(end_burn, color='grey')

    plt.show()