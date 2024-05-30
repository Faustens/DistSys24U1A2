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

clients = []
results = []
#roundNumber=0

def serve_client(client_socket,client_address):
    global results
    global roundNumber
    try:
        while True:
            message = client_socket.recv(BUFFER_ROUND).decode()
            if message:
                name, wurf = message.split(':')
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
    results.append([])
    print(f"[INFO] Runde {roundNumber} gestartet")
    for client in clients:
        client.send("START".encode())    
    time.sleep(DAUER_DER_RUNDE)
    for client in clients:
        client.send("STOP".encode())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Würfelspiel Server")
    parser.add_argument("--ddr", type=int, default=DAUER_DER_RUNDE, help="Dauer der Runde in Sekunden")
    args = parser.parse_args()
    DAUER_DER_RUNDE = args.ddr

    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    global roundNumber
    roundNumber=0
    input("Drücke Enter, um das Spiel zu starten")
    for i in range(0,number_of_rounds):
        roundNumber=i
        start_round()
    print(f"[INFO] Ergebnisse der {number_of_rounds} Runden:")
    for i in range(0,number_of_rounds):
        print(f"    Runde {i}:")
        results[i].sort(key=lambda entry: entry[0])
        for entry in results[i]:
            print(f"        {entry[0]}:{entry[1]}")
            
    print(f"[INFO] Spiel Vorbei")




    
