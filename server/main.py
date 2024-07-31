import socket
import threading
import wave

PORT = 5000
HOST = "0.0.0.0"
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((HOST, PORT))
SERVER.listen(5)

print(f"server listening on {HOST}:{PORT}")

CLIENTS = []


def start():
    try:
        while True:
            conn, addr = SERVER.accept()
            CLIENTS.append(conn)
            t = threading.Thread(target=send, args=(conn,))
            t.start()
    except Exception as e:
        print("Error accepting connection:", e)


def broadcast(conn,data):
    for cl in CLIENTS:
        if cl != conn:
            cl.send(data)


def send(from_connection):
    try:
        while True:
            data = from_connection.recv(4096)
            broadcast(from_connection,data)
    except Exception as e:
        print("Client Disconnected", e)
    finally:
        print(f"Closing connection ...")
        from_connection.close()
        if from_connection in CLIENTS:
            CLIENTS.remove(from_connection)

        with wave.open("byebye.wav", "rb") as wf:
            while len(data := wf.readframes(1024)):
                broadcast(from_connection,data)


if __name__ == "__main__":
    start()
