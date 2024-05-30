import socket
import threading
import time
import random
import argparse

HOST = '192.168.2.131'
PORT = 5000
BUFFER_SIZE = 1024
SPIELER_LATENZ = 5

def play_game(name,latency):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((HOST,PORT))

    try:
        while True:
            message = client.recv(BUFFER_SIZE).decode()
            if message == "START":
                delay = random.uniform(0,latency)
                time.sleep(delay)
                wurf = random.randint(1,100)
                client.send(f"{name}:{wurf}".encode())
                print(f"[INFO] {client} würfelte {wurf}")
            elif message == "STOP":
                print(f"[INFO] {name} wartet auf die nächste Runde")
    except ConnectionResetError:
        print(f"[ERROR] Verbindung zum Server Verloren")
    finally:
        client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Würfelspiel Client")
    parser.add_argument("--name", type=str, required=True, help="Name des Spielers")
    parser.add_argument("--latency", type=int, default=SPIELER_LATENZ)
    args = parser.parse_args()

    server_thread = threading.Thread(target=play_game, args=(args.name,args.latency))
    server_thread.start()
