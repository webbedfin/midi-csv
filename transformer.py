"""
A class to make pplx API calls 
"""
import sys
import os
from openai import OpenAI

class Transformer:
    def __init__(self):
       self.API_KEY = os.environ.get('PPLX_API_KEY')
    
    def pplx_process(self, csv_content, note_counts, chord_counts):
        # truncate the string to the 16384 token limit
        csv1 = csv_content[:16384]
        csv2 = csv_content[16384:32768]

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an artificial intelligence assistant and you are an expert"
                    "in music theory and MIDI, including the CSV format that the python library"
                    "py_midicsv works with, as that is what we shall be working with."
                    "carefully, step-by-stepw, convert this information into a timeline that"
                    "I'm going to want you to analyze a CSV representations of a MIDI file and"
                    "can be used with music theory. This will be a CSV-like."
                    "When you have this, interpret what each note and chord mean in relation"
                    "those those preceding and those following. Use your MIDI expertise"
                    "on how MIDI note on and note off messages mean to detmermine"
                    "the durations of the notes and the chords that are being played."
                    "Take a first pass and go through note by note to get a feel for the"
                    "rhythm and how it changes, and for how the chords (or lack thereof) create a"
                    "harmonic structure. Then, take a second pass to determine the melody (or "
                    "lack thereof). From what you know of various music theoretical systems look"
                    "for anything interesting or novel as you reexamine the music"
                    "and include this in your report."
                    "As you do this, note where you think the song sections are and name then."
                    "If you can't, it is ok to simply use names like 'A' or 'B'" 
                    "Try to determine the genre and other extended information about the piece"
                    "of music, such cultural influences, approximate age, origin, etc."
                    "I am interested in your analysis, observations and insights."
                    "I am mostly interested in musical observations, but technical"
                    "concerns and curiosities should be noted as well. For technical issues"
                    "that you think are irrelevant, you can ignore them but note at the end"
                    "if you find more than 5 or so. Many MIDI files have issues with them that"
                    "prevent py_midicsv from converting from CSV format back to MIDI format."
                    "If you encounter any of these issues, try your best to fix the error."
                    "If you or if you cannot, then alert me. Hold your analysis until I indicate"
                    "I indicate that I have finished sending you relevant data."
                    "Break up your analysis into sections:"
                    "1) high level analysis of the piece of music."
                    "Discuss its tempo, key and chord changes. Talk about melody, harmony, and rhythm."
                    "likely genre, any prominent tonal relationships or lack thereof. Discuss intent of sections, likely emotional"
                    "impact, and traditional music analysis that may be taught at a graduate music school."
                    "Elaborate with as much traditional Western music theory analysis as you can."
                    "Tell me the bpm, and make sure convert it to beats per minute. If bpm is less than"
                    "10 or more than 500, then it is likely an error. If you find an error, try to fix it."
                    "2) talk about"
                    "interesting sections you find, chosen by in a way that shows uniqueness, difficulty, or beauty."
                    "3) describe musical ideas inspired by this music I could pursue, ideally written out as short guitar"
                    "tablature examples. 4) suggest music by other musicians who sound similar or pursue similar methods."
                    "5) discuss any technical issues you encountered and how you resolved them."
                    "6) Consider non Western music such as African music, Asian music and music around the world."
                    "If you notice close similarities in a piece of music to some very different style point that out."
                    "Consider advanced musical theory in your analysis, including western tonal or atonal theory, church music," 
                    "baroque, classical, romantic, high romantic, impressionism, expressionsm, post-impressionisn, ragtime, blues,"
                    "country, bluegrass, jazz, western swing, rock, microtonality, spectralism, hyperspectralism, stable music,"
                    "minimalism, soul, funk, thrash, death metal, metal, blues rock, shred, pop, hip hop, EDM, etc."
                    "When I have sent you the data give me your analysis."
                  ),
            },     
            {   
                "role": "user",
                "content": "Here is part 1 of 2 of the CSV-formatted MIDI data: " + csv1
            },
            #{   
            #    "role": "user",
            #    "content": "Here is part 2 of 2 of the CSV-formatted MIDI data: " + csv2
            #},
            #{   
            #    "role": "assistant",
            #    "content": "I have finished sending you the data. Be verbose, creative, and give me your analysis now."
            #},

            # {
            #     "role": "user",
            #     "content": (
            #         "Here is some additional information that was created with the python library mido"
            #         "python library. It consists of a tuple of python dictionaries which contain a crude harmonic"
            #         "analysis that you may want to use a reference to supplement your understanding of the MIDI data."
            #         "They were created using the python library mido. The first dictionary contains a count of all notes"
            #         "played in the piece of music, and the second dictionary contains a count of all chords played."
            #         "These can be used as histograms, but do not contain any timing information."
            #         "Note that the chord names are untraditional and are instead are the collection of the names"
            #         "of all of the notes present. This means that each chord will have very precise voicings."
            #         "Any patterns you notice emerging from your analysis of how these chords are used and how they"
            #         "develop should be prominent in your analysis. "
            #         "Make sure you understand the rhythmic structure well when examining the CSV-MIDI formatted data,"
            #         "and try to draw from all sources to create your understanding of the piece of music."
            #         + harmonic_analysis,
            #     ),
            # },
   
        ]

        client = OpenAI(api_key=self.API_KEY, base_url="https://api.perplexity.ai")

        ml_model = ["sonar-medium-online",
                "mixtral-8x7b-instruct",
                "mistral-7b-instruct"]
        ml_model_idx = 1

        stream = False
        if stream:
            sys.exit(1)

            # For chat completion with streaming
            response_stream = client.chat.completions.create(
                model=ml_model[ml_model_idx],
                messages=messages,
                stream=True,
            )
            for response in response_stream:
                 print(response)

        else:
            # For chat completion without streaming
            response = client.chat.completions.create(
                model=ml_model[ml_model_idx],
                messages=messages,
            )
            print(response.choices[0].message.content)

        