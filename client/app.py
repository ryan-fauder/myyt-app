from flask import Flask, render_template, request, redirect, url_for,Response
import socket
import io
from moviepy.editor import VideoFileClip


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload():
    file = request.files['file']
    file_name = file.filename
    print(file_name)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("172.16.41.123", 9999))
    client.send(f"UPLOAD {file_name}".encode())
    #file_size = file.seek(0, os.SEEK_END)
    #client.send(str(file_size).encode())

    data = file.read()
    client.sendall(data)
    client.send(b"<END>")

    client.close()

    return "File uploaded successfully! You can now upload another file."


@app.route('/stream')
def stream():
    video_name = request.args.get('id');
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("172.16.41.123", 9999))
    client.send(f"STREAM {video_name}".encode())  # Use the "STREAM" request format
    
    def generate():
        chunk_size = 1024  # Tamanho dos pedaços em bytes
        while True:
            data = client.recv(chunk_size)
            if not data:
                break
            yield data
    client.close()
    return Response(generate(), content_type='video/mp4')

@app.route('/stream_video')
def stream_video():
    video_name = 'loginfailed.mp4'  # Substitua pelo caminho real do seu vídeo

    def generate():
        chunk_size = 1024  # Tamanho dos pedaços em bytes
        with open(video_name, 'rb') as video_file:
            while True:
                chunk = video_file.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    return Response(generate(), content_type='video/mp4')


@app.route('/streaming/<name>')
def streaming():
    video_name = request.form['video_name']
    print(request.args)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("172.16.41.123", 9999))

    client.send(f"STREAM {video_name}".encode())  # Use the "STREAM" request format

    response = b''
    while True:
        data = client.recv(1024)
        if not data:
            break
        response += data

    video_data = response

    with io.BytesIO(video_data) as video_file:
        with open('video.mp4', 'wb') as output_file:
            output_file.write(video_file.read())

    if response == b'File not found':
        client.close()
        return render_template('index.html', video_src=None)

    # Carregue o arquivo de vídeo
    video = VideoFileClip('video.mp4')  # Substitua pelo nome do seu vídeo

    # Reproduza o vídeo com áudio
    video.preview()

    # Feche a janela de visualização após a reprodução
    video.close()
    client.close()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
