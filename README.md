# EEG-Robot-Control
EEG-Robot Control: A project using real-time EEG signals to control a robot based on the user's state of alertness.
 
- **Alert (eyes open)** → Robot moves forward  
- **Rest (eyes closed / theta detected)** → Robot stops  

By filtering EEG data in the **4–8 Hz (theta) band**, the system distinguishes between alert and resting states and translates them into motor commands for the robot.

---

## How It Works

1. **EEG Signal Acquisition**  
   - 3 gel electrodes (stick-on)  
   - EXG Pill amplifier  
   - Arduino Uno for data capture  

2. **Signal Processing**  
   - `serial-read-theta.py` filters EEG for 4–8 Hz activity  
   - If **theta detected**, writes `stop` to a motor command file  
   - Else, writes `go`  

3. **Robot Control**  
   - `mbot-motor-control.py` reads the command file  
   - Sends the appropriate motor commands to the robot (mBot) via serial  

---

## Repository Structure

