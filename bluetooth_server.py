import bluetooth
import random
import time

def generate_pin():
    return str(random.randint(1000, 9999))

def main():
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1
    server_socket.bind(("", port))
    server_socket.listen(1)

    print("Waiting for a connection...")
    client_socket, address = server_socket.accept()
    print(f"Accepted connection from {address}")

    while True:
        pin = generate_pin()
        print(f"Generated PIN: {pin}")

        # Send PIN to mobile device
        client_socket.send(pin)
        print("PIN sent to mobile device.")

        # Wait for the response from the mobile device
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received PIN from mobile device: {data}")
        print(data)

        if data == pin:
            print("PIN verified successfully! Transaction can be signed.")
        else:
            print("Invalid PIN! Access denied.")

        time.sleep(5)  # Wait before generating the next PIN

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
