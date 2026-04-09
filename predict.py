import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from ultralytics import YOLO

class YoloPredictorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Cat & Dog Detector")
        self.root.geometry("700x650")
        self.root.configure(bg="#f5f6fa")

        # --- Variables ---
        # Provide the correct path to your trained weights
        self.model_path = r'runs/detect/train/weights/best.pt'
        self.loaded_model = None
        self.selected_img_path = None

        self.setup_ui()
        self.load_yolo_model()

    def setup_ui(self):
        # Header Label
        header = tk.Label(self.root, text="YOLOv8 Object Recognition", 
                          font=("Segoe UI", 18, "bold"), bg="#2f3640", fg="white", pady=15)
        header.pack(fill="x")

        # Image Display Area
        self.canvas = tk.Canvas(self.root, width=500, height=350, bg="#dcdde1", 
                                highlightthickness=2, highlightbackground="#7f8c8d")
        self.canvas.pack(pady=20)
        self.img_label = self.canvas.create_text(250, 175, text="No Image Selected", 
                                                 font=("Arial", 12), fill="#7f8c8d")

        # Control Buttons Frame
        btn_frame = tk.Frame(self.root, bg="#f5f6fa")
        btn_frame.pack(pady=10)

        self.select_btn = tk.Button(btn_frame, text="Upload Image", command=self.select_image,
                                    bg="#3498db", fg="white", font=("Arial", 11, "bold"), 
                                    width=15, pady=8, relief="flat")
        self.select_btn.grid(row=0, column=0, padx=10)

        self.predict_btn = tk.Button(btn_frame, text="Detect Objects", command=self.run_inference,
                                     bg="#2ecc71", fg="white", font=("Arial", 11, "bold"), 
                                     width=15, pady=8, relief="flat")
        self.predict_btn.grid(row=0, column=1, padx=10)

        # Status Bar
        self.status_var = tk.StringVar(value="Status: Waiting for user...")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, 
                                   relief="sunken", anchor="w", bg="#ffffff", padx=10)
        self.status_bar.pack(side="bottom", fill="x")

    def load_yolo_model(self):
        if os.path.exists(self.model_path):
            try:
                self.loaded_model = YOLO(self.model_path)
                self.status_var.set("Status: Model Loaded Successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load model: {e}")
        else:
            messagebox.showwarning("Warning", f"Could not find weights at:\n{self.model_path}\nPlease train the model first.")

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            self.selected_img_path = file_path
            self.display_image(file_path)
            self.status_var.set(f"Status: Selected {os.path.basename(file_path)}")

    def display_image(self, path):
        img = Image.open(path)
        img.thumbnail((500, 350))  # Resize to fit canvas
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(250, 175, image=self.tk_img)

    def run_inference(self):
        if not self.loaded_model:
            messagebox.showerror("Error", "Model not loaded!")
            return
        if not self.selected_img_path:
            messagebox.showwarning("Warning", "Please select an image first!")
            return

        self.status_var.set("Status: Detecting... Please wait.")
        self.root.update_idletasks()

        # Run Prediction
        results = self.loaded_model.predict(source=self.selected_img_path, save=True, conf=0.5)

        # Get the path where YOLO saved the result
        save_dir = results[0].save_dir
        result_filename = os.path.basename(self.selected_img_path)
        final_path = os.path.join(save_dir, result_filename)

        # Update Display with the result image (showing bounding boxes)
        if os.path.exists(final_path):
            self.display_image(final_path)
            self.status_var.set(f"Status: Detection Complete! Saved in {save_dir}")
            messagebox.showinfo("Success", f"Results saved to:\n{final_path}")
        else:
            self.status_var.set("Status: Detection finished, but couldn't load result preview.")

if __name__ == "__main__":
    root = tk.Tk()
    app = YoloPredictorGUI(root)
    root.mainloop()