from gtts import gTTS
import os

# Function to generate TTS for a line of text
def text_to_speech(line, filename):
    tts = gTTS(text=line, lang='en')  # You can change 'en' to another language if needed
    tts.save(filename)

# Input and output directories
input_file = "input.txt"  # Path to the input text file
output_dir = "output_audio"  # Directory to save the .wav files

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Read the text file and process each line
with open(input_file, 'r') as file:
    for i, line in enumerate(file):
        line = line.strip()  # Remove leading/trailing whitespace
        if line:  # Skip empty lines
            output_filename = os.path.join(output_dir, f"line_{i + 1}.wav")
            print(f"Generating TTS for line {i + 1}: {line}")
            text_to_speech(line, output_filename)

print(f"Audio files saved in {output_dir}")
