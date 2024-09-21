import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading

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
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Read and display standard output in real-time
    output_text.insert(tk.END, "Output: ")
    for stdout_line in iter(process.stdout.readline, ''):
        filtered_stdout = filter_console_mode_errors(stdout_line)
        if filtered_stdout:
            output_text.insert(tk.END, f"{filtered_stdout}\n")
            output_text.yview(tk.END)  # Auto-scroll to the bottom
    
    process.stdout.close()
    process.wait()  # Wait for the process to complete

def on_submit():
    user_input = input_entry.get("1.0", "end-1c").strip()
    if user_input:
        output_text.insert(tk.END, f"Input: {user_input}\n")
        input_entry.delete("1.0", "end")
        
        # Run the ollama command in a separate thread to keep the GUI responsive
        thread = threading.Thread(target=execute_command, args=(user_input,))
        thread.start()

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
