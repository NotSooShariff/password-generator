import customtkinter as ctk
import string
import random
import pyperclip
import hashlib
from datetime import datetime
import os
import psutil
import platform
from pathlib import Path

class PasswordGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Password Generator")
        self.geometry("800x600")

        custom_font = ("mono", 18)

        # Seed Word Entry
        self.seed_label = ctk.CTkLabel(self, text="Seed Word:", font=custom_font)
        self.seed_label.pack(pady=10)
        self.seed_entry = ctk.CTkEntry(self, font=custom_font)
        self.seed_entry.pack(pady=10)

        # Password Length Slider
        self.length_label = ctk.CTkLabel(self, text="Password Length:", font=custom_font)
        self.length_label.pack(pady=10)

        self.slider_frame = ctk.CTkFrame(self)
        self.slider_frame.pack(pady=10)

        self.length_slider = ctk.CTkSlider(self.slider_frame, from_=8, to=32, number_of_steps=24, command=self.update_slider_label)
        self.length_slider.grid(row=0, column=0, padx=5)
        self.length_slider.set(8)  # Set initial slider value

        self.slider_value_label = ctk.CTkLabel(self.slider_frame, text=f"{int(self.length_slider.get())}", font=custom_font)
        self.slider_value_label.grid(row=0, column=1, padx=5)

        # Checkboxes
        self.uppercase_var = ctk.BooleanVar()
        self.lowercase_var = ctk.BooleanVar()
        self.symbols_var = ctk.BooleanVar()
        self.numbers_var = ctk.BooleanVar()
    
        # Set initial values for checkboxes
        self.uppercase_var = ctk.BooleanVar(value=True)
        self.lowercase_var = ctk.BooleanVar(value=True)
        self.symbols_var = ctk.BooleanVar(value=True)
        self.numbers_var = ctk.BooleanVar(value=True)


        self.uppercase_check = ctk.CTkCheckBox(self, text="Include Uppercase", variable=self.uppercase_var, font=custom_font)
        self.uppercase_check.pack(pady=5)
        self.lowercase_check = ctk.CTkCheckBox(self, text="Include Lowercase", variable=self.lowercase_var, font=custom_font)
        self.lowercase_check.pack(pady=5)
        self.symbols_check = ctk.CTkCheckBox(self, text="Include Symbols", variable=self.symbols_var, font=custom_font)
        self.symbols_check.pack(pady=5)
        self.numbers_check = ctk.CTkCheckBox(self, text="Include Numbers", variable=self.numbers_var, font=custom_font)
        self.numbers_check.pack(pady=5)

        # Generate Button
        self.generate_button = ctk.CTkButton(self, text="Generate ➡️", command=self.generate_password, font=custom_font, height=20, width=40)
        self.generate_button.pack(pady=20)

    def update_slider_label(self, value):
        self.slider_value_label.configure(text=f"{int(value)}")

    def generate_password(self):
        seed_word = self.seed_entry.get()
        length = int(self.length_slider.get())
        include_uppercase = self.uppercase_var.get()
        include_lowercase = self.lowercase_var.get()
        include_symbols = self.symbols_var.get()
        include_numbers = self.numbers_var.get()

        # Get current time and convert to MD5 hash
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        time_hash = hashlib.md5(current_time.encode()).hexdigest()

        #System Info
        disk_usage = psutil.disk_usage('/').percent
        memory_usage = psutil.virtual_memory().percent
        platform_info = platform.platform()
        system = platform.system()
        processor = platform.processor()
        
        # Combine seed word and time hash
        combined_seed = seed_word + time_hash + str(disk_usage) + str(memory_usage) + platform_info + system + processor
        print(combined_seed)

        characters = ''
        if include_uppercase:
            characters += string.ascii_uppercase
        if include_lowercase:
            characters += string.ascii_lowercase
        if include_symbols:
            characters += string.punctuation
        if include_numbers:
            characters += string.digits

        if not characters:
            characters = string.ascii_letters + string.digits + string.punctuation

        random.seed(combined_seed)
        password = ''.join(random.choice(characters) for _ in range(length))

        self.show_password_screen(password)

    def show_password_screen(self, password):
        custom_font = ("mono", 18)

        self.password_screen = ctk.CTkToplevel(self)
        self.password_screen.title("Generated Password")
        self.password_screen.geometry("600x250")

        # Ensure the new window is on top
        self.password_screen.lift()
        self.password_screen.attributes("-topmost", True)

        self.password_label = ctk.CTkLabel(self.password_screen, text="Generated Password:", font=custom_font)
        self.password_label.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self.password_screen, width=300, font=custom_font)
        self.password_entry.insert(0, password)
        self.password_entry.pack(pady=10)

        self.copy_button = ctk.CTkButton(self.password_screen, text="Copy to Clipboard", command=lambda: self.copy_to_clipboard(password), font=custom_font)
        self.copy_button.pack(pady=5)

        self.save_button = ctk.CTkButton(self.password_screen, text="Save as Document", command=lambda: self.save_as_document(password), font=custom_font)
        self.save_button.pack(pady=5)


    def copy_to_clipboard(self, password):
        pyperclip.copy(password)
        self.show_custom_message_box(f"Password copied to clipboard", "✅")
        self.password_screen.destroy()

    def save_as_document(self, password):
        # Get the Downloads folder path
        downloads_path = str(Path.home() / "Downloads")
        
        # Format the current date and time for the file name
        current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        safe_time = current_time.replace(":", "-") 

        # Construct the file name
        file_name = f"Password Generated on {safe_time}.txt"
        file_path = os.path.join(downloads_path, file_name)

        # Save the password to the file
        with open(file_path, "w") as file:
            file.write(password)
        
        self.show_custom_message_box(f"Password saved as \n ' {file_name} ' \n in Downloads", "💾")
        self.password_screen.destroy()

    def show_custom_message_box(self, message, icon):
        custom_font = ("mono", 18)

        message_box = ctk.CTkToplevel(self)
        message_box.title("Information")
        message_box.geometry("500x230")

        # Ensure the new window is on top
        self.password_screen.lift()
        self.password_screen.attributes("-topmost", True)

        icon_label = ctk.CTkLabel(message_box, text=icon, font=("Arial", 48))
        icon_label.pack(pady=10)

        message_label = ctk.CTkLabel(message_box, text=message, font=custom_font)
        message_label.pack(pady=10)

        ok_button = ctk.CTkButton(message_box, text="OK", command=message_box.destroy,font=custom_font)
        ok_button.pack(pady=10)

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
