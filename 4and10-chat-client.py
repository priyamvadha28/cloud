import socket
import threading

def recv_msg(client_sock):
    while True:
        try:
            msg = client_sock.recv(1024).decode('UTF-8')
            if msg:
                print('\n' + msg)
            else:
                break
        except:
            print("Error receiving message from server.")
            break

def send_messa(client_sock):
    name = input('Enter your name: ')
    print("Type 'exit' to leave the chat.")
    
    while True:
        msg = input('Enter the message: ')
        
        if msg.lower() == "exit":
            print("Exiting chat...")
            client_sock.close()  # Close the connection
            break
        
        full_msg = f"{name}: {msg}"
        client_sock.send(full_msg.encode('UTF-8'))

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('localhost', 5000))

# Start a thread to handle receiving messages from the server
threading.Thread(target=recv_msg, args=(client_sock,)).start()

# Run the function to send messages
send_messa(client_sock)