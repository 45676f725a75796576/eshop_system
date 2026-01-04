import tkinter as tk
from tkinter import ttk
import requests

server_ip = ""
server_port = 1433

token = ""

data = {
    "Orders": [],
    "Products": [],
    "Warehouses": [],
    "Inventory": []
}

def update_data():
    global data
    url = f"http://{server_ip}:{server_port}/orders/all"
    
    r = requests.get(url, params={"token": token})
    r.raise_for_status()
    data["Orders"] = list(r.json())
    
    url = f"http://{server_ip}:{server_port}/products/all"
    
    r = requests.get(url, params={"token": token})
    r.raise_for_status()
    data["Products"] = list(r.json())
    
    url = f"http://{server_ip}:{server_port}/warehouses/all"
    
    r = requests.get(url, params={"token": token})
    r.raise_for_status()
    data["Warehouses"] = list(r.json())
    
    url = f"http://{server_ip}:{server_port}/inventory"
    
    r = requests.get(url, params={"token": token})
    r.raise_for_status()
    data["Inventory"] = list(r.json())

def populate_tree(tree: ttk.Treeview, parent: str, data: dict):
    if len(data.items()) < 1:
        tree.insert(parent, "end", text="directory is empty")
        return

    for name, content in data.items():
        if isinstance(content, dict):
            node = tree.insert(parent, "end", text=name, open=False)
            populate_tree(tree, node, dict(content))
        else:
            tree.insert(parent, "end", text=name)

def get_authorization_panel() -> tk.PanedWindow:
    global server_ip
    global password
    
    auth_panel = tk.PanedWindow(width=600, height=500)
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
            
            create_main_panel()
        except:
            pass
        
    submit_btn = tk.Button(auth_panel, text="Connect", command=save_auth)
    submit_btn.pack(padx=30, pady=100)
    
    return auth_panel

def create_main_panel() -> tk.PanedWindow:
    global root

    main = tk.PanedWindow(root, width=1280, height=720)
    main.pack(fill=tk.BOTH, expand=True)

    frame_left = tk.Frame(main)
    tree = ttk.Treeview(frame_left)
    tree.pack(fill=tk.BOTH, expand=True)
    main.add(frame_left, width=300)
    
    frame_right = tk.Frame(main, bg="#CFCFCF")
    main.add(frame_right, width=300, height=600)
    
    update_data()
    
    populate_tree(tree, "", data) 
    
    return main
    
if __name__ == '__main__':
    root = tk.Tk()
    root.title("E-shop register system")
    
    def on_closing():
        url = f"http://{server_ip}:{server_port}/logout"
        r = requests.delete(url, params={'token': token})
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    a_panel = get_authorization_panel()
    a_panel.pack(fill=tk.BOTH)
    
    root.mainloop()