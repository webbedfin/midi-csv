"""
midi-csv.py
Converts a .mid file to .csv or .csv to .mid, with optional pitch transposition

2024 Chris Derry
"""

import sys
import py_midicsv as pm

encodings = ["utf-8",
             "utf-8-sig", 
             "iso-8859-1", 
             "latin1", 
             "cp1252"]
ENCODING = encodings[0]

def transpose_notes(csv_data, interval):
    """Transpoke all notes by number of semitones."""
    transposed_data = []
    for row in csv_data:
        if "Note_on_c" in row or "Note_off_c" in row:
            parts = row.strip().split(", ")
            note = int(parts[4])
            transposed_note = max(0, min(127, note + interval))  # Ensure note is within MIDI range
            parts[4] = str(transposed_note)
            row = ", ".join(parts)
        transposed_data.append(row)
    return transposed_data

def midi_to_csv_transpose(input_midi, interval, output_csv):
    """Convert MIDI to CSV + transpose """
    csv_string = pm.midi_to_csv(input_midi)
    transposed_csv = transpose_notes(csv_string, interval)
    with open(output_csv, "w", encoding=ENCODING) as f:
        f.writelines(transposed_csv)

def csv_to_midi_transpose(input_csv, interval, output_midi):
    """Convert CSV to MIDI CSV + transpose """
    with open(input_csv, "r", encoding=ENCODING) as f:
        csv_data = f.readlines()
    transposed_csv = transpose_notes(csv_data, interval)
    midi = pm.csv_to_midi(transposed_csv)
    with open(output_midi, "wb", encoding=ENCODING) as midi_file:
        midi_writer = pm.FileWriter(midi_file)
        midi_writer.write(midi)

def midi_loopback(input_midi, output_midi):
    """Loopback: convert MIDI to CSV to MIDI """
    csv = pm.midi_to_csv(input_midi)
    midi = pm.csv_to_midi(csv)
    with open(output_midi, "wb", encoding=ENCODING) as midi_file:
        midi_writer = pm.FileWriter(midi_file)
        midi_writer.write(midi)


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python midi-csv.py <input_type> <input_file> <semitones> <output_file>")
        print("<input_type> should be 'mid', 'csv' or 'loop' (mid->mid)")
        sys.exit(1)

    input_type = sys.argv[1]
    input_file = sys.argv[2]
    semitones = int(sys.argv[3])
    output_file = sys.argv[4]

    if input_type == "mid":
        midi_to_csv_transpose(input_file, semitones, output_file)
    elif input_type == "csv":
        csv_to_midi_transpose(input_file, semitones, output_file)
    elif input_type == "loop":
        midi_loopback(input_file, output_file)
    else:
        print("Invalid input type.")
