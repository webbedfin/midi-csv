class Transformer:
    def process(midi_path):
        """
        A class to make pplx API calls 
        """

        # Load the MIDI file and parse it into CSV format
        csv_string = pm.midi_to_csv(midi_path)

        # Convert the CSV output into a single string
        csv_content = "".join(csv_string)

        # truncate the string to the 16384 token limit
        csv_content = csv_content[:16384]

        API_KEY = os.environ.get('PPLX_API_KEY')
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an artificial intelligence assistant and you are an expert"
                    "in all things MIDI, including the CSV format that the python library"
                    "py_midicsv uses, as that is what we shall be using."
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
                ),
            },
            {
                "role": "user",
                "content": csv_content,
            },
        ]

        client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

        # For chat completion without streaming
        response = client.chat.completions.create(
            model="mistral-7b-instruct",
            messages=messages,
        )
        print(response.choices[0].message.content)

        # For chat completion with streaming
        # response_stream = client.chat.completions.create(
        #     model="mistral-7b-instruct",
        #     messages=messages,
        #     stream=True,
        # )
        # for response in response_stream:
        #     print(response)