def wav8bit_to_bin(input_wav, output_bin):
    with open(input_wav, 'rb') as wav_file:
        wav_file.seek(44)  # Skip the standard 44-byte header
        raw_data = wav_file.read()  # Get the raw PCM data

    with open(output_bin, 'wb') as bin_file:
        bin_file.write(raw_data)

    print(f"8-bit PCM data extracted to '{output_bin}'")

wav8bit_to_bin("audio.wav", "audio_16K.bin")