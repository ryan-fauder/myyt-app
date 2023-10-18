import socket
import os
import mimetypes
import time

# Defina o endereço e a porta do servidor
host = '127.0.0.1'  # Substitua pelo endereço do servidor
port = 8080

def detect_mimetype(filename):
    # Detecta o tipo MIME do arquivo com base na extensão do arquivo
    return mimetypes.guess_type(filename)[0]

def serve_file(client, filename):
    try:
        with open(filename, 'rb') as file:
            while True:
                chunk = file.read(1024)
                if not chunk:
                    break
                client.send(chunk)
                time.sleep(0.01)  # Pequeno atraso para controlar a taxa de envio
    except Exception as e:
        print(f"Erro ao enviar arquivo: {e}")

def handle_request(client, address):
    request = client.recv(1024)
    print(request)
    # request = request.decode('utf-8')
    parts = request.split(b'\r\n\r\n')
    header = parts[0]
    if(len(parts) > 1 and parts[1] != b''):
        content_body = parts[2]
    header_parts = header.split()    
    if len(header_parts) > 1 and header_parts[0] == b'GET':
        filename = header_parts[1].lstrip('/')

        if os.path.exists(filename):
            mimetype = detect_mimetype(filename)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: {mimetype}\r\n\r\n"
            client.send(response.encode('utf-8'))

            serve_file(client, filename)
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\nArquivo não encontrado."
            client.send(response.encode('utf-8'))
    if len(header_parts) > 1 and header_parts[0] == b'POST':
        print('POSTTT')
        with open('video_saved.mp4', 'wb') as video:
            print('ok')
            video.write(content_body)

    client.close()

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"Servidor socket em execução em {host}:{port}")

    while True:
        client, address = server.accept()
        print(f"Conexão de {address[0]}:{address[1]}")

        # Lide com a solicitação em uma nova thread para lidar com várias conexões
        handle_request(client, address)
