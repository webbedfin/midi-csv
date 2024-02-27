""" Look for .mid files we can convert to CSV and back """

import os
import sys
from midi_csv import midi_loopback

def sweep_directory(directory: str):
    """
    Function to sweep through all subfolders in a directory, 
    convert all files to midi and dump as 'junk.mid'
    
    Args:
    directory (str): The directory to sweep
    """
    fails = 0
    succeeds = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                status = midi_loopback(filepath, 0, "junk.mid")
            except Exception:
                #print(f"An error occurred: {e}")
                fails += 1 
            else:
                print(filepath)
                succeeds += 1
           
    print(f"{fails} failures, {succeeds} successes")
    
if __name__ == "__main__":
    root_folder = sys.argv[1]
    sweep_directory(root_folder)

