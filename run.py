import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import re

def filter_console_mode_errors(output):
    # Remove specific error messages or unwanted characters
    error_messages = [
        "failed to get console mode for stdout: The handle is invalid.",
        "failed to get console mode for stderr: The handle is invalid."
    ]
    
    # Filter out unwanted spinner characters using regex
    output = re.sub(r'[\u2800-\u28FF]', '', output)  # Remove braille patterns
    for msg in error_messages:
        output = output.replace(msg, "")
    return output.strip()

def execute_command(user_input):
    command = f'ollama run llama2 "Summarize {user_input} in a few sentences."'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')

    def read_output(pipe):
        for line in iter(pipe.readline, ''):
            filtered_line = filter_console_mode_errors(line)
            if filtered_line:
                output_text.insert(tk.END, filtered_line + "\n")
                output_text.yview(tk.END)  # Auto-scroll to the bottom
                output_text.update_idletasks()  # Update the GUI with the output

    stdout_thread = threading.Thread(target=read_output, args=(process.stdout,))
    stderr_thread = threading.Thread(target=read_output, args=(process.stderr,))

    stdout_thread.start()
    stderr_thread.start()

    stdout_thread.join()
    stderr_thread.join()

def on_submit():
    user_input = input_entry.get("1.0", "end-1c").strip()
    output_text.insert(tk.END, f"\n")
    if user_input:
        output_text.insert(tk.END, f"Input: {user_input}\n")
        input_entry.delete("1.0", "end")
        
        # Run the ollama command in a separate thread to keep the GUI responsive
        thread = threading.Thread(target=execute_command, args=(user_input,))
        thread.start()

# Create the main window
window = tk.Tk()
window.title("Offline LLM")

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
