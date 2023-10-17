import cv2
import socket
import struct
import zlib

# Inicializa o soquete UDP
server_address = ('127.0.0.1', 5000)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Abre o arquivo de vídeo com OpenCV
cap = cv2.VideoCapture('C:/Users/Randy/Downloads/Aulas/8 Periodo/Sistemas Distribuidos/myyt-app/server/storage/video.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Compacta o quadro antes de enviar
    _, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    data = zlib.compress(buffer, zlib.Z_BEST_COMPRESSION)

    # Envie o tamanho do quadro primeiro
    size = struct.pack(">L", len(data))
    udp_socket.sendto(size, server_address)

    # Em seguida, envie o quadro comprimido
    udp_socket.sendto(data, server_address)

udp_socket.close()
