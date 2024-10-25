import bluetooth
import random
import time

def bluetooth_server():
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1
    server_socket.bind(("", port))
    server_socket.listen(1)

    print("Waiting for a connection...")
    client_socket, address = server_socket.accept()
    print(f"Accepted connection from {address}")
    return client_socket, address, server_socket
