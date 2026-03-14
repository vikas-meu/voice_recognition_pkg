# Voice Recognition Navigation ROS2 Package

ROS2 package that enables **voice controlled robot navigation** using an **Arduino Nano** and **DFRobot Offline Voice Recognition Module**.

The system listens for predefined voice commands and sends them to a ROS2 node through **serial communication**. The ROS2 node then converts the command into navigation goals for the robot.

This package was designed for **autonomous robot control using voice commands** and can easily be integrated with **Nav2 navigation stack**.

---

## Features

* Offline voice recognition (no internet required)
* Serial communication between Arduino and ROS2
* Voice commands mapped to navigation goals
* Works with ROS2 Navigation Stack (Nav2)
* Designed for Raspberry Pi / Ubuntu robots
* Easy to integrate into existing ROS2 workspaces

---

## Hardware Used

* Arduino Nano
* DFRobot Offline Voice Recognition Module
* Raspberry Pi (or Ubuntu PC running ROS2)
* Differential Drive Robot Base
* Motor driver (ex: L298N)
* Encoders (optional for odometry)

---

## System Architecture

Voice Command
↓
DFRobot Voice Recognition Module
↓
Arduino Nano processes command
↓
Serial communication to ROS2 node
↓
ROS2 node sends goal to Nav2
↓
Robot navigates to location

---

## ROS2 Workspace Setup

Clone this package inside your ROS2 workspace.

```bash
cd ~/ros2_ws/src
git clone https://github.com/YOUR_USERNAME/voice_recognition_pkg.git
```

Build the workspace:

```bash
cd ~/ros2_ws
colcon build
```

Source the workspace:

```bash
source install/setup.bash
```

---

## Running the Package

Run the voice recognition node:

```bash
ros2 run voice_recognition_pkg serial_goal_sender
```

Make sure:

* Arduino is connected via USB
* Serial port matches the one used in the node
* Nav2 stack is running

---

## Example Voice Commands

Example commands that can be configured:

* "Kitchen"
* "Bedroom"
* "Hall"
* "Stop"
* "Return Home"

Each command corresponds to a **predefined navigation goal**.

---

## Arduino Side

The Arduino reads the command ID from the **DFRobot Voice Recognition Module** and sends it over serial to the ROS2 system.

Example serial output:

```
CMD:1
CMD:2
CMD:3
```

The ROS2 node interprets these IDs and converts them into navigation goals.

---

## Package Structure

```
voice_recognition_pkg
│
├── src
│   └── serial_goal_sender.py
│
├── launch
│
├── package.xml
├── setup.py
└── README.md
```

---

## Applications

* Voice controlled service robots
* Home automation robots
* Assistive robotics
* Autonomous indoor navigation
* Robotics research and education

---

## License

This project is licensed under the **MIT License**.

You are free to use, modify, and distribute this software as long as proper credit is given.

---

## Author

Vikas Singh Thakur

GitHub: https://github.com/vikas-meu

---

## Contribution

Contributions are welcome.
If you improve the package or add new features, feel free to open a **pull request**.
