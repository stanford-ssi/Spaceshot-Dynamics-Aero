import matplotlib.pyplot as plt

def kinematics(profile, rho=True):
    plt.subplot(311)
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.plot(profile.tt, profile.vel, label='')

    plt.subplot(313)
    plt.plot(profile.tt, profile.altit, label='altitude', color='tab:blue')
    plt.xlabel('Time (s)')
    plt.ylabel('Altitude (m)')
    if rho:
        plt2 = plt.twinx()
        plt2.set_ylabel('Air Density(kg/m^3)')
    plt.plot(profile.tt, profile.rho(), label='air density', color='tab:red')

    plt.show()

def spin(profile, gyro=True, dynamic=True):
    plt.xlabel('Time (s)')
    plt.ylabel('Spin (rad/s)')

    spin = profile.spin()
    spin = spin.reshape(spin.shape[0],)
    plt.plot(profile.tt, spin, 'k', label='Expected Spin')
    if gyro:
        gyro_stab = profile.gyro_stab_crit()
        print(gyro_stab.shape)
        plt.plot(profile.tt, gyro_stab, 'tab:blue', label='Gyroscopic Stability Threshold')
        plt.fill_between(profile.tt, 0, plt.ylim()[1], where=spin<gyro_stab, facecolor='red', alpha=0.5)
    if dynamic:
        dyn_stab = profile.dynamic_stab_crit()
        plt.plot(profile.tt, dyn_stab, 'tab:green', label='Dynamic Stability Threshold')
        # plt.fill_between(profile.tt, 0, plt.ylim()[1], where=spin<dyn_stab, facecolor='red', alpha=0.5)

    plt.show()
