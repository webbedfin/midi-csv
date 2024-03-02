import unittest
from collections import defaultdict
from midi_csv import analyze_chords

class TestAnalyzeChords(unittest.TestCase):
    def test_analyze_chords(self):
        # Define a sample MIDI file path79
        midi_path = "fight4right.mid"

        # Call the analyze_chords function
        note_counts, chord_counts = analyze_chords(midi_path)

        # Assert the expected results
        expected_note_counts = defaultdict(int)
        expected_chord_counts = defaultdict(int)

        # Update the expected note counts and chord counts based on your test case
        expected_note_counts["C"] = 1
        expected_chord_counts["C+E+G"] = 1

        self.assertEqual(note_counts, expected_note_counts)
        self.assertEqual(chord_counts, expected_chord_counts)

if __name__ == '__main__':
    unittest.main()