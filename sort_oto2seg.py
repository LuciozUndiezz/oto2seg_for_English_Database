import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def select_source_folder():
    folder = filedialog.askdirectory()
    if folder:
        source_folder_var.set(folder)

def select_dest_root_folder():
    folder = filedialog.askdirectory()
    if folder:
        dest_root_folder_var.set(folder)

def sort_files():
    source_folder = source_folder_var.get()
    dest_root_folder = dest_root_folder_var.get()
    
    if not source_folder or not dest_root_folder:
        messagebox.showerror("Error", "Please select both source and destination root folders")
        return
    
    for prefix in prefixes:
        dest_folder = os.path.join(dest_root_folder, prefix)
        os.makedirs(dest_folder, exist_ok=True)
    
    for filename in os.listdir(source_folder):
        filepath = os.path.join(source_folder, filename)
        if os.path.isfile(filepath):  # Ensure the item is a file
            for prefix in prefixes:
                if filename.startswith(prefix):
                    shutil.move(filepath, os.path.join(dest_root_folder, prefix, filename))
                    break
    
    messagebox.showinfo("Success", "Files sorted successfully")

root = tk.Tk()
root.title("Sort Files by Prefix")

prefixes = ['vc_', 'cv_', 'vcv_', 'vv_', 'rv_', 'rcv_', 'rc_', 'vr_', 'cc_']

source_folder_var = tk.StringVar()
dest_root_folder_var = tk.StringVar()

tk.Label(root, text="Source Folder:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
tk.Entry(root, textvariable=source_folder_var, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_source_folder).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Destination Root Folder:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
tk.Entry(root, textvariable=dest_root_folder_var, width=50).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_dest_root_folder).grid(row=1, column=2, padx=10, pady=10)

tk.Button(root, text="Sort Files", command=sort_files).grid(row=2, column=0, columnspan=3, pady=20)

root.mainloop()
