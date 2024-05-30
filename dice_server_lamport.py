import socket
import threading
import time
import random
import argparse

DAUER_DER_RUNDE = 3
number_of_rounds = 5
HOST = '192.168.2.131'
PORT = 5000
BUFFER_ROUND = 1024
events = []
LC = 0

clients = []
results = []
events = []

def local_event(event):
    LC = LC+1
    return (event,LC)

def serve_client(client_socket,client_address):
    global results
    global roundNumber
    global events
    global LC
    try:
        while True:
            message = client_socket.recv(BUFFER_ROUND).decode()
            if message:
                name, wurf, CC = message.split(':')
                CC = int(CC)
                LC = (max(LC,CC))+1
                events.append(((name,wurf),CC))
                wurf = int(wurf)
                results[roundNumber].append((name,wurf))
                print(f"{name} würfelte {wurf}")
    except ConnectionResetError:
        print(f"[ERROR] Verbindung zu {client_address} verloren")
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST,PORT))
    server.listen(5)
    print(f"[INFO] Server läuft auf {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        clients.append(client_socket)
        print(f"[INFO] Verbindung von {client_address} akzeptiert")
        client_handler = threading.Thread(target=serve_client, args=(client_socket, client_address))
        client_handler.start()

def start_round():
    global results
    global roundNumber
    global events
    global LC
    results.append([])
    print(f"[INFO] Runde {roundNumber} gestartet")
    LC = LC+1
    events.append(("START",LC))
    for client in clients:
        client.send(f"START:{LC}".encode())   
    time.sleep(DAUER_DER_RUNDE)
    LC = LC+1
    for client in clients:
        client.send(f"STOP:{LC}".encode())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Würfelspiel Server")
    parser.add_argument("--ddr", type=int, default=DAUER_DER_RUNDE, help="Dauer der Runde in Sekunden")
    args = parser.parse_args()
    DAUER_DER_RUNDE = args.ddr

    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    #global roundNumber
    roundNumber=0
    input("Drücke Enter, um das Spiel zu starten")
    for i in range(0,number_of_rounds):
        roundNumber=i
        start_round()

    time.sleep(5)
    print(f"[INFO] Ergebnisse der {number_of_rounds} Runden:")
    events.sort(key=lambda tup: tup[1])
    print(events)
