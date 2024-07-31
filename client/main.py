import socket
import threading
import pyaudio
import sys
import numpy as np


CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# host = "87.248.153.134"
HOST = "87.248.153.134"
THRESHOLD = 200
PORT = 5000
CHUNKS = 2048


def connect():
    try:
        CLIENT.connect((HOST, PORT))
        print("Connected")
    except Exception as e:
        print("Error connecting to the server:", e)
        sys.exit(1)


def send():
    while True:
        try:
            data = input_stream.read(CHUNKS)
            audio_data = np.frombuffer(data, dtype=np.int16)
            amplitude = np.abs(audio_data)
            if np.max(amplitude) > THRESHOLD:
                CLIENT.send(data)
        except Exception as e:
            print("Error sending data:", e)
            break


def receive():
    while True:
        try:
            data = CLIENT.recv(CHUNKS)
            output_stream.write(data)
        except Exception as e:
            print("Error receiving data:", e)
            break


if __name__ == "__main__":
    connect()
    p = pyaudio.PyAudio()
    Format = pyaudio.paInt16
    channels = 1 if sys.platform == "darwin" else 2
    rate = 46000
    

    input_stream = p.open(
        format=Format,
        channels=channels,
        rate=rate,
        input=True,
        frames_per_buffer=CHUNKS,
    )

    output_stream = p.open(
        format=Format,
        channels=channels,
        rate=rate,
        output=True,
        frames_per_buffer=CHUNKS,
    )

    t1 = threading.Thread(target=send)
    t2 = threading.Thread(target=receive)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    input_stream.stop_stream()
    input_stream.close()
    output_stream.stop_stream()
    output_stream.close()
    p.terminate()
