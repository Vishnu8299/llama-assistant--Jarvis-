import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pytesseract
import mss
import os
import subprocess
import time
import pyautogui
import random
from langchain_ollama import OllamaLLM

# Set up the path for Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path if necessary

# Initialize the language model
model = OllamaLLM(model="llama3")
history_file = "conversation_history.txt"

def save_history(history):
    with open(history_file, "w", encoding="utf-8") as file:
        file.write("\n".join(history) + "\n")

def process_text(user_input):
    user_input = user_input.strip()

    if user_input:
        # Load existing history if available
        conversation_history = []
        if os.path.exists(history_file):
            with open(history_file, "r", encoding="utf-8") as file:
                conversation_history = file.read().splitlines()

        # Update history with user input
        conversation_history.append(f"User: {user_input}")
        prompt = "\n".join(conversation_history) + "\nBot:"

        try:
            # Measure the start time
            start_time = time.time()
            
            # Get model response
            result = model.invoke(input=prompt).strip()
            
            # Measure the end time
            end_time = time.time()
            
            # Calculate the response time
            response_time = end_time - start_time

            # Update history with model response
            conversation_history.append(f"Bot: {result}")

            # Check for command execution
            if "execute" in result.lower():
                command = result.lower().replace("execute", "").strip()
                command_result = subprocess.run(command, shell=True, capture_output=True, text=True)
                result = f"Executed command. Output: {command_result.stdout + command_result.stderr}"

            # Save history
            save_history(conversation_history)
            
            # Return the response and response time
            return {"response": result, "response_time": response_time}

        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}

    return {"error": "No input provided"}

def type_text(text):
    text_aar = text.split(" ")
    start_delay = 15

    # Initial delay before sending the message
    time.sleep(start_delay)

    for word in text_aar:
        for char in word:
            pyautogui.typewrite(char)
            # Random delay between each character (e.g., 0.1 to 0.5 seconds)
            char_delay = random.uniform(0.3, 0.6)
            time.sleep(char_delay)
        # Add a space between words
        pyautogui.typewrite(" ")
        # Random delay between each word (e.g., 0.5 to 1.0 seconds)
        word_delay = random.uniform(0.5, 0.8)
        time.sleep(word_delay)

    # Optionally, press Enter at the end if needed
    pyautogui.press("enter")

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
        
        # Process the extracted text using the model
        result = process_text(extracted_text)
        
        # Print the extracted text, model response, and response time
        print(f"Extracted Text: {extracted_text}")
        
        if 'response' in result:
            print(f"Model Response: {result['response']}")
            print(f"Response Time: {result['response_time']:.2f} seconds")

            # Ask the user if they want to type the response using pyautogui
            user_response = messagebox.askyesno("Type Response", "Do you want to type the response using pyautogui?")

            if user_response:
                # Type the model response using pyautogui
                type_text(result['response'])
            else:
                # You can add additional actions here if needed
                messagebox.showinfo("Info", "Response typing was skipped.")
        else:
            # Handle the error case
            print(f"Error: {result.get('error', 'Unknown error occurred')}")
            messagebox.showerror("Error", result.get('error', 'Unknown error occurred'))

if __name__ == "__main__":
    app = ScreenTextCaptureApp()
    app.mainloop()