class Transposer:
    """
    A class used to transpose MIDI notes.
    """
    @staticmethod
    def _transpose_note_in_row(self, row, interval):
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
        return [self._transpose_note_in_row(row, interval) for row in csv_data]
    