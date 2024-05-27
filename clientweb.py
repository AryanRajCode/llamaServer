from flask import Flask, render_template, request
import socket

app = Flask(__name__)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


host = "0.0.0.0"
port = 12345

client_socket.connect((host, port))

def send_message(message):
    client_socket.send(message.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message_route():
    if request.method == 'POST':
        message = request.form['message']
        response = send_message(message)
        return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4040)
