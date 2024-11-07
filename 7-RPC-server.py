import socket
import json

def add(args):
    return sum(args)

def subtract(args):
    return args[0] - args[1]

def multiply(args):
    return args[0] * args[1]

def divide(args):
    if args[1] == 0:
        return "Error: Division by zero"
    return args[0] / args[1]

def handle_client(client_socket):
    # Receive the request data from the client
    request = client_socket.recv(1024).decode()
    request_data = json.loads(request)

    function_name = request_data.get("function")
    args = request_data.get("args")

    # Prepare a response dictionary
    response = {
        "result": None
    }

    # Map function name to actual function and call it
    if function_name == "add":
        response["result"] = add(args)
    elif function_name == "subtract":
        response["result"] = subtract(args)
    elif function_name == "multiply":
        response["result"] = multiply(args)
    elif function_name == "divide":
        response["result"] = divide(args)
    else:
        response["result"] = "Error: Function not found"

    # Send the result back to the client
    client_socket.sendall(json.dumps(response).encode())
    client_socket.close()

def start_server(host='127.0.0.1', port=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server listening on {host}:{port}...")

    while True:
        # Accept a client connection
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        # Handle the client in a separate function
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()