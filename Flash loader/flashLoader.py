import serial
import sys
import time

COM_PORT = 'COM3'
BAUD = 921600
file_path = "BadApple.bin"

def print_progress(progress, total, step):
    bar_len = 40  # ancho barra
    filled_len = int(round(bar_len * progress / float(total)))

    bar = "█" * filled_len + "-" * (bar_len - filled_len)
    percent = round(100.0 * progress / float(total), 1)

    sys.stdout.write(f"\r[{bar}] {percent}%")
    sys.stdout.flush()

ser = serial.Serial(COM_PORT, BAUD)
with open(file_path, "rb") as f:
    data = f.read()

# Mandar tamaño del archivo
ser.write(len(data).to_bytes(4, 'little'))

chunk_size = 256
total_chunks = (len(data) + chunk_size - 1) // chunk_size
step = 0

for i in range(0, len(data), chunk_size):
    chunk = data[i:i+chunk_size]
    ser.write(chunk)
    ack = ser.read(1)
    if ack != b'\x01':
        print(f"\nError en chunk {i//chunk_size}")
        break

    step += 1
    print_progress(step, total_chunks, step)

ser.close()
print("\nFlash completada")
