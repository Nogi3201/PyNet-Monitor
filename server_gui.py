import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, ttk
from datetime import datetime
from PIL import Image, ImageTk
import time

HOST = "0.0.0.0"
PORT = 5000

server_socket = None
server_running = False

client_count = 0
message_count = 0
total_bytes = 0

clients = {}   # username : ip


# ================= SPLASH =================

def splash_screen():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.geometry("400x300+500+250")
    splash.configure(bg="#0f172a")

    img = Image.open("logo.png")
    img = img.resize((100, 100))
    logo = ImageTk.PhotoImage(img)

    lbl = tk.Label(splash, image=logo, bg="#0f172a")
    lbl.image = logo
    lbl.pack(pady=20)

    title = tk.Label(splash, text="PyNet Monitor",
                     fg="white", bg="#0f172a",
                     font=("Arial", 16, "bold"))
    title.pack()

    load = tk.Label(splash, text="Loading Server Dashboard...",
                    fg="#00ff9d", bg="#0f172a")
    load.pack(pady=10)

    splash.update()
    time.sleep(2)
    splash.destroy()


# ================= AUTO IP =================

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    s.close()
    return ip


# ================= LOG =================

def write_log(message):
    with open("log.txt", "a") as file:
        file.write(message + "\n")


# ================= UPDATE COUNTER =================

def update_counter():
    client_label.config(text=f"Clients Connected: {client_count}")
    message_label.config(text=f"Messages Received: {message_count}")
    data_label.config(text=f"Total Data: {round(total_bytes / 1024, 2)} KB")


# ================= CLIENT TABLE =================

def update_client_table():
    for item in client_table.get_children():
        client_table.delete(item)

    for username, ip in clients.items():
        client_table.insert("", "end", values=(username, ip, "ONLINE"))


# ================= SERVER =================

def start_server():
    global server_socket, server_running
    global client_count, message_count, total_bytes

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    server_running = True

    status_label.config(text="SERVER ONLINE", fg="#00ff9d")
    log_box.insert(tk.END, "Server started...\n")

    while server_running:
        try:
            client_socket, addr = server_socket.accept()

            data = client_socket.recv(1024)
            total_bytes += len(data)

            decoded = data.decode()

            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if decoded:
                username, message = decoded.split("|")

                # Save client
                clients[username] = addr[0]

                client_count = len(clients)
                message_count += 1

                update_counter()
                update_client_table()

                log_text = f"[{time_now}] {username} ({addr[0]}) : {message}\n"

                log_box.insert(tk.END, log_text)
                write_log(log_text)

                client_socket.send("Data received successfully".encode())

            client_socket.close()

        except:
            break


# ================= BUTTON =================

def start_button():
    thread = threading.Thread(target=start_server)
    thread.daemon = True
    thread.start()


def stop_button():
    global server_running

    server_running = False

    if server_socket:
        server_socket.close()

    status_label.config(text="SERVER OFFLINE", fg="red")
    log_box.insert(tk.END, "Server stopped...\n")


def clear_log():
    log_box.delete("1.0", tk.END)


# ================= MAIN GUI =================

splash_screen()

window = tk.Tk()
window.title("PyNet Monitor Server")
window.geometry("1000x650")
window.configure(bg="#1e1e1e")
window.resizable(False, False)


# LOGO
img = Image.open("logo.png")
img = img.resize((110, 110))
logo = ImageTk.PhotoImage(img)

logo_label = tk.Label(window, image=logo, bg="#1e1e1e")
logo_label.image = logo
logo_label.pack(pady=5)


title = tk.Label(window, text="PyNet Monitor Server Dashboard",
                 font=("Arial", 18, "bold"),
                 fg="white", bg="#1e1e1e")
title.pack()


ip_label = tk.Label(window, text=f"Local IP : {get_local_ip()}",
                    fg="#00ff9d", bg="#1e1e1e")
ip_label.pack()


status_label = tk.Label(window, text="SERVER OFFLINE",
                        fg="red", bg="#1e1e1e")
status_label.pack()


# ================= COUNTER PANEL =================

counter_frame = tk.Frame(window, bg="#1e1e1e")
counter_frame.pack(pady=10)

client_label = tk.Label(counter_frame, text="Clients Connected: 0",
                        fg="white", bg="#1e1e1e")
client_label.grid(row=0, column=0, padx=20)

message_label = tk.Label(counter_frame, text="Messages Received: 0",
                         fg="white", bg="#1e1e1e")
message_label.grid(row=0, column=1, padx=20)

data_label = tk.Label(counter_frame, text="Total Data: 0 KB",
                      fg="white", bg="#1e1e1e")
data_label.grid(row=0, column=2, padx=20)


# ================= BUTTON =================

btn_frame = tk.Frame(window, bg="#1e1e1e")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="START SERVER", bg="#00ff9d",
          width=15, command=start_button).grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="STOP SERVER", bg="red", fg="white",
          width=15, command=stop_button).grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="CLEAR LOG", bg="#f59e0b",
          width=15, command=clear_log).grid(row=0, column=2, padx=5)


# ================= CLIENT TABLE =================

table_frame = tk.Frame(window)
table_frame.pack(pady=10)

columns = ("Username", "IP Address", "Status")

style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
    background="#111",
    foreground="white",
    rowheight=30,
    fieldbackground="#111",
    bordercolor="#111",
    borderwidth=0
)

style.configure("Treeview.Heading",
    background="#1f2937",
    foreground="white",
    relief="flat"
)

style.map("Treeview",
    background=[("selected", "#2563eb")]
)


client_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)

client_table.heading("Username", text="Username")
client_table.heading("IP Address", text="IP Address")
client_table.heading("Status", text="Status")

client_table.column("Username", width=200)
client_table.column("IP Address", width=200)
client_table.column("Status", width=120)

client_table.pack()


# ================= LOG BOX =================

log_box = scrolledtext.ScrolledText(window,
                                   width=110,
                                   height=12,
                                   bg="#111",
                                   fg="#00ff9d")
log_box.pack(pady=10)


window.mainloop()
