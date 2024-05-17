import socket
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import os

def send_message(ip, port, message):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024).decode('utf-8')
        update_response(response)
    except Exception as e:
        handle_error(f"An error occurred: {e}")
    finally:
        client_socket.close()

def update_response(response):
    response_text.insert(tk.END, f"Server response: {response}\n")

def handle_error(message):
    messagebox.showerror("Error", message)

def on_send_button_click():
    user_input = input_text.get()
    if user_input.lower() == 'exit':
        root.quit()
    else:
        send_message(ip_address, port_number, user_input)
        input_text.set("")

def prompt_for_ip_and_port():
    global ip_address, port_number
    ip_address = simpledialog.askstring("Input", "Enter IP address:", parent=root)
    port_number = simpledialog.askinteger("Input", "Enter port number:", parent=root)
    if ip_address and port_number:
        save_ip_and_port()
    else:
        handle_error("IP address and port number are required.")
        root.quit()

def save_ip_and_port():
    try:
        with open('saveipport.txt', 'w') as f:
            f.write(f"{ip_address}\n{port_number}")
    except Exception as e:
        handle_error(f"Error saving IP address and port number: {e}")

def load_ip_and_port():
    global ip_address, port_number
    if os.path.exists('saveipport.txt'):
        try:
            with open('saveipport.txt', 'r') as f:
                lines = f.readlines()
                if len(lines) == 2:
                    ip_address = lines[0].strip()
                    port_number = int(lines[1].strip())
                else:
                    prompt_for_ip_and_port()
        except Exception as e:
            handle_error(f"Error loading IP address and port number: {e}")
            prompt_for_ip_and_port()
    else:
        prompt_for_ip_and_port()

def toggle_fullscreen():
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))

def on_fullscreen_toggle(event=None):
    if root.attributes('-fullscreen'):
        root.attributes('-fullscreen', False)
    else:
        toggle_fullscreen()

root = tk.Tk()
root.title("Message Sender")

# Full screen setup
root.attributes('-fullscreen', True)
root.configure(bg='#008080')  # Background color: Teal
root.bind("<F11>", on_fullscreen_toggle)
root.bind("<Escape>", on_fullscreen_toggle)

frame = tk.Frame(root, bg='#008080')  # Frame background color: Teal
frame.pack(expand=True)

load_ip_and_port()

input_text = tk.StringVar()

response_text = scrolledtext.ScrolledText(frame, width=60, height=20, wrap=tk.WORD, bg='#f0f0f0', fg='#000000', font=("Helvetica", 12))
response_text.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

input_label = tk.Label(frame, text="Enter your message:", bg='#008080', fg='#ffffff', font=("Helvetica", 12))
input_label.grid(row=1, column=0, padx=10, pady=10)

input_entry = tk.Entry(frame, textvariable=input_text, width=50, bg='#ffffff', fg='#000000', font=("Helvetica", 12))
input_entry.grid(row=1, column=1, padx=10, pady=10)

send_button = tk.Button(frame, text="Send", command=on_send_button_click, bg='#32CD32', fg='#ffffff', font=("Helvetica", 12))  # Button color: Lime Green
send_button.grid(row=1, column=2, padx=10, pady=10)

root.mainloop()
