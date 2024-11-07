import socket
import threading

# List to keep track of all connected clients
clients = []

# Function to broadcast a message to all clients except the sender
def broadcast(sender, msg):
    for client in clients:
        if client != sender:
            try:
                client.send(msg)
            except:
                print("Error sending message to a client.")

# Function to handle each client connection
def handle_client(client, addr):
    print(f"New connection from {addr}")
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                break  # Exit if the client has disconnected
            broadcast(client, msg)
        except:
            print(f"Error with client {addr}")
            break
    
    print(f"Client {addr} disconnected.")
    clients.remove(client)
    client.close()

# Setting up the server
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind(('localhost', 5000))
server_sock.listen()

print("Server is listening for connections...")

while True:
    client, addr = server_sock.accept()
    clients.append(client)
    threading.Thread(target=handle_client, args=(client, addr)).start()