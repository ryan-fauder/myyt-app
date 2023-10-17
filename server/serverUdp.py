import socketserver
import socket
import cv2
import pickle
import struct
import imutils

class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print("Conexão de cliente recebida de", self.client_address)
        
        with open('C:/Users/Randy/Downloads/Aulas/8 Periodo/Sistemas Distribuidos/myyt-app/server/storage/Parte 1 - Iniciando um Projeto em Cloud.mp4', 'rb') as video_file:
            while True:
                clientsocket, address = self.request
                data = video_file.read(1024)
                if not data:
                    break
                clientsocket.sendto(data, self.client_address)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        print("Servidor iniciou")
        server.serve_forever()