import cv2
import pyaudio
import wave
import numpy
import ffmpeg

file_path = 'C:/Users/Randy/Downloads/Aulas/8 Periodo/Sistemas Distribuidos/myyt-app/server/storage/video.mp4'

p = pyaudio.PyAudio()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

client_stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)
server_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
audio  = ffmpeg.input(file_path).audio

video = cv2.VideoCapture(file_path)
fps = video.get(cv2.CAP_PROP_FPS)
sleep_ms = int(numpy.round((1/fps)*1000))

# Verifique se o vídeo foi aberto corretamente
if not video.isOpened():
    print("Erro ao abrir o vídeo.")
    exit()

while True:
    # Leia o próximo frame do vídeo
    ret, frame = video.read()
    audio_frame = wave_file.readframes(CHUNK)
    # Verifique se a leitura do frame foi bem-sucedida
    if not ret:
        print("Fim do vídeo.")
        break
    # Exiba o frame
    cv2.imshow('Player de Vídeo', frame)
    client_stream.write(audio_frame)

    # Aguarde um curto período de tempo entre os frames (por exemplo, 25 milissegundos)

    if cv2.waitKey(sleep_ms) & 0xFF == ord('q'):
        break
client_stream.stop_stream()
client_stream.close()
video.release()
cv2.destroyAllWindows()