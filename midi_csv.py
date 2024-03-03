"""
midi-csv.py
Converts a .mid file to .csv or .csv to .mid, with optional pitch transposition.
Can also loopback test .mid to .mid

2024 Chris Derry & ChatGPT
"""

import sys
import argparse

from analyzer import Analyzer
from converter import Converter
from plotter import Plotter
from transformer import Transformer

VERSION = '0.2.0'

parser = argparse.ArgumentParser(
    description="Converts .mid to .csv or .csv to .mid, with optional pitch transposition.")
parser.add_argument('conv_mode', type=str,
    help="Conversion mode ('mid', 'csv', 'loop', 'xform')")
parser.add_argument('input_file', type=str,
    help="Input file")
parser.add_argument('--semitones', type=int,
    help="Number of semitones to transpose")
parser.add_argument('--output_file', type=str,
    help="Output file")
parser.add_argument('--plot', type=bool, default=False,
    help="Enable plotting")

args = parser.parse_args()

conv = Converter(args.input_file,
                args.output_file,
                args.semitones)

if args.plot:
    note_counts, chord_counts = Analyzer.midi_chords(args.input_file)
    print(f"note counts: {note_counts}   chord counts: {chord_counts}")
    Plotter.plot_chords(note_counts, chord_counts)

try:
    if args.conv_mode == "mid":
        conv.midi_to_csv_transpose()
    elif args.conv_mode == "csv":
        conv.csv_to_midi_transpose()
    elif args.conv_mode == "loop":
        conv.midi_loopback()
    elif args.conv_mode == "xform":
        csv_content = conv.midi_to_csv()
        Transformer.pplx_process(csv_content)
    else:
        print("Invalid mode")
        sys.exit(1)
except Exception:
    print("x")

