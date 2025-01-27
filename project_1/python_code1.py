import socket

def connect_to_server(server_ip, server_port):
    """Establishes a connection to the server and returns the socket."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Connected to server at {server_ip}:{server_port}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    return client_socket

def send_message(client_socket, data):
    """Sends raw data to the server."""
    client_socket.sendall(data)
    print("Sent data.")

def receive_message(client_socket):
    """Receives raw data from the server."""
    data = client_socket.recv(1024)  # Buffer size is 1024 bytes
    print("Received data.")
    return data

if __name__ == "__main__":
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # define the paramters here
    SERVER_IP = "192.168.1.10"  # Change to your server's IP address
    SERVER_PORT = 7       # Change to your server's port number
    MESSAGE = "Hello, Server!"
    
    # Connect to the server
    client_socket = connect_to_server(SERVER_IP, SERVER_PORT)

    # Encode the message
    encoded_message = MESSAGE.encode('utf-8')
    
    # Send the encoded message to the server
    print(f"Sent to server: {MESSAGE}")
    send_message(client_socket, encoded_message)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # Receive the response from the server
    raw_response = receive_message(client_socket)

    # Decode the response
    response = raw_response.decode('utf-8')
    print(f"Response from server: {response}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # Close the connection
    client_socket.close()
    print("Connection closed.")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
