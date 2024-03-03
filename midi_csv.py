"""
midi-csv.py
Converts a .mid file to .csv or .csv to .mid, with optional pitch transposition.
Can also loopback test .mid to .mid

2024 Chris Derry & ChatGPT
"""

import sys
import os
import argparse
from collections import defaultdict

import mido
from openai import OpenAI
from converter import Converter
from transformer import Transformers

def midi_csv_convert(self, conv_mode, plot=False):
    """
    Convert MIDI to CSV or CSV to MIDI based on the conversion mode.
    """
    modes = {"mid": self._midi_to_csv_transpose,
                "csv": self._csv_to_midi_transpose, 
                "loop": self._midi_loopback}
    process = modes.get(conv_mode)
    if process is None:
        print("Invalid input type.")
        sys.exit(1)

    try:
        process()
    except Exception:
        print("x")
    
    if plot:
        note_counts, chord_counts = self.analyzer.analyze_chords(self.input_file)
        print(f"note counts: {note_counts}   chord counts: {chord_counts}")
        self.plotter.plot_chords(note_counts, chord_counts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Converts .mid to .csv or .csv to .mid, with optional pitch transposition.")
    parser.add_argument('conv_mode', type=str,
                        help="Conversion mode ('mid', 'csv', 'loop', 'xform')")
    parser.add_argument('input_file', type=str,
                        help="Input .mid/.csv file")
    parser.add_argument('--semitones', type=int,
                        help="Number of semitones to transpose")
    parser.add_argument('--output_file', type=str,
                        help="Output .csv/.mid file")
    parser.add_argument('--plot', type=bool, default=False,
                        help="Enable plotting")

    args = parser.parse_args()

    if args.conv_mode == "xform":
        Transformer.process(args.input_file)
    else:
        Converter(args.input_file,
                  args.output_file,
                  args.semitones).midi_csv_convert(args.conv_mode, args.plot)
