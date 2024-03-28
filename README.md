# ODrive Framework

pls note that this whole repository is still in progress. dont consider to use it by now

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/vmisslbeck/odrive_qdd/blob/main/LICENSE)

The odrive_qdd Interface is a powerful tool for configuring, controlling, and manipulating ODrive motor controllers and motors that are not directly interfaced with ODrive.

## Features

- **Configuration**: Easily configure ODrive motor controllers and motors.
- **Control**: Take full control of your motors with advanced control algorithms.
- **Manipulation**: Manipulate motors that are not natively supported by ODrive.

## Installation


1. Install the required dependencies:

    ```bash
    pip install odrive
    ```

## Usage

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

## Contributing

Contributions are welcome!

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or inquiries, please contact the project creator, vmisslbeck, at [raise.robotics@gmail.com](mailto:raise.robotics@gmail.com).