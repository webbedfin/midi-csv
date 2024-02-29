"""
midi-csv.py
Converts a .mid file to .csv or .csv to .mid, with optional pitch transposition.
Can also loopback test .mid to .mid

2024 Chris Derry
"""

import sys
import argparse
from collections import defaultdict
import matplotlib.pyplot as plt
import py_midicsv as pm
import mido

class Converter:
    """
    A class used to convert MIDI files to CSV and vice versa, with optional pitch transposition.
    """
    def __init__(self, input_file, semitones, output_file):
        """
        Initialize the Converter with input file, semitones for transposition, and output file.
        """
        self.input_file = input_file
        self.semitones = semitones
        self.output_file = output_file
        self.transposer = Transposer()
        self.analyzer = Analyzer()
        self.plotter = Plotter()

    def midi_to_csv_transpose(self):
        """
        Convert MIDI to CSV and transpose it.
        """
        csv_string = pm.midi_to_csv(self.input_file)
        transposed_csv = self.transposer.transpose(csv_string, self.semitones)
        with open(self.output_file, "w", encoding=self.transposer.ENCODING) as f:
            f.writelines(transposed_csv)

    def csv_to_midi_transpose(self):
        """
        Convert CSV to MIDI and transpose it.
        """
        with open(self.input_file, "r", encoding=self.transposer.ENCODING) as f:
            csv_data = f.readlines()   
        transposed_csv = self.transposer.transpose(csv_data, self.semitones)
        midi = pm.csv_to_midi(transposed_csv)
        with open(self.output_file, "wb") as midi_file:
            pm.FileWriter(midi_file).write(midi)

    def midi_loopback(self):
        """
        Perform a loopback test from MIDI to MIDI.
        """
        csv = pm.midi_to_csv(self.input_file)
        midi = pm.csv_to_midi(csv)
        with open(self.output_file, "wb") as midi_file:
            pm.FileWriter(midi_file).write(midi)

    def midi_csv_convert(self, conv_mode):
        """
        Convert MIDI to CSV or CSV to MIDI based on the conversion mode.
        """
        modes = {"mid": self.midi_to_csv_transpose,
                 "csv": self.csv_to_midi_transpose, 
                 "loop": self.midi_loopback}
        process = modes.get(conv_mode)

        if process is None:
            print("Invalid input type.")
            sys.exit(1)

        try:
            process()
            note_counts, chord_counts = self.analyzer.analyze_chords(self.output_file)
            self.plotter.plot_chords(note_counts, chord_counts)
        except Exception as e:
            print(f"An error occurred: {e}")

class Transposer:
    """
    A class used to transpose MIDI notes.
    """
    def __init__(self):
        """
        Initialize the Transposer with a list of possible encodings.
        """
        self.encodings = ["utf-8", "utf-8-sig", "iso-8859-1", "latin1", "cp1252"]
        self.ENCODING = self.encodings[0]

    def transpose_note_in_row(self, row, interval):
        """
        Transpose a note in a row by a given interval.
        """
        parts = row.strip().split(", ")
        if "Note_on_c" in row or "Note_off_c" in row:
            note = int(parts[4])
            min_midi, max_midi = 0, 127  # Ensure note is within MIDI range
            transposed_note = min(max(min_midi, note + interval), max_midi)
            parts[4] = str(transposed_note)
            row = ", ".join(parts)
        return row

    def transpose(self, csv_data, interval):
        """
        Transpose all notes in a CSV data by a given interval.
        """
        return [self.transpose_note_in_row(row, interval) for row in csv_data]

class Analyzer:
    """
    A class used to analyze chords from a MIDI file.
    """
    def note_number_to_name(self, note_number):
        """
        Convert MIDI note numbers to note names.
        """
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        return note_names[note_number % 12] # + str(note_number // 12 - 1)

    def analyze_chords(self, midi_path):
        """
        Analyze chords from a MIDI file.
        """
        mid = mido.MidiFile(midi_path)
        note_counts = defaultdict(int)
        chord_counts = defaultdict(int)
        total_notes = 0
        total_chords = 0
        
        # Set to hold currently active notes
        active_notes = set()

        # chord definition
        chord_note_count = [2, 3, 4]

        # Process each track in the MIDI file
        for track in mid.tracks:
            for msg in track:
                if msg.type == 'note_on' and msg.velocity > 0:
                    # Note on
                    active_notes.add(msg.note)
                elif (msg.type == 'note_off') or (msg.type == 'note_on' and msg.velocity == 0):
                    # Note off
                    if msg.note in active_notes:
                        note_counts[self.note_number_to_name(msg.note)] += 1
                        total_notes += 1
                        active_notes.remove(msg.note)
                        # When a note is released, check if there are any other notes being played
                        if active_notes:
                            # Sort unique notes to ensure consistent chord naming
                            note_names = [self.note_number_to_name(note) for note in active_notes]
                            # Convert to set to remove duplicates, then sort
                            unique_note_names = sorted(set(note_names))  
                            chord = '+'.join(unique_note_names)
                            if len(unique_note_names) in chord_note_count:
                                chord_counts[chord] += 1
                                total_chords += 1

        return note_counts, chord_counts


class Plotter:
    """
    A class used to plot chord and note histograms.
    """
    def plot_chords(self, note_counts, chord_counts):
        """
        Plot chord and note histograms.
        """
        max_chord_count = max(chord_counts.values())

        # Now we have the counts of each chord, we can plot a histogram
        histogram_count = max_chord_count / 3
        chord_names = [chord for chord in chord_counts.keys() if chord_counts[chord] >= histogram_count]
        chord_values = [chord_counts[chord] for chord in chord_names if chord_counts[chord] >= histogram_count]

        _, axs = plt.subplots(2)

        axs[0].bar(chord_names, chord_values)
        axs[0].set_title('Chord Histogram')

        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        note_values = [note_counts[note] for note in note_names]

        axs[1].bar(note_names, note_values)
        axs[1].set_title('Note Histogram')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
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

    converter = Converter(args.input_file, args.semitones, args.output_file)
    converter.midi_csv_convert(args.conv_mode)