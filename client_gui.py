import socket
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time


# ================= SPLASH =================

def splash_screen():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.geometry("420x320+500+250")
    splash.configure(bg="#020617")

    img = Image.open("logo.png")
    img = img.resize((100, 100))
    logo = ImageTk.PhotoImage(img)

    tk.Label(splash, image=logo, bg="#020617").pack(pady=20)
    splash.logo = logo

    tk.Label(splash, text="PyNet Monitor Client",
             fg="white", bg="#020617",
             font=("Segoe UI", 16, "bold")).pack()

    tk.Label(splash, text="Initializing network module...",
             fg="#38bdf8", bg="#020617").pack(pady=10)

    splash.update()
    time.sleep(2)
    splash.destroy()


# ================= SEND =================

def send_data():
    username = username_entry.get()
    server_ip = ip_entry.get()
    message = message_entry.get()

    if username == "" or server_ip == "" or message == "":
        messagebox.showwarning("Warning", "Semua field harus diisi!")
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, 5000))

        data = username + "|" + message
        client_socket.send(data.encode())

        response = client_socket.recv(1024).decode()

        status_label.config(text="✓ " + response, fg="#22c55e")

        client_socket.close()

    except:
        status_label.config(text="✗ Connection Failed", fg="#ef4444")


# ================= GUI =================

splash_screen()

window = tk.Tk()
window.title("PyNet Monitor Client")
window.geometry("520x460")
window.configure(bg="#020617")
window.resizable(False, False)


# MAIN CARD
card = tk.Frame(window, bg="#0f172a", width=450, height=360)
card.place(relx=0.5, rely=0.5, anchor="center")


# TITLE
tk.Label(card, text="PyNet Monitor Client",
         font=("Segoe UI", 20, "bold"),
         fg="white", bg="#0f172a").pack(pady=20)


# FIELD STYLE
def create_entry(parent):
    return tk.Entry(parent,
                    width=30,
                    bg="#020617",
                    fg="white",
                    insertbackground="white",
                    relief="flat",
                    font=("Segoe UI", 10))


# USERNAME
tk.Label(card, text="Username",
         fg="#94a3b8", bg="#0f172a").pack()

username_entry = create_entry(card)
username_entry.pack(pady=6)


# SERVER IP
tk.Label(card, text="Server IP",
         fg="#94a3b8", bg="#0f172a").pack()

ip_entry = create_entry(card)
ip_entry.insert(0, "127.0.0.1")
ip_entry.pack(pady=6)


# MESSAGE
tk.Label(card, text="Message",
         fg="#94a3b8", bg="#0f172a").pack()

message_entry = create_entry(card)
message_entry.pack(pady=6)


# SEND BUTTON
send_btn = tk.Button(card,
                     text="SEND DATA",
                     width=26,
                     height=1,
                     bg="#2563eb",
                     fg="white",
                     relief="flat",
                     font=("Segoe UI", 10, "bold"),
                     activebackground="#1d4ed8",
                     command=send_data)
send_btn.pack(pady=20)


# STATUS
status_label = tk.Label(card,
                        text="",
                        bg="#0f172a",
                        font=("Segoe UI", 10))
status_label.pack()

window.mainloop()
