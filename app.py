import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import os

def on_button_click():
  # Get user input from the entry boxes
  attribute = attribute_entry.get()

  # Get user's home directory and current working directory to generate the correct paths
  home_dir = os.path.expanduser("~")

  # Generate the schema file path and Fabric path
  file_path = os.path.join(home_dir, "Documents/fabric-app/schemas", file_entry.get() + ".json") 
  fabric_path = os.path.join(home_dir, "go/bin/fabric")

  # Check if the Fabric file exists
  if not os.path.exists(fabric_path):
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Error: Fabric not found at {fabric_path}\n")
    return

  # Check if a file name is provided
  if not attribute:
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Error: Please enter a file name\n")
    return

  # Check if the file_path is a file
  if not os.path.isfile(file_path):
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Error: File not found at {file_path}\n")
    return
  
  # Check if an attribute is provided
  if not attribute:
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Error: Please enter an attribute\n")
    return

  # Construct the command using the user input
  command = f'(cat {file_path}; echo "attribute: {attribute}") | {fabric_path} --model gpt-4o -sp map_prompt'
  print(command)
  try:
    # Run the command and capture the output
    result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    
    # Clear previous output
    output_text.delete(1.0, tk.END)

    # Show the output in the text widget
    output_text.insert(tk.END, result.stdout)

  except subprocess.CalledProcessError as e:
    # Clear previous output
    output_text.delete(1.0, tk.END)
    
    # Show error message in the text widget
    output_text.insert(tk.END, "Error occurred:\n")
    output_text.insert(tk.END, "========================\n")
    output_text.insert(tk.END, f'Error: {e}\nOutput: {e.output}')

# Create the main window
root = tk.Tk()
root.title("Mapping With Fabric")

# Set initial window size
window_width = 800
window_height = 600

# Get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the position of the window to center it
position_top = int(screen_height/2 - window_height/2)
position_right = int(screen_width/2 - window_width/2)

# Set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Create a Message widget for the instructions
instruction_text = (
  "This user interface allows you to interact with Fabric to map API attributes. "
  "Ensure you have Fabric installed and have specified the path to the Fabric executable in the app.py file.\n\n"
  "Instructions:\n"
  "    1. Enter the name of the JSON schema you want to map to.\n"
  "    2. Specify the attribute you wish to map.\n\n"
  "Once you submit this information, it will be sent to the GPT-4o model via Fabric, "
  "which will return the top three closest matches for the logical mapping."
)
instructions_message = tk.Message(root, text=instruction_text, width=600, justify=tk.LEFT)
instructions_message.pack(pady=(30, 10))

# Create a label and entry for the file path
file_path_label = tk.Label(root, text="Enter the file name:")
file_path_label.pack(pady=(20,10))

file_entry = tk.Entry(root, width=50)
file_entry.pack(pady=(0,10))

# Create a label and entry for the attribute
attribute_label = tk.Label(root, text="Enter an attribute:")
attribute_label.pack(pady=10)

attribute_entry = tk.Entry(root, width=50)
attribute_entry.pack(pady=(0,10))

# Create a submit button
button = tk.Button(root, text="Submit", command=on_button_click)
button.pack(pady=(10,20))

# Create a scrolled text widget for output
output_text = scrolledtext.ScrolledText(root, width=65, height=10, wrap=tk.WORD)
output_text.pack(pady=10)

# Start the main loop
root.mainloop()
