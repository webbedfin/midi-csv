import matplotlib.pyplot as plt

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