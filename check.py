import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading

def start_ollama_process():
    global ollama_process

    # Start the ollama process in a persistent mode
    ollama_process = subprocess.Popen(
        ["ollama", "run", "llama2"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True
    )

def send_input_to_ollama(user_input):
    if ollama_process:
        # Send input to the running ollama process
        ollama_process.stdin.write(user_input + "\n")
        ollama_process.stdin.flush()

        # Capture the output
        output = ollama_process.stdout.readline()

        # Display the output in the GUI
        output_text.insert(tk.END, f"Output: {output}\n")

def on_submit():
    user_input = input_entry.get("1.0", "end-1c")
    if user_input.strip():
        output_text.insert(tk.END, f"Input: {user_input}\n")
        input_entry.delete("1.0", "end")

        # Send the user input to the ollama process in a separate thread
        thread = threading.Thread(target=send_input_to_ollama, args=(user_input,))
        thread.start()

# Initialize the Ollama process globally
ollama_process = None

# Create the main window
window = tk.Tk()
window.title("Ollama Terminal GUI")

# Input entry
input_label = tk.Label(window, text="Enter your query:")
input_label.pack()

input_entry = tk.Text(window, height=3)
input_entry.pack()

# Submit button
submit_button = tk.Button(window, text="Submit", command=on_submit)
submit_button.pack()

# Output display
output_text = scrolledtext.ScrolledText(window, height=20, width=60)
output_text.pack()

# Start the Ollama process when the GUI is launched
start_ollama_process()

# Start the main loop
window.mainloop()

# Ensure the Ollama process is terminated when the GUI is closed
if ollama_process:
    ollama_process.terminate()
