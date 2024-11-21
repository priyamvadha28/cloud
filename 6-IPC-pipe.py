'''import os

def parent_child_communication():
    # Create two pipes: one for parent-to-child and one for child-to-parent communication
    parent_to_child, child_to_parent = os.pipe(), os.pipe()

    # Fork the process to create a child
    pid = os.fork()

    if pid > 0:  # Parent process
        # Close unused ends of pipes
        os.close(parent_to_child[0])  # Close reading end of parent-to-child pipe
        os.close(child_to_parent[1])  # Close writing end of child-to-parent pipe

        # Message from parent to child
        parent_message = "Hello from parent!".encode()
        os.write(parent_to_child[1], parent_message)
        print("Parent: Sent message to child.")

        # Read response from the child
        child_response = os.read(child_to_parent[0], 1024).decode()
        print("Parent: Received response from child:", child_response)

        # Close used ends of pipes
        os.close(parent_to_child[1])
        os.close(child_to_parent[0])

    else:  # Child process
        # Close unused ends of pipes
        os.close(parent_to_child[1])  # Close writing end of parent-to-child pipe
        os.close(child_to_parent[0])  # Close reading end of child-to-parent pipe

        # Read message from the parent
        parent_message = os.read(parent_to_child[0], 1024).decode()
        print("Child: Received message from parent:", parent_message)

        # Message from child to parent
        child_message = "Hello from child!".encode()
        os.write(child_to_parent[1], child_message)
        print("Child: Sent response to parent.")

        # Close used ends of pipes
        os.close(parent_to_child[0])
        os.close(child_to_parent[1])

if __name__ == "__main__":
    parent_child_communication()'''

''''import multiprocessing

def child_process(child_conn):
    # Receive message from the parent
    parent_message = child_conn.recv()
    print("Child: Received message from parent:", parent_message)

    # Send a response back to the parent
    child_message = "Hello from child!"
    child_conn.send(child_message)
    print("Child: Sent response to parent.")

def parent_child_communication():
    # Create a Pipe
    parent_conn, child_conn = multiprocessing.Pipe()

    # Create and start the child process
    child = multiprocessing.Process(target=child_process, args=(child_conn,))
    child.start()

    # Send a message to the child
    parent_message = "Hello from parent!"
    parent_conn.send(parent_message)
    print("Parent: Sent message to child.")

    # Receive the response from the child
    child_response = parent_conn.recv()
    print("Parent: Received response from child:", child_response)

    # Wait for the child process to finish
    child.join()

if __name__ == "__main__":
    parent_child_communication()''''

import multiprocessing

def child_process(pipe):
    # Receive message from parent
    message = pipe.recv()
    print(f"Child received: {message}")
    
    # Respond to parent
    response = "Hello Parent! I got your message."
    pipe.send(response)

def parent_process():
    # Create a pipe
    parent_conn, child_conn = multiprocessing.Pipe()
    
    # Start the child process
    child = multiprocessing.Process(target=child_process, args=(child_conn,))
    child.start()
    
    # Send message to the child
    message = "Hello Child! How are you?"
    parent_conn.send(message)
    
    # Receive response from the child
    response = parent_conn.recv()
    print(f"Parent received: {response}")
    
    # Wait for the child process to finish
    child.join()

if __name__ == "__main__":
    parent_process()