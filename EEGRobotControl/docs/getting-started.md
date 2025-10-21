# EEG-Robot-Control
This project uses real-time EEG signals to control a robot based on the user's state of alertness.
 
- **Alert (eyes open)** → Robot moves forward  
- **Rest (eyes closed)** → Robot stops  

During the eyes-closed, resting state, EEG exhibits stable, large amplitude alpha waves. Contrastingly, in the eyes-open, active state, low amplitude alpha waves are detected. By analyzing wave amplitude in the **8–12 Hz (alpha) band**, the system distinguishes between alert and resting states and translates them into motor commands for the robot.

---

## How It Works

**EEG Signal Acquisition**  

   - Raw EEG Data is collected via stick on EEG-Electrodes
   - The BioAmp EXG Pill eliminates noise and amplifies the EEG signal by 1000x
   - The Arduino Uno captures the amplifed EEG signal and relays it to the `serial-read-alpha.py` script

**Signal Processing**  

   - `serial-read-alpha.py` filters EEG for alpha activity  
   - Root Mean Square(RMS) calculations are applied to detemine the aplitude of the alpha waves 
   - The amplitude is comapred to high and low thresholds. If the amplitude meets or exceeds these, the eyes closed state is detected. Else, the eyes open state is detected. 
   - If the eyes-closed state si detected, the script writes `stop` to a motor command file. Else, it writes `go` . 

**Robot Control** 

   - `mbot-motor-control.py` configures the motors and defines the `stop_motors` and `move_forward` functions 
   - The script reads the motor command file and sends the appropriate motor commands to the robot (mBot) via serial  



**System Requirements**

- Python 3.x  
- NumPy, SciPy  
- See Hardware section for complete materials list

---

## Getting Started

1. Setup the EEG system and build the M-Bot. 
2. Follow the electronics schematics or tutorial video to setup the complete system. 
2. Run `serial-read-alpha.py` to begin capturing EEG and writing `stop`/`go`commands.  
3. In a separate terminal, run `mbot-motor-control.py` to control robot motors.  
4. Close your eyes → robot **stops**.  
5. Stay alert (eyes open) → robot **moves**.  

---


