from collections import defaultdict
import mido

class Analyzer:
    """
    A class used to analyze chords from a MIDI file.
    """
    @staticmethod
    def _note_number_to_name(self, note_number):
        """
        Convert MIDI note numbers to note names.
        """
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        return note_names[note_number % 12] # + str(note_number // 12 - 1)

    @staticmethod
    def midi_chords(self, midi_path):
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
        chord_note_count = [3, 4]

        # Process each track in the MIDI file
        for track in mid.tracks:
            for msg in track:
                if msg.type == 'note_on' and msg.velocity > 0:
                    # Note on
                    active_notes.add(msg.note)
                elif (msg.type == 'note_off') or (msg.type == 'note_on' and msg.velocity == 0):
                    # Note off
                    if msg.note in active_notes:
                        note_counts[self._note_number_to_name(msg.note)] += 1
                        total_notes += 1
                        active_notes.remove(msg.note)
                        # When a note is released, check if there are any other notes being played
                        if active_notes:
                            # Sort unique notes to ensure consistent chord naming
                            note_names = [self._note_number_to_name(note) for note in active_notes]
                            # Convert to set to remove duplicates, then sort
                            unique_note_names = sorted(set(note_names))  
                            chord = '+'.join(unique_note_names)
                            if len(unique_note_names) in chord_note_count:
                                chord_counts[chord] += 1
                                total_chords += 1

        return note_counts, chord_counts
