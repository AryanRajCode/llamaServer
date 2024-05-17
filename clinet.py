import socket

def send_message(ip, port, message):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()

def get_ip_and_port():
    try:
        with open('ip_port.txt', 'r') as f:
            ip_address, port_number = f.readline().strip(), int(f.readline().strip())
            return ip_address, port_number
    except FileNotFoundError:
        return None, None

def save_ip_and_port(ip_address, port_number):
    try:
        with open('ip_port.txt', 'w') as f:
            f.write(f"{ip_address}\n{port_number}")
    except Exception as e:
        print(f"Error saving IP address and port number: {e}")

def main():
    ip_address, port_number = get_ip_and_port()
    if not ip_address or not port_number:
        ip_address = input("Enter IP address: ")
        port_number = int(input("Enter port number: "))
        save_ip_and_port(ip_address, port_number)

    while True:
        user_input = input("Enter your message ('exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        else:
            send_message(ip_address, port_number, user_input)

if __name__ == "__main__":
    main()
