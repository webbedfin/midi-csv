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
    midi_data = pm.csv_to_midi(transposed_csv)
    with open(output_midi, "wb") as midi_file:
        midi_file.write(midi_data)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python script.py <mode> <input_file> <semitones> <output_file>")
        print("<mode> should be 'midi-to-csv' or 'csv-to-midi'")
        sys.exit(1)

    mode = sys.argv[1]
    input_file = sys.argv[2]
    semitones = int(sys.argv[3])
    output_file = sys.argv[4]

    if mode == "midi-to-csv":
        midi_to_csv_transpose(input_file, semitones, output_file)
    elif mode == "csv-to-midi":
        csv_to_midi_transpose(input_file, semitones, output_file)
    else:
        print("Invalid mode. Use 'midi-to-csv' or 'csv-to-midi'.")