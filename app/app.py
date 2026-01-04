import tkinter as tk
from tkinter import ttk
import requests

server_ip = "localhost"
server_port = 5000

token = ""

ITEM_PARAMS = {
    "Orders": ["user_id", "currency", "shipping_address", "billing_address"],
    "Products": ["product_name", "unit_price", "tax_rate"],
    "Warehouses": ["warehouse_name", "location_code", "is_active"],
    "Inventory": ["product_id", "warehouse_id", "quantity"]
}

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
    tree.delete(*tree.get_children())

    for section, items in data.items():
        section_id = tree.insert(parent, "end", text=section, open=True)

        for idx, item in enumerate(items):
            tree.insert(
                section_id,
                "end",
                text=f"{section} #{idx}",
                iid=f"{section}:{idx}"
            )
            
        tree.insert(
            section_id,
            "end",
            text=f"[ + New {section} ]",
            iid=f"{section}:new"
        )

def get_authorization_panel() -> tk.PanedWindow:
    global server_ip
    global password
    global server_port
    
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
        except Exception as e:
            print(str(e))
        
    submit_btn = tk.Button(auth_panel, text="Connect", command=save_auth)
    submit_btn.pack(padx=30, pady=100)
    
    return auth_panel

def create_main_panel() -> tk.PanedWindow:
    global root

    main = tk.PanedWindow(root, width=1280, height=720)
    main.pack(fill=tk.BOTH, expand=True)

    frame_left = tk.Frame(main)
    frame_left.pack(fill=tk.BOTH, expand=True)

    frame_right = tk.Frame(main, bg="#CFCFCF")

    def on_tree_select(event):
        tree = event.widget
        selection = tree.selection()

        if not selection:
            return

        item_id = selection[0]
        parent_id = tree.parent(item_id)

        if not parent_id:
            return

        section = tree.item(parent_id, "text")
        item_name = tree.item(item_id, "text")
        
        is_new = item_id.endswith(":new")

        show_item_editor(section, item_name, is_new)

    def show_item_editor(section: str, item_name: str, is_new: bool):
        for widget in frame_right.winfo_children():
            widget.destroy()
            
        title = f"Create new {section}" if is_new else item_name

        tk.Label(
            frame_right,
            text=title,
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=10, pady=10)

        params = ITEM_PARAMS.get(section, [])

        for param in params:
            row = tk.Frame(frame_right)
            row.pack(fill=tk.X, padx=10, pady=4)

            tk.Label(row, text=param, width=20, anchor="w").pack(side=tk.LEFT)
            tk.Entry(row).pack(side=tk.RIGHT, fill=tk.X, expand=True)

    tree = ttk.Treeview(frame_left)
    tree.pack(fill=tk.BOTH, expand=True)
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    main.add(frame_left, width=300)
    main.add(frame_right, width=600)

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