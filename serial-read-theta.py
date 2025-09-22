import serial
import time
import numpy as np
import csv
from scipy.signal import butter, lfilter
from scipy.fft import fft, fftfreq
from collections import deque
from datetime import datetime

sampling_rate = 256   
sampling_interval = 1.0 / sampling_rate
window_size = 256     
lowcut = 4.0          
highcut = 8.0        

serial_port = "/dev/cu.usbmodem1422401"  # Note: Change this to your serial port
baudrate = 115200
timeout = 1 

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


with open("motor_command.txt", "w") as f:
    f.write("")  

try:
    while True:
        start_time = time.time()

        line = ser.readline().decode("utf-8", errors="replace").strip()
        if not line:
            continue

        try:
            parts = line.split(',')
            if parts:
                eeg_value = float(parts[0])
            else:
                continue
        except (ValueError, IndexError):
            continue

        data_buffer.append(eeg_value)

        if len(data_buffer) == window_size:
            raw_data = np.array(data_buffer)
            filtered = apply_filter(raw_data, lowcut, highcut, sampling_rate)

            yf = np.abs(fft(filtered))
            freqs = fftfreq(window_size, d=sampling_interval)

            yf = yf[:window_size // 2]
            freqs = freqs[:window_size // 2]

            dominant_freq = freqs[np.argmax(yf)]


            if 4 <= dominant_freq <= 8:
                command = "go"
                print(f"🛑 STOP | Dominant freq: {dominant_freq:.2f} Hz")
            else:
                command = "stop"
                print(f"✅ GO | Dominant freq: {dominant_freq:.2f} Hz")

            with open("motor_command.txt", "w") as f:
                f.write(command)

            timestamp = datetime.now().isoformat()
            csv_writer.writerow([timestamp, eeg_value, f"{dominant_freq:.2f}", command])
            csv_file.flush()

        elapsed = time.time() - start_time
        time.sleep(max(0, sampling_interval - elapsed))

except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    csv_file.close()
    if ser.is_open:
        ser.close()
    print("Serial port and file closed.")

