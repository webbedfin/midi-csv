import sys
import py_midicsv as pm

def main():
    # Check if a MIDI file name was provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python midi-csv.py <midi_file_name>")
        sys.exit(1)
    
    midi_file_name = sys.argv[1]

    # Load the MIDI file and parse it into CSV format
    csv_string = pm.midi_to_csv(midi_file_name)

    # Save the CSV output to a file
    with open("example_converted.csv", "w") as f:
        f.writelines(csv_string)

if __name__ == "__main__":
    main()