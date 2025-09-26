# Hardware Setup

Materials: 
- Gel Electrodes(3 per use)
- 3 Snap-fit Wires
- BioAmp EXG Pill by Upside Down Labs
- 3 Male-Female Jumper Wires
- Arduino Uno
- 2 USB Type-B Cables


To set up the EEG system, start by connecting the electrode to the snap fit cables, and connect the free ends to the Bioamp EXG pill. I used red, black, and yellow cables to represent IN+, IN-, and REF respectively. Next, connect the BioAmp EXG Pill to the Arduino Uno board using the male-female jumper wires. Connect the yellow wire from the output pin to the A0 Analog Input port on the Arduino; connect the black wire from the ground pin to the ground port on the Arduino; and connect the red wire from the VCC(power) pin to the 5V port. See Diagram 1 for the complete connection setup. 
![Complete Connection Setup](EEG-Hardware.png)

Now connect the USB cable from the arduino board to your computer, so that the EEG signal can be processed. Connect the second USB cable from your computer to the M-Bot, in order to send the robot real-time motor commands based on the EEG input. Alternatively, you can connect to the M-Bot via bluetooth.
![Hardware Setup](hardware-setup.png)
