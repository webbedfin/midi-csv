import sys
import py_midicsv as pm

def transpose_notes(csv_data, interval):
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

def midi_to_csv_transpose(midi_file, interval, output_csv):
    csv_string = pm.midi_to_csv(midi_file)
    transposed_csv = transpose_notes(csv_string, interval)
    with open(output_csv, "w") as f:
        f.writelines(transposed_csv)

def csv_to_midi_transpose(input_csv, interval, output_midi):
    with open(input_csv, "r") as f:
        csv_data = f.readlines()
    transposed_csv = transpose_notes(csv_data, interval)
    midi = pm.csv_to_midi(transposed_csv)
    with open(output_midi, "wb") as midi_file:
        midi_writer = pm.FileWriter(midi_file)
        midi_writer.write(midi)

def midi_loopback(midi_file, output_midi):
    csv = pm.midi_to_csv(midi_file)    
    midi = pm.csv_to_midi(csv)
    with open(output_midi, "wb") as midi_file:
        midi_writer = pm.FileWriter(midi_file)
        midi_writer.write(midi)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python midi-csv.py <input_type> <input_file> <semitones> <output_file>")
        print("<input_type> should be 'midi' or 'csv'")
        sys.exit(1)

    input_type = sys.argv[1]
    input_file = sys.argv[2]
    semitones = int(sys.argv[3])
    output_file = sys.argv[4]

    if input_type == "midi":
        midi_to_csv_transpose(input_file, semitones, output_file)
    elif input_type == "csv":
        csv_to_midi_transpose(input_file, semitones, output_file)
    elif input_type == "loop":
        midi_loopback(input_file, output_file)
    else:
        print("Invalid input type. Use 'midi' or 'csv'.")