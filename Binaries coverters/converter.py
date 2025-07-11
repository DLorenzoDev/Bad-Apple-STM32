import cv2
import numpy as np

# Abrir video
cap = cv2.VideoCapture("input.mp4")

# Parámetros de destino
target_w, target_h = 128, 64
aspect_w, aspect_h = 4, 3

# Escalado proporcional (85x64)
new_w = 85
new_h = 64

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Escalar manteniendo aspecto
    resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Convertir a escala de grises
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # Umbral a blanco y negro (puedes ajustar 127)
    _, bw = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Agregar padding lateral
    padded = cv2.copyMakeBorder(bw, 0, 0, (target_w - new_w)//2, (target_w - new_w + 1)//2, cv2.BORDER_CONSTANT, value=0)

    # Guardar frame o convertir a bytes para STM32
    bw_bytes = np.packbits(padded, axis=1)
    # Aquí puedes escribir a archivo o buffer

cap.release()
