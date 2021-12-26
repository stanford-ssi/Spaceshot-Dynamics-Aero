# Stabsim
Your one stop shop for finless spin-stabilized projectiles

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
Stabsim relies on Digital DATCOM to calculate aerodynamic coefficients. A compiled version of the fortran is provided but its unlikely to work for everyone's set up. If you experience issues with DATCOM
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
Stabsim can be used as either as a python library or as an graphical application.
#### Command line interface
Even as stabsim's gui changes the command-line interface should remain fairly stagnant. Examples are provided in `examples/`. A sample is provided below for convenience
```
motor_dim = "data/H550_dim.csv"
motor_thrust = "data/H550_thrust.txt"
rocket = "data/Marvin.csv"

marvin = Rocket.fromfile(os.path.join(script_dir, rocket))
h550 = Motor.fromfiles(os.path.join(script_dir, motor_dim), os.path.join(script_dir, motor_thrust))
baby_spacehot = Profile(marvin, h550, 262, launch_altit=26000, length=5,        timesteps=100)

vis.kinematics(baby_spacehot)
vis.spin(baby_spacehot)
```
As you can see, sample motors and airframe data is provided in the `data\` folder. To run stabsim on a new configuration you'll need to provide information about the motor and the airframe. Motor information can be loaded using
1. the industry standard RASP file format
2. a csv with motor file specification
3. raw numerical values
4. any combination thereof

Airframe information can be loaded using
1. a csv file with airframe specifications
2. a DATCOM file with airframe specifications
3. some combination thereof
For examples of how to format .csv files again refer to the `data\` folder.
#### Graphical user interface
Clearly this is a lot of data. The graphical application makes it all a bit easier to manage. You can either load information using these file formats or manually input your vehicles specifications. Be warned that the GUI does abstract away a few features that are more readily accessible via the CLI.
![Stabsim at Startup](/assets/startup.PNG)
![Spaceshot](/assets/spaceshot.PNG)
![Baby Spaceshot](/assets/baby_spaceshot.PNG)

## Built With
* [TKInter](https://docs.python.org/3/library/tkinter.html) - Python Interface to TK GUI toolkit
* [Sun Valley](https://github.com/rdbende/Sun-Valley-ttk-theme) - A stunning theme for ttk based on Microsoft's Sun Valley visual style
* [Digital DATCOM](http://www.pdas.com/datcomdownload.html) - by USAF via PDAD
* [NRMLSISE-00](https://github.com/DeepHorizons/Python-NRLMSISE-00) - atmospheric model

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
_The many many many folks whose sweat and tears have gone into Spaceshot_


