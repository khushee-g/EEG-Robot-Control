# EEG-Robot-Control

**EEG-Robot Control** is a project that uses real-time EEG signals to control a robot based on the user's state of alertness.

---

## How It Works

### User States

- **Alert (eyes open)** → Robot moves forward  
- **Rest (eyes closed / theta detected)** → Robot stops  

By filtering EEG data in the **4–8 Hz (theta) band**, the system distinguishes between alert and resting states and translates them into motor commands for the robot.

---

### EEG Signal Acquisition

- 3 gel electrodes (stick-on)  
- EXG Pill amplifier  
- Arduino Uno for data capture  

---

### Signal Processing

- `serial-read-theta.py` filters EEG for 4–8 Hz activity  
- If **theta detected**, writes `stop` to a motor command file  
- Else, writes `go`  

---

### Robot Control

- `mbot-motor-control.py` reads the command file  
- Sends the appropriate motor commands to the robot (**mBot**) via serial  

---

## Requirements

- Python 3.x  
- NumPy, SciPy  
- Arduino Uno + EXG Pill  
- mBot (MakerBlock)  
- EEG electrodes (3 gel stick-on)  

---

## Getting Started

1. Run `serial-read-theta.py` to begin capturing EEG and writing commands.  
2. In a separate terminal, run `mbot-motor-control.py` to control robot motors.  
3. **Close your eyes** → robot stops  
4. **Stay alert (eyes open)** → robot moves  

---


