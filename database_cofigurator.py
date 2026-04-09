import os
import yaml
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class DatasetConfigurator:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO Dataset Configurator")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        # Variables
        self.dataset_path = tk.StringVar()
        self.train_dir = tk.StringVar(value="images")
        self.val_dir = tk.StringVar(value="images")
        self.class_names = tk.StringVar(value="dog, cat")

        self.create_widgets()

    def create_widgets(self):
        padding = {'padx': 20, 'pady': 10}

        # --- Section 1: Folder Selection ---
        header_font = ("Arial", 10, "bold")
        tk.Label(self.root, text="1. Select Dataset Root Folder", font=header_font).pack(anchor="w", **padding)
        
        path_frame = tk.Frame(self.root)
        path_frame.pack(fill="x", padx=20)
        
        tk.Entry(path_frame, textvariable=self.dataset_path, width=55).pack(side="left", ipady=3)
        tk.Button(path_frame, text="Browse", command=self.browse_folder, bg="#e1e1e1").pack(side="left", padx=5)

        # --- Section 2: Configuration Details ---
        tk.Label(self.root, text="2. Define Classes (Comma separated)", font=header_font).pack(anchor="w", **padding)
        tk.Entry(self.root, textvariable=self.class_names, width=70).pack(padx=20, ipady=3)

        config_frame = tk.Frame(self.root)
        config_frame.pack(fill="x", padx=20, pady=15)

        tk.Label(config_frame, text="Train Images Folder:").grid(row=0, column=0, sticky="w")
        tk.Entry(config_frame, textvariable=self.train_dir).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(config_frame, text="Val Images Folder:").grid(row=1, column=0, sticky="w")
        tk.Entry(config_frame, textvariable=self.val_dir).grid(row=1, column=1, padx=10, pady=5)

        # --- Section 3: Folder Structure Preview ---
        self.preview_text = tk.Text(self.root, height=5, width=65, bg="#f0f0f0", font=("Courier", 9))
        self.preview_text.pack(padx=20, pady=5)
        self.preview_text.insert("1.0", "Folder structure preview will appear here...")
        self.preview_text.config(state="disabled")

        # --- Section 4: Action Buttons ---
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Save data.yaml", command=self.save_yaml, 
                  bg="#4CAF50", fg="white", width=20, font=("Arial", 10, "bold")).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="Clear", command=self.clear_fields, width=10).pack(side="left")

    def browse_folder(self):
        path = filedialog.askdirectory(title="Select YOLO Dataset Root")
        if path:
            self.dataset_path.set(path)
            self.update_preview(path)

    def update_preview(self, path):
        self.preview_text.config(state="normal")
        self.preview_text.delete("1.0", tk.END)
        
        # Simple tree view
        preview = f"Selected: {os.path.basename(path)}\n"
        subfolders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        
        for folder in subfolders:
            preview += f" └── {folder}/\n"
            
        self.preview_text.insert("1.0", preview)
        self.preview_text.config(state="disabled")

    def save_yaml(self):
        path = self.dataset_path.get()
        if not path:
            messagebox.showerror("Error", "Please select a dataset folder!")
            return

        # Process classes
        raw_classes = self.class_names.get().split(',')
        classes_dict = {i: name.strip() for i, name in enumerate(raw_classes) if name.strip()}

        if not classes_dict:
            messagebox.showerror("Error", "Please enter at least one class name!")
            return

        # Prepare YAML data
        data_config = {
            'path': path,
            'train': self.train_dir.get(),
            'val': self.val_dir.get(),
            'names': classes_dict
        }

        try:
            # Save file in the current script directory
            save_path = os.path.join(os.getcwd(), 'data.yaml')
            with open(save_path, 'w') as f:
                yaml.dump(data_config, f, default_flow_style=False)
            
            messagebox.showinfo("Success", f"Configuration saved successfully!\n\nLocation: {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

    def clear_fields(self):
        self.dataset_path.set("")
        self.preview_text.config(state="normal")
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert("1.0", "Folder structure preview will appear here...")
        self.preview_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatasetConfigurator(root)
    root.mainloop()