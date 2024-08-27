import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pytesseract
import mss
import os

# Set up the path for Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path if necessary

class ScreenTextCaptureApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Screen Text Capture")
        self.geometry("200x100")

        self.selection_coords = None
        self.full_image = None

        self.info_label = tk.Label(self, text="Click 'Capture Screen' to start.")
        self.info_label.pack(pady=20)

        self.capture_button = tk.Button(self, text="Capture Screen", command=self.capture_screen)
        self.capture_button.pack(pady=5)

        self.image_label = tk.Label(self)
        self.image_label.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def capture_screen(self):
        try:
            with mss.mss() as sct:
                monitor = {"top": 0, "left": 0, "width": self.winfo_screenwidth(), "height": self.winfo_screenheight()}
                img = sct.grab(monitor)
                self.full_image = Image.frombytes('RGB', img.size, img.rgb)
                self.setup_selection_window()
        except Exception as e:
            messagebox.showerror("Error", f"Error capturing screen: {e}")

    def setup_selection_window(self):
        self.selection_window = tk.Toplevel(self)
        self.selection_window.title("Select Region")
        self.selection_window.attributes("-topmost", True)
        self.selection_window.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.selection_window.bind("<Button-1>", self.on_mouse_down)
        self.selection_window.bind("<ButtonRelease-1>", self.on_mouse_up)

        self.start_x = self.start_y = None
        self.selection_coords = None

        # Display the full screen image in the selection window
        self.display_full_image()

    def display_full_image(self):
        if not self.full_image:
            messagebox.showwarning("Warning", "No image available for display.")
            return
        
        full_image_tk = ImageTk.PhotoImage(self.full_image)
        image_label = tk.Label(self.selection_window, image=full_image_tk)
        image_label.image = full_image_tk  # Keep a reference to avoid garbage collection
        image_label.pack(fill=tk.BOTH, expand=True)

    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_up(self, event):
        end_x = event.x
        end_y = event.y

        x1, y1, x2, y2 = self.start_x, self.start_y, end_x, end_y
        
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        width = x2 - x1
        height = y2 - y1

        if width <= 0 or height <= 0:
            messagebox.showwarning("Warning", "Invalid selection area. Please select a valid region.")
            self.selection_coords = None
            return

        self.selection_coords = (x1, y1, x2, y2)
        self.selection_window.destroy()

        self.process_selected_region()

    def process_selected_region(self):
        if not self.selection_coords or not self.full_image:
            messagebox.showwarning("Warning", "No image available or selection invalid.")
            return

        x1, y1, x2, y2 = self.selection_coords
        selected_image = self.full_image.crop((x1, y1, x2, y2))
        extracted_text = pytesseract.image_to_string(selected_image)
        print(f"{extracted_text}")
if __name__ == "__main__":
    app = ScreenTextCaptureApp()
    app.mainloop()
