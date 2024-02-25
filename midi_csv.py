"""
midi-csv.py
Converts a .mid file to .csv or .csv to .mid, with optional pitch transposition.
Can also loopback test .mid to .mid

2024 Chris Derry
"""

import sys
import argparse
import py_midicsv as pm

encodings = ["utf-8",
             "utf-8-sig", 
             "iso-8859-1", 
             "latin1", 
             "cp1252"]
ENCODING = encodings[0]

def transpose_note_in_row(row, interval):
    """Transpose note by number of semitones."""
    parts = row.strip().split(", ")
    if "Note_on_c" in row or "Note_off_c" in row:
        note = int(parts[4])
        min_midi, max_midi = 0, 127  # Ensure note is within MIDI range
        transposed_note = min(max(min_midi, note + interval), max_midi)
        parts[4] = str(transposed_note)
        row = ", ".join(parts)
    return row

def transpose(csv_data, interval):
    """Transpose all notes in CSV"""
    return [transpose_note_in_row(row, interval) for row in csv_data]

def midi_to_csv_transpose(input_midi, interval, output_csv):
    """Convert MIDI to CSV + transpose """
    csv_string = pm.midi_to_csv(input_midi)
    transposed_csv = transpose(csv_string, interval)
    with open(output_csv, "w", encoding=ENCODING) as f:
        f.writelines(transposed_csv)
    return 0

def csv_to_midi_transpose(input_csv, interval, output_midi):
    """Convert CSV to MIDI CSV + transpose """
    with open(input_csv, "r", encoding=ENCODING) as f:
        csv_data = f.readlines()   
    transposed_csv = transpose(csv_data, interval)
    midi = pm.csv_to_midi(transposed_csv)
    with open(output_midi, "wb") as midi_file:
        pm.FileWriter(midi_file).write(midi)

def midi_loopback(input_midi, _, output_midi):
    """Loopback: convert MIDI to CSV to MIDI """
    csv = pm.midi_to_csv(input_midi)
    midi = pm.csv_to_midi(csv)
    with open(output_midi, "wb") as midi_file:
        pm.FileWriter(midi_file).write(midi)

def midi_csv_convert():
    """ main """
    parser = argparse.ArgumentParser(
        description="Converts .mid to .csv or .csv to .mid, with optional pitch transposition.")
    parser.add_argument('conv_mode', type=str,
                        help="Conversion mode ('mid', 'csv', 'loop')")
    parser.add_argument('input_file', type=str,
                        help="Input .mid/.csv file")
    parser.add_argument('semitones', type=int,
                        help="Number of semitones to transpose")
    parser.add_argument('output_file', type=str,
                        help="Output .csv/.mid file")
    args = parser.parse_args()

    modes = {"mid": midi_to_csv_transpose,
             "csv": csv_to_midi_transpose, 
             "loop": midi_loopback}
    process = modes.get(args.conv_mode)

    if process is None:
        print("Invalid input type.")
        sys.exit(1)

    try:
        process(args.input_file, args.semitones, args.output_file)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    midi_csv_convert()
    
