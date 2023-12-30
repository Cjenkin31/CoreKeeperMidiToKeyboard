# Derrived from https://steamcommunity.com/app/1621690/discussions/0/5514142341105205082/
import tkinter as tk
from tkinter import ttk
import mido
from pynput.keyboard import Controller
import threading

# Create a dictionary to map MIDI notes to keyboard keys
midi_to_key = {
    48: 'z',  # C3
    49: 's',  # C#3/D♭3
    50: 'x',  # D3
    51: 'd',  # D#3/E♭3
    52: 'c',  # E3
    53: 'v',  # F3
    54: 'g',  # F#3/G♭3
    55: 'b',  # G3
    56: 'h',  # G#3/A♭3
    57: 'n',  # A3
    58: 'j',  # A#3/B♭3
    59: 'm',  # B3
    60: 'q',  # C4
    61: '2',  # C#4/D♭4
    62: 'w',  # D4
    63: '3',  # D#4/E♭4
    64: 'e',  # E4
    65: 'r',  # F4
    66: '5',  # F#4/G♭4
    67: 't',  # G4
    68: '6',  # G#4/A♭4
    69: 'y',  # A4
    70: '7',  # A#4/B♭4
    71: 'u',  # B4
}

# Function to find MIDI inputs and update the dropdown
def find_midi_inputs():
    midi_inputs = mido.get_input_names()
    midi_input_dropdown['values'] = midi_inputs
    if midi_inputs:
        midi_input_dropdown.current(0)

# Function to start processing MIDI input in a new thread
def start_script():
    selected_input = midi_input_var.get()
    if selected_input:
        threading.Thread(target=run_script, args=(selected_input,), daemon=True).start()


# Function to update the key label in the GUI
def update_label(note):
    if note in midi_to_key:
        key_label.config(text=f"Most recent key: {midi_to_key[note]}")
    else:
        key_label.config(text="Key not mapped")

# The main script that processes MIDI input
def run_script(input_name):
    keyboard = Controller()
    with mido.open_input(input_name) as midi_input:
        for msg in midi_input:
            if msg.type == 'note_on' and msg.velocity > 0 and msg.note in midi_to_key:
                keyboard.press(midi_to_key[msg.note])
                update_label(msg.note)
            elif (msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)) and msg.note in midi_to_key:
                keyboard.release(midi_to_key[msg.note])

# Initialize the GUI application
app = tk.Tk()
app.title("MIDI to Keyboard Mapper")
app.geometry("400x200")

# Add GUI components
find_button = ttk.Button(app, text="Find MIDI Inputs", command=find_midi_inputs)
find_button.pack(pady=10)

midi_input_var = tk.StringVar()
midi_input_dropdown = ttk.Combobox(app, textvariable=midi_input_var)
midi_input_dropdown.pack(pady=10)

start_button = ttk.Button(app, text="Start", command=start_script)
start_button.pack(pady=10)

key_label = tk.Label(app, text="Most recent key: None")
key_label.pack(pady=10)

# Start the GUI event loop
app.mainloop()
