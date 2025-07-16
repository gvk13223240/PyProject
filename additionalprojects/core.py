import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import io

st.title("🎵 Audio Upload, Playback & Waveform Visualizer")

# Upload audio file
audio_file = st.file_uploader("Upload audio file", type=["wav", "mp3", "ogg", "flac"])

if audio_file is not None:
    # Play audio in Streamlit
    st.audio(audio_file)

    # Try to read and plot waveform if it's a WAV file
    if audio_file.type == "audio/wav":
        # Read WAV file data
        wav_bytes = audio_file.read()
        samplerate, data = wavfile.read(io.BytesIO(wav_bytes))

        # If stereo, take one channel
        if len(data.shape) > 1:
            data = data[:, 0]

        # Create time axis
        time = np.linspace(0, len(data) / samplerate, num=len(data))

        # Plot waveform
        fig, ax = plt.subplots()
        ax.plot(time, data)
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Amplitude")
        ax.set_title("Waveform")
        st.pyplot(fig)
    else:
        st.info("Waveform visualization only supports WAV files currently.")
