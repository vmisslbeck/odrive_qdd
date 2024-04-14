# ODrive Framework

pls note that this whole repository is still in progress. dont consider to use it by now, unless you like the unknown 

[![License](https://img.shields.io/badge/license-GPL_3.0-blue.svg)](https://github.com/vmisslbeck/odrive_qdd/blob/main/LICENSE)

The odrive_qdd Interface is a powerful tool for configuring, controlling, and manipulating ODrive motor controllers and motors that are not directly interfaced with ODrive.

## Features

- **Configuration**: Easily configure ODrive motor controllers and motors.
- **Control**: Take full control of your motors with advanced control algorithms.
- **Manipulation**: Manipulate motors that are not natively supported by ODrive.

## Getting Started

### Installs
1. Install the required dependencies:

    ```bash
    pip install odrive
    pip install pynput
    ```

### Usage

For quick start, plug in the USB-C cable to your odrive (which is already configured & calibrated, if not continue reading),
then connect your odrive to power connection and now you can
run the src/odrive_usb_demo.py
with 
```python
cd path/to/your/directory/odrive_qdd
python src/odrive_usb_demo
```
It will first ask you to control the motor velocity with your keyboard, then if you are ready and quit the input mode (press 'q')
it will jump into a sine wave movement.


To use the ODrive Framework, follow these steps:

1. Import the necessary modules:

    ```python
    import odrive
    import odrive_qdd
    ```

2. Initialize the ODrive controller:

    ```python
    odrv = odrive.find_any()
    ```

3. Configure and control your motors using the provided functions and APIs.

### Configuration

If you are very new to Odrive, I recommend to connect the odrive first of all to your computer
and get familiar with the [Odrive GUI](https://gui.odriverobotics.com/configuration). 
There you can configure your Odrive for your motor. Feel free to reach out to us if you are having trouble finding the right config settings.

But if you want a python tool for this you can also use this Framework. 
With odrv_con_and_calib.py module you can configure and calibrate your odrive

### Calibration
Calibration is very important, so be sure to have your odrive calibrated, 
also possible with 
```python
import odrv_con_and_calib
```


## Contributing

Contributions are welcome!

## License

This project is licensed under the [GPL-3.0 license](LICENSE).

## Contact

For any questions or inquiries, please contact the project creator, vmisslbeck, at [raise.robotics@gmail.com](mailto:raise.robotics@gmail.com).