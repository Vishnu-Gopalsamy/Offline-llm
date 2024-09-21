import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading

def run_command(command):
    """ Run a command and return the output. """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout
        error = result.stderr
        return output, error
    except Exception as e:
        return "", f"Error: {e}"

def initial_command():
    """ Run the initial command when the GUI starts. """
    output, error = run_command("ollama run llama2")
    output_text.config(state=tk.NORMAL)  # Enable editing
    if output:
        output_text.insert(tk.END, output + "\n")
    if error:
        output_text.insert(tk.END, error + "\n")
    output_text.config(state=tk.DISABLED)  # Disable editing
    output_text.yview(tk.END)  # Scroll to the end

def ask_question():
    """ Handle user input and run a command. """
    question = input_field.get()
    if question.strip():
        output_text.config(state=tk.NORMAL)  # Enable editing
        output_text.insert(tk.END, f"Processing question: {question}\n")
        output_text.config(state=tk.DISABLED)  # Disable editing
        # Run the command in a separate thread to avoid blocking the GUI
        threading.Thread(target=lambda: run_command("ollama run llama2"), daemon=True).start()
    else:
        output_text.config(state=tk.NORMAL)  # Enable editing
        output_text.insert(tk.END, "Please enter a question.\n")
        output_text.config(state=tk.DISABLED)  # Disable editing

# Create the main window
root = tk.Tk()
root.title("Command Runner GUI")

# Create a text widget to display output
output_text = scrolledtext.ScrolledText(root, width=80, height=20, state=tk.DISABLED)
output_text.pack()

# Create an input field
input_field = tk.Entry(root, width=80)
input_field.pack()

# Create a button to ask a question
ask_button = tk.Button(root, text="Ask", command=ask_question)
ask_button.pack()

# Run the initial command when the GUI starts
root.after(100, initial_command)

# Run the Tkinter event loop
root.mainloop()
