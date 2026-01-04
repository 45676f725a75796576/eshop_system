import tkinter as tk
from tkinter import ttk
import requests

server_ip = ""
server_port = 1433

token = ""

def update_data():
    pass

def get_authorization_panel() -> tk.PanedWindow:
    global server_ip
    global password
    
    auth_panel = tk.PanedWindow()
    ip_label = tk.Label(auth_panel, width=60, text="Server IP address")
    ip_entry = tk.Entry(auth_panel, width=60)
    password_label = tk.Label(auth_panel, width=60, text="Password")
    password_entry = tk.Entry(auth_panel, width=60, show="*")
    port_label = tk.Label(auth_panel, width=30, text="Server Port")
    port_entry = tk.Entry(auth_panel, width=30)
    
    ip_label.pack(padx=5, pady=5)
    ip_entry.pack(padx=5, pady=5)
    password_label.pack(padx=5, pady=5)
    password_entry.pack(padx=5, pady=5)
    port_label.pack(padx=5, pady=5)
    port_entry.pack(padx=5, pady=5)
    
    def save_auth():
        global token
        global server_ip
        global server_port
        
        password = password_entry.get()
        server_ip = ip_entry.get()
        server_port = port_entry.get()
        
        url = f"http://{server_ip}:{server_port}/authorize"
        
        r = requests.get(url, params={'password': password})
        try:
            r.raise_for_status()
            
            token = r.json()["token"]
            
            auth_panel.destroy()
        except:
            pass
        
        
    
    submit_btn = tk.Button(auth_panel, text="Connect", command=save_auth)
    submit_btn.pack(padx=30, pady=100)
    
    return auth_panel

if __name__ == '__main__':
    root = tk.Tk()
    root.title("E-shop register system")
    
    def on_closing():
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    a_panel = get_authorization_panel()
    a_panel.pack(fill=tk.BOTH)
    
    root.mainloop()