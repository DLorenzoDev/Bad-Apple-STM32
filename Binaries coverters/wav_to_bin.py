import wave

# Abre archivo WAV 8-bit mono
with wave.open('Bad Apple!!.wav', 'rb') as wav_in:
    assert wav_in.getsampwidth() == 1  # 8-bit = 1 byte
    assert wav_in.getnchannels() == 1  # mono

    frames = wav_in.readframes(wav_in.getnframes())

# Guarda solo los datos de audio en un archivo binario
with open('audio.bin', 'wb') as bin_out:
    bin_out.write(frames)
