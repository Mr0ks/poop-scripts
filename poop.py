import os
import sys
import subprocess
import threading
import ctypes
import keyboard
import pyautogui
import tkinter as tk
import time

# Function to install required libraries
def install_dependencies():
    required_packages = ["keyboard", "pyautogui", "tk"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install dependencies at the start
install_dependencies()

# Function to lock the screen
def lock_screen():
    # Create a fullscreen Tkinter window to simulate the lock
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(background="black")
    label = tk.Label(root, text="COMPUTER LOCKED", fg="red", bg="black", font=("Arial", 40))
    label.pack(expand=True)
    
    # Block all keyboard and mouse input
    ctypes.windll.user32.BlockInput(True)

    # Monitor for override keys
    def check_override():
        # If Ctrl + Alt is pressed, unblock the input and destroy the lock screen
        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("alt"):
            ctypes.windll.user32.BlockInput(False)
            root.destroy()
    
    # Periodically check for the unlock condition (Ctrl + Alt)
    def periodic_check():
        check_override()
        root.after(100, periodic_check)
    
    periodic_check()
    root.mainloop()

# Function to block all keyboard keys except Ctrl and Alt
def disable_all_keys_except_ctrl_alt():
    def block_keys(event):
        # Allow only Ctrl and Alt keys, block all others (including Windows key)
        if event.name not in ["ctrl", "alt"]:
            return False  # Block all other key presses
    keyboard.hook(block_keys)

# Function to disable mouse movement (continuously reset mouse position)
def disable_mouse():
    while True:
        pyautogui.moveTo(0, 0)  # Continuously move mouse to (0, 0) to block it
        time.sleep(0.1)  # Adjust the sleep time to control the frequency of resetting

# Main function to execute the lock
def main():
    # Start key disabling and mouse blocking in separate threads
    threading.Thread(target=disable_all_keys_except_ctrl_alt, daemon=True).start()
    threading.Thread(target=disable_mouse, daemon=True).start()
    
    # Lock the screen by preventing input
    lock_screen()

if __name__ == "__main__":
    main()
