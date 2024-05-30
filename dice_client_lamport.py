import socket
import threading
import time
import random
import argparse

HOST = '192.168.2.131'
PORT = 5000
BUFFER_SIZE = 1024
SPIELER_LATENZ = 5
event_queue = []
LC = 0
client = None
connection = True

def listen():
    global LC
    global client
    global event_queue
    
    try:
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((HOST,PORT))
        while True:
            message = client.recv(BUFFER_SIZE).decode()
            event, SC = message.split(':')
            SC = int(SC)
            event_queue.append((event,SC))
            LC = max(LC,SC)+1
    except ConnectionResetError:
        print(f"[ERROR] Verbindung zum Server Verloren")
    finally:
        connection = False
        client.close()

def handle_event_queue(name,latency):
    #try:
    global event_queue
    while connection:
        if event_queue:
            event = event_queue.pop(0)
            play_game(event,name,latency)
    #except:
    #   print(f"[ERROR] Fehler in handle_event_queue")

def play_game(event,name,latency):
    global LC
    global client     
    if event[0] == "START":
        delay = random.uniform(0,latency)
        time.sleep(delay)
        wurf = random.randint(1,100)
        CC = event[1]+1
        client.send(f"{name}:{wurf}:{CC}".encode())
        print(f"[INFO] {client} würfelte {wurf}")
    elif event[0] == "STOP":
        print(f"[INFO] {name} wartet auf die nächste Runde")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Würfelspiel Client")
    parser.add_argument("--name", type=str, required=True, help="Name des Spielers")
    parser.add_argument("--latency", type=int, default=SPIELER_LATENZ)
    args = parser.parse_args()

    connection_handler = threading.Thread(target=listen, args=())
    event_handler = threading.Thread(target=handle_event_queue, args=(args.name,args.latency))
    
    connection_handler.start()
    event_handler.start()
