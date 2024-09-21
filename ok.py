import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading

def filter_console_mode_errors(output):
    # Define the specific error messages to filter out (if necessary)
    error_messages = [
        "failed to get console mode for stdout: The handle is invalid.",
        "failed to get console mode for stderr: The handle is invalid."
    ]
    
    # Remove specific error messages from the output
    for msg in error_messages:
        output = output.replace(msg, "")
    return output.strip()

def execute_command(user_input):
    # Format the command to request a summary
    command = f'ollama run llama2 "Summarize {user_input} in a few sentences."'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    
    # Maximum number of characters to display
    max_chars = 1000

    # Continuously read from stdout while the process runs
    def read_output(pipe):
        output_text.insert(tk.END, "Output: ")
        output_accumulated = ""
        for line in iter(pipe.readline, ''):
            filtered_line = filter_console_mode_errors(line)
            if filtered_line:
                output_accumulated += filtered_line + " "
                # Truncate the output if it exceeds the max_chars limit
                if len(output_accumulated) > max_chars:
                    output_accumulated = output_accumulated[:max_chars] + "..."
                    break
        output_text.insert(tk.END, output_accumulated)
        output_text.yview(tk.END)  # Auto-scroll to the bottom
        output_text.update_idletasks()  # Update the GUI with the output

    stdout_thread = threading.Thread(target=read_output, args=(process.stdout,))
    
    # Start the thread to read stdout
    stdout_thread.start()
    
    # Wait for the process to complete
    process.wait()
    stdout_thread.join()

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
window.title("offline llm")

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
