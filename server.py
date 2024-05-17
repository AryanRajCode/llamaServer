import socket
import threading
import queue
import ollama
# import uuid

# Function to handle client connections
def handle_client(client_socket, client_id, response_queue):
    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')
        print(f'Received from {client_id}: {data}')

        if not data:
            break

        # Pass received message to Ollama for response
        with open("model.txt") as j: 
            bb= j.read()
        response = ollama.chat(model=bb, messages=[{'role': 'user', 'content': data}])
        response_text = response['message']['content']

        # Put the response in the queue with client_id as identifier
        response_queue.put((client_id, response_text))

    # Close the connection
    client_socket.close()

# Function to send responses to clients
def send_responses(response_queue, clients):
    while True:
        client_id, response_text = response_queue.get()
        try:
            client_socket = clients.get(client_id)
            if client_socket:
                client_socket.send(response_text.encode('utf-8'))
            else:
                print(f"Client {client_id} not found.")
        except OSError as e:
            print(f"Error sending response to client {client_id}: {e}")
        finally:
            response_queue.task_done()

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the local machine name
host = "0.0.0.0"
port = 12345

# Bind to the port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(5)
print(f"Server listening on {host}:{port}")

# Queue to hold responses
response_queue = queue.Queue()

# Dictionary to hold connected clients
clients = {}

# Start a thread to send responses to clients
response_thread = threading.Thread(target=send_responses, args=(response_queue, clients))
response_thread.start()

try:
    while True:
        # Accept a connection
        client_socket, addr = server_socket.accept()
        print('Got connection from', addr)

        # Generate a unique client ID using IP address and port combination
        client_id = f"{addr[0]}:{addr[1]}"

        # Add the client to the dictionary of connected clients
        clients[client_id] = client_socket

        # Start a new thread to handle the client connection
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_id, response_queue))
        client_handler.start()

except KeyboardInterrupt:
    print("Server shutting down.")

finally:
    # Close the server socket
    server_socket.close()

    # Wait for the response thread to finish
    response_thread.join()
