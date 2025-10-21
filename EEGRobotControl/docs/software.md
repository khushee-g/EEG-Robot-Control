# Software Setup


## `serial-read-theta.py` – EEG Signal Processing

This program reads real-time EEG data from the Arduino/EXG setup, filters for theta band activity (4–8 Hz), and writes motor commands (`go` / `stop`) to a file for the robot to read. ⚠️ Important:** Change the `serial_port` variable to match your Arduino’s port on your computer.

### Full Code

    import serial
    import time
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.signal import butter, lfilter
    from collections import deque

    sampling_rate = 256
    sampling_interval = 1.0 / sampling_rate
    window_size = 2048

    lowcut = 8.0
    highcut = 12.0

    serial_port = "/dev/cu.usbmodem142401"  # Change to your port
    baudrate = 115200
    timeout = 1

    AMPLITUDE_THRESHOLD_LOW = 8.4  # adjust to calibrate against your own brain
    AMPLITUDE_THRESHOLD_HIGH = 8.7

    def butter_bandpass(lowcut, highcut, fs, order=4):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        return butter(order, [low, high], btype='band')

    def apply_filter(data, lowcut, highcut, fs):
        b, a = butter_bandpass(lowcut, highcut, fs)
        return lfilter(b, a, data)

    try:
        ser = serial.Serial(serial_port, baudrate, timeout=timeout)
        print(f"Connected to serial port: {serial_port}")
    except Exception as e:
        print(f"Could not open serial port: {e}")
        exit(1)

    data_buffer = deque(maxlen=window_size)
    last_command_time = time.time()

    plt.ion()
    fig, ax = plt.subplots()
    x_vals = []
    y_vals = []
    line, = ax.plot([], [], lw=2)
    ax.set_xlim(0, 60)
    ax.set_ylim(8, 9)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Alpha Amplitude (RMS)")
    ax.set_title("Real-Time Alpha Oscillation Amplitude")
    fig.tight_layout()

    start_plot_time = time.time()



    try:
        while True:
            line_data = ser.readline().decode("utf-8", errors="replace").strip()
            if not line_data:
                continue

            try:
                eeg_value = float(line_data.split(',')[0])
            except (ValueError, IndexError):
                continue

            data_buffer.append(eeg_value)

            if len(data_buffer) == window_size:
                raw_data = np.array(data_buffer)
                filtered = apply_filter(raw_data, lowcut, highcut, sampling_rate)

                # Use RMS as amplitude measure
                alpha_amplitude = np.sqrt(np.mean(filtered**2))

                # Determine command
                if alpha_amplitude < AMPLITUDE_THRESHOLD_LOW or alpha_amplitude > AMPLITUDE_THRESHOLD_HIGH:
                    command = "stop"
                    print(f"🛑 STOP | Alpha amplitude: {alpha_amplitude:.1f}")
                else:
                    command = "go"
                    print(f"✅ GO | Alpha amplitude: {alpha_amplitude:.1f}")

                with open("motor_command.txt", "w") as f:
                    f.write(command)



                current_time = time.time() - start_plot_time
                x_vals.append(current_time)
                y_vals.append(alpha_amplitude)

                if x_vals[-1] > 60:
                    x_vals = [t for t in x_vals if t >= x_vals[-1] - 60]
                    y_vals = y_vals[-len(x_vals):]
                    ax.set_xlim(x_vals[0], x_vals[-1])

                line.set_data(x_vals, y_vals)

                
                plt.pause(0.001)

            time.sleep(sampling_interval)

    except KeyboardInterrupt:
        print("Program stopped by user.")

    finally:
        ser.close()
        print("Serial port closed.")



---

## `mbot-motor-control.py` – Robot Control
This program reads the motor_command.txt file and sends corresponding motor commands to the mBot via serial.
⚠️ Important: Update serial_port to match your mBot’s connection.

### Full Code
    import serial
    import time


    serial_port = "/dev/tty.usbserial-14230"  # Change this to your port
    baudrate = 115200

    try:
        mbot = serial.Serial(serial_port, baudrate, timeout=1)
        print(f"Connected to mBot on {serial_port}")
    except Exception as e:
        print(f"Error opening serial port: {e}")
        exit(1)



    def run_motor(port, speed):
        """
        port: 0x09 = left motor, 0x0A = right motor
        speed: -255 to 255
        """
        speed_bytes = speed.to_bytes(2, byteorder='little', signed=True)

        packet = bytearray([
            0xFF, 0x55,    
            0x07,          
            0x00,          
            0x02,          
            0x0A,          
            port,          
            speed_bytes[0],
            speed_bytes[1]
        ])

        checksum = sum(packet[2:]) % 256
        packet.append(checksum)

        mbot.write(packet)

        print(f"Sent to port {hex(port)}: {list(packet)} (speed {speed})")

    def move_forward():
        run_motor(0x09, 100)  
        run_motor(0x0A, -100)  

    def stop_motors():
        run_motor(0x09, 0)  
        run_motor(0x0A, 0)  





    last_command = None

    try:
        while True:
            try:
                with open("motor_command.txt", "r") as f:
                    command = f.read().strip().lower()
            except FileNotFoundError:
                command = None

            if command in ["go", "stop"]:
                if command == "go":
                    move_forward()
                    print("✅ GO → Moving forward")
                elif command == "stop":
                    stop_motors()
                    print("🛑 STOP → Motors stopped")
                    time.sleep(1)
                last_command = command
                
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nProgram interrupted! Stopping motors...")
        stop_motors()
        mbot.close()

