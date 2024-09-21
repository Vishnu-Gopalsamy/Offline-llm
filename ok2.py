import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import time

def filter_console_mode_errors(output):
    # Define the specific error messages to filter out
    error_messages = [
        "failed to get console mode for stdout: The handle is invalid.",
        "failed to get console mode for stderr: The handle is invalid."
    ]
    
    # Remove specific error messages from the output
    for msg in error_messages:
        output = output.replace(msg, "")
    return output.strip()

def execute_command(user_input):
    command = f'ollama run llama2 "{user_input}"'
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        # Filter out specific error messages
        filtered_stdout = filter_console_mode_errors(result.stdout)
        filtered_stderr = filter_console_mode_errors(result.stderr)

        # Only insert output if it's not empty
        if filtered_stdout:
            output_text.insert(tk.END, f"Output: {filtered_stdout}\n")
        if filtered_stderr:
            pass
           # output_text.insert(tk.END, f"Error: {filtered_stderr}\n")
    except subprocess.CalledProcessError as e:
        # Filter out specific error messages
        filtered_stderr = filter_console_mode_errors(e.stderr)
        #output_text.insert(tk.END, f"Error: {filtered_stderr}\n")

def run_ollama_command():
    while True:
        user_input = input_entry.get("1.0", "end-1c")
        if user_input.strip():
            output_text.insert(tk.END, f"Input: {user_input}\n")
            input_entry.delete("1.0", "end")

            # Run the ollama command in a separate thread to keep the GUI responsive
            thread = threading.Thread(target=execute_command, args=(user_input,))
            thread.start()
        time.sleep(10)  # Delay for 10 seconds after each command execution

def on_submit():
    threading.Thread(target=run_ollama_command, daemon=True).start()

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

# Start the main loop
window.mainloop()
