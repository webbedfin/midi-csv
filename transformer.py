"""
A class to make pplx API calls 
"""
import sys
from openai import OpenAI

class Transformer:
    __init__(self):
        self.API_KEY = os.environ.get('PPLX_API_KEY')
    
    def pplx_process(self, csv_content):

        # truncate the string to the 16384 token limit
        little_csv = csv_content[:16384]

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an artificial intelligence assistant and you are an expert"
                    "in all things MIDI, including the CSV format that the python library"
                    "py_midicsv works with, as that is what we shall be using."
                    "I'm going to want you to analyze CSV representations of MIDI files and"
                    "reflect on what you know about how note on and off works to detmermine"
                    "the length of the notes and the chords that are being played."
                    "Take a first pass through to get a feel how the chords create a harmonic"
                    "structure and then take a second pass to determine the melody."
                    "As you do this, note where you think the song sections are and name then"
                    "Try to determine the genre of the song."
                    "After you have done this, I want you to report on your observations."
                    "I am more interested in purely musical observations, but technical"
                    "concerns and curiosities should be noted as well. For technical issues"
                    "that you think are irrelevant, you can ignore them but note at the end"
                    "if you find more than 5 or so."
                    "Many MIDI files have issues with them that prevent py_midicsv from converting"
                    "from CSV format back to MIDI format. If you encounter any of these issues,"
                    "try your best to fix the error. If you cannot, then alert me."
                ),
            },
            {
                "role": "user",
                "content": little_csv,
            },
        ]

        client = OpenAI(api_key=self.API_KEY, base_url="https://api.perplexity.ai")

        stream = false
        if stream:
            sys.exit(1)

            # For chat completion with streaming
            response_stream = client.chat.completions.create(
                model="mistral-7b-instruct",
                messages=messages,
                stream=True,
            )
            for response in response_stream:
                 print(response)

        else:
            # For chat completion without streaming
            response = client.chat.completions.create(
                model="mistral-7b-instruct",
                messages=messages,
            )
            print(response.choices[0].message.content)

        