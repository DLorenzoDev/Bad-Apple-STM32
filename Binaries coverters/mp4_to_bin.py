import cv2
import numpy as np

# Parámetros
input_video = "Bad Apple!!.mp4"
output_bin = "BadApple.bin"

target_w, target_h = 128, 64
new_w, new_h = 85, 64  # ancho con aspect ratio conservado
frame_size_bytes = target_w * target_h // 8

cap = cv2.VideoCapture(input_video)
frames = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    padded = cv2.copyMakeBorder(
        bw,
        0, 0,
        (target_w - new_w) // 2,
        (target_w - new_w + 1) // 2,
        cv2.BORDER_CONSTANT,
        value=0
    )

    # Invertir color si es necesario (negro = 1, blanco = 0)
    padded = 255 - padded

    # Empaquetar 1 bit por píxel (cada fila → 16 bytes)
    packed = np.packbits(padded, axis=1)
    frame_data = packed.flatten()
    frames.append(frame_data)

cap.release()

# Escribir archivo binario crudo
with open(output_bin, "wb") as f:
    for frame in frames:
        f.write(frame.tobytes())
