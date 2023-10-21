from flask import Flask, render_template, request, redirect, url_for,Response
import socket
import io
import time

HOST = "127.0.0.1"
PORT = 8080

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_name = file.filename
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    header = f"UPLOAD {file_name} "
    header_formatted = f"{header: <1024}"
    print(header_formatted)
    client.send(header_formatted.encode())
    #file_size = file.seek(0, os.SEEK_END)
    #client.send(str(file_size).encode())
    data = file.read()
    client.sendall(data)
    client.send(b"<END>")
    client.close()
    return "File uploaded successfully! You can now upload another file."


@app.route('/stream')
def stream():
    video_name = request.args.get('id')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    header = f"STREAM {video_name} "
    client.send(f"{header: <1024}".encode())  # Use the "STREAM" request format
    
    def generate(client):
        chunk_size = 4096  # Tamanho dos pedaços em bytes
        while True:
            data = client.recv(chunk_size)
            if not data:
                break
            yield data
            # time.sleep(0.01)  # Pequeno atraso para controlar a taxa de envio
        client.close()
    return Response(generate(client), content_type='video/mp4')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
