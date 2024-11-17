import cv2
import pandas as pd
from datetime import datetime

# Variables de configuración
first_frame = None
status_list = [0, 0]  # Lista para el estado anterior y el actual
times = []  # Lista para almacenar tiempos de cambio de estado

# Iniciar captura de video
video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    status = 0  # Inicializar el estado como 'sin movimiento'

    # Convertir a escala de grises y aplicar desenfoque
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Definir el primer cuadro de referencia
    if first_frame is None:
        first_frame = gray
        continue

    # Calcular la diferencia con el primer cuadro
    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Encontrar contornos en la imagen umbralizada
    (contours, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1  # Cambiar estado a 'movimiento detectado'
        
        # Dibujar un rectángulo alrededor del contorno detectado
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        
    status_list=status_list[-2:]

    # Registrar los cambios de estado
    if status_list[-1] == 0 and status == 1:
        times.append(datetime.now())
    elif status_list[-1] == 1 and status == 0:
        times.append(datetime.now())

    status_list.append(status)

    # Mostrar las ventanas de video
    cv2.imshow("Grabando", gray)
    cv2.imshow("Delta", delta_frame)
    cv2.imshow("Thresh", thresh_frame)
    cv2.imshow("Colores", frame)

    # Salir del bucle al presionar la tecla 'q'
    if cv2.waitKey(1) == ord('q'):
        if status == 1:
            times.append(datetime.now())  # Añadir tiempo final si el último estado fue de movimiento
        break

# Guardar los tiempos en el archivo CSV
df = pd.DataFrame([{"Start": times[i], "End": times[i + 1]} for i in range(0, len(times), 2)])
df.to_csv("App - Detectar obj/Datos.csv", index=False)

# Liberar recursos
video.release()
cv2.destroyAllWindows()
