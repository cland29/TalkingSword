import os
from pydub import AudioSegment

# Input and output directories
input_folder = "output_audio"  # Folder containing the original .wav files
output_folder = "converted_wav_files"  # Folder to save the converted .wav files

# Ensure the output directory exists
os.makedirs(output_folder, exist_ok=True)

# Process each .wav file in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".wav"):
        print(filename)
    if filename.lower().endswith(".wav"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        print(filename)
        # Load the audio file
        # Check if the file exists
        if not os.path.exists(input_path):
            print(f"Error: File not found: {input_path}")
            continue

        # Load the audio file
        try:
            audio = AudioSegment.from_file(input_path)

            # Convert to stereo if not already
            if audio.channels != 2:
                audio = audio.set_channels(2)

            # Set sample rate to 44100 Hz
            audio = audio.set_frame_rate(44100)

            # Export with Signed 16-bit PCM encoding
            audio.export(output_path, format="wav", parameters=["-acodec", "pcm_s16le"])
            print(f"Converted: {filename} -> {output_path}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("Conversion complete!")