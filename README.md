# Stabsim
Calculating stability thresholds for finless spin-stabilized projectiles

## Getting Started
We're not too fancy here. Get started by cloning the repo
`git clone https://github.com/stanford-ssi/Spaceshot-Dynamics-Aero.git`

### Prerequisites
You'll need some basic packages for scientific computing with Python
- Python 3.6 or higher
- numpy==1.16.2
- scipy==1.2.1
- matplotlib==3.0.3
And some more exotic ones
- numpy-quaternion==2020.11.2.17.0.49
- numba==0.43.1
Stabsim also relies on Digital DATCOM to calculate aerodynamic coefficients. A compile version of the fortran is provided but its unlikely to work for everyone's set up. If you experience issues with DATCOM
1. Download the Digital Datcom via [Public Domain Aeronautical Software](http://www.pdas.com/datcom.html)
2. Install the Fortran compiler `gfortran`. On Ubuntu this is as simple as
```
sudo apt update && sudo apt upgrade
sudo apt install gfortran
```
3. Compile `stabsim/DigitalDATCOM/datcom.f` using the legacy version of gfortran
```
gfortran -std=legacy datcom.f -o datcom
``` 

### Running Stabsim
The process for running stabsim is currently being overhauled but the command-line interface should remain fairly stagnant. Examplesare provided in `examples/`. A sample is provided below for convenience
```
motor_dim = "data/H550_dim.csv"
motor_thrust = "data/H550_thrust.txt"
rocket = "data/Marvin.csv"
marvin_body = Rocket(os.path.join(script_dir, rocket))

H550 = load_motor(os.path.join(script_dir, motor_dim), os.path.join(script_dir, motor_thrust))
marvin = Profile(marvin_body, H550, 262, launch_altit=26000, length=25, timesteps=100)
vis.kinematics(marvin)
vis.spin(marvin)
```
As you can see, sample motors and airframe data is provided in the `data\` folder. To run stabsim on a new configuration you'll need to provide
1. Dimensons of the motor as a csv
2. Thrust curve of the motor as a txt
3. Dimensions of the airframe as a csv
4. Dimensions of the airframe as a dcm
Clearly this is a lot of data. The new GUI should make all of this a bit simpler but until then you'll have to bare with this.

End with an example of getting some data out of the system or using it for a little demo

## Built With
* [TKInter](https://docs.python.org/3/library/tkinter.html) - Python Interface to TK GUI toolkit
* [Digital DATCOM](http://www.pdas.com/datcomdownload.html) - by USAF via PDAD
* [NRMLSISE-00](https://github.com/DeepHorizons/Python-NRLMSISE-00) - atmospheric model

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
* The many many many folks who sweat and tears have gone into Spaceshot


