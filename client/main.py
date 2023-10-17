import cv2
import socket
import struct
import zlib
import numpy as np

# Inicializa o soquete UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('0.0.0.0', 12345))

cv2.namedWindow("Vídeo Recebido", cv2.WINDOW_NORMAL)

while True:
    data, _ = udp_socket.recvfrom(65535)
    size = struct.unpack(">L", data[:4])[0]
    data = data[4:]

    if len(data) == size:
        frame = cv2.imdecode(zlib.decompress(data), 1)
        cv2.imshow("Vídeo Recebido", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
udp_socket.close()
