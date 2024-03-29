import py_midicsv as pm
from transposer import Transposer
from analyzer import Analyzer
from plotter import Plotter

class Converter:
    """
    A class used to convert MIDI files to CSV and vice versa, with optional pitch transposition.
    """
    def __init__(self, input_file, semitones=0, output_file="loopback.mid"):
        """
        Initialize the Converter with input file, semitones for transposition, and output file.
        """
        self.input_file = input_file
        self.semitones = semitones
        self.output_file = output_file
        self.transposer = Transposer()

        self.ENCODINGS = ["utf-8", "utf-8-sig", "iso-8859-1", "latin1", "cp1252"]
        self.encoding = self.ENCODINGS[0]

    def midi_to_csv(self):
        """
        Convert MIDI to CSV and return the CSV string
        """
        csv_string = pm.midi_to_csv(self.input_file)
            
        # Convert the CSV output into a single string
        return "".join(csv_string)    

    def midi_to_csv_transpose(self):
        """
        Convert MIDI to CSV and transpose it.
        """
        csv_string = pm.midi_to_csv(self.input_file)
        transposed_csv = self.transposer.transpose(csv_string, self.semitones)
        with open(self.output_file, "w", encoding=self.encoding) as f:
            f.writelines(transposed_csv)
            
    def csv_to_midi_transpose(self):
        """
        Convert CSV to MIDI and transpose it.
        """
        with open(self.input_file, "r", encoding=self.ENCODING) as f:
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

