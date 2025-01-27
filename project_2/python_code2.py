import socket
import numpy as np
import matplotlib.pyplot as plt
import struct

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

def receive_message(client_socket, data_size):
    """Receives raw data from the server."""
    data = client_socket.recv(data_size)  # Receive the data of the specified size
    print("Received data.")
    return data

def generate_sine_wave(num_samples, amplitude=32767, frequency=10, sample_rate=256):
    """Generates a sine wave of `num_samples`."""
    t = np.arange(num_samples) / sample_rate
    sine_wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return sine_wave.astype(np.int32)

def plot_data(sent_data, received_data):
    """Plots the sent and received data with customizations."""
    plt.figure(figsize=(10, 5))
    
    # Set background color to black
    plt.gcf().set_facecolor('black')
    
    # Plot the sent data
    plt.subplot(2, 1, 1)
    plt.title("Sent Sine Wave Data", color='white')
    plt.plot(sent_data, linewidth=3, color='yellow')  # Thicker cyan line for sent data
    plt.grid(True, color='white')  # White grid lines
    plt.tick_params(axis='both', colors='white')  # White ticks

    # Plot the received data
    plt.subplot(2, 1, 2)
    plt.title("Received Signal Data", color='white')
    plt.plot(received_data, linewidth=3, color='red')  # Thicker red line for received data
    plt.grid(True, color='white')  # White grid lines
    plt.tick_params(axis='both', colors='white')  # White ticks

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # Define the parameters here
    SERVER_IP = "192.168.1.10"  # Change to your server's IP address
    SERVER_PORT = 7            # Change to your server's port number
    NUM_SAMPLES = 256         # Number of sine samples to send
    
    # Generate the sine wave (integer values)
    sine_wave = generate_sine_wave(NUM_SAMPLES)
    
    # Connect to the server
    client_socket = connect_to_server(SERVER_IP, SERVER_PORT)
    
    # Send the sine wave data to the server (packed as binary)
    sine_wave_bytes = struct.pack(f'{NUM_SAMPLES}i', *sine_wave)
    send_message(client_socket, sine_wave_bytes)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
    # Receive the response (assuming the server sends 32-bit integers)
    raw_response = receive_message(client_socket, NUM_SAMPLES * 4)  # 4 bytes per integer
    received_data = np.array(struct.unpack(f'{NUM_SAMPLES}i', raw_response), dtype=np.int32)
    
    # Plot the sent and received data
    plot_data(sine_wave, received_data)
    
    # Close the connection
    client_socket.close()
    print("Connection closed.")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
