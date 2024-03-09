"""
midi_cobbler.py
- convert .mid file to/from .csv 
- transpose pitch in csv domain
- loopback test .mid to .mid
- GPT analysis mode

2024 Chris Derry & ChatGPT
"""

import sys
import argparse

from analyzer import Analyzer
from converter import Converter
from plotter import Plotter
from transformer import Transformer

VERSION = '0.1.0'

parser = argparse.ArgumentParser(
    description="MidiCobbler: A MIDI file conversion and ML analysis tool.")
parser.add_argument('mode', type=str,
    help="Conversion mode ('mid', 'csv', 'loop', 'xform')")
parser.add_argument('input_file', type=str,
    help="Input file")
parser.add_argument('--semitones', type=int, default = 0,
    help="Number of semitones to transpose")
parser.add_argument('--output_file', type=str, default = "loopback.mid",
    help="Output file")
parser.add_argument('--plot', type=bool, default=False,
    help="Enable plotting")

args = parser.parse_args()

conv = Converter(args.input_file,
                args.output_file,
                args.semitones)

note_counts, chord_counts = Analyzer().midi_chords(args.input_file)

if args.plot:
    print(f"note counts: {note_counts}   chord counts: {chord_counts}")
    Plotter.plot_chords(note_counts, chord_counts)

try:
    if args.mode == "mid":
        conv.midi_to_csv_transpose()
    elif args.mode == "csv":
        conv.csv_to_midi_transpose()
    elif args.mode == "loop":
        conv.midi_loopback()
    elif args.mode == "xform":
        Transformer().pplx_process(conv.midi_to_csv(), note_counts, chord_counts)
        #midi_csv = conv.midi_to_csv()
        #TransformerSimple().pplx_process(midi_csv)
    else:
        print("Invalid mode")
        sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    #print("x")

