import socket

def start_server(host='192.168.1.20', port=12345):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the address and port
    server_socket.bind((host, port))
    
    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    # Accept a connection
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    try:
        while True:
            # Send a command to the client
            command = input("Enter command to send to client: ")
            client_socket.send(command.encode())

            # Optionally, receive a response from the client
            response = client_socket.recv(1024).decode()
            print(f"Response from client: {response}")
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        client_socket.close()
        server_socket.close()
        server_socket.shutdown(socket.SHUT_RDWR)

if __name__ == "__main__":
    start_server()
