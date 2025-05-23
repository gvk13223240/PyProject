import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import tempfile

st.title("🔊 Simple Sound Wave Visualizer")

# Parameters
wave_type = st.selectbox("Select Wave Type", ["Sine", "Square"])
freq = st.slider("Frequency (Hz)", 100, 2000, 440)
duration = st.slider("Duration (seconds)", 1, 5, 2)
sample_rate = 44100

# Generate time array
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generate waveform
if wave_type == "Sine":
    wave = 0.5 * np.sin(2 * np.pi * freq * t)
else:  # Square wave
    wave = 0.5 * np.sign(np.sin(2 * np.pi * freq * t))

# Plot waveform
fig, ax = plt.subplots()
ax.plot(t[:1000], wave[:1000])  # plot first 1000 samples
ax.set_title(f"{wave_type} Wave - {freq} Hz")
ax.set_xlabel("Time [s]")
ax.set_ylabel("Amplitude")
st.pyplot(fig)

# Convert wave to 16-bit PCM for playback and saving
wave_int16 = np.int16(wave * 32767)

# Save wav to a temp file
with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
    write(f.name, sample_rate, wave_int16)
    wav_path = f.name

# Streamlit audio player
with open(wav_path, "rb") as audio_file:
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/wav")

# Download button
st.download_button("⬇️ Download WAV file", data=audio_bytes, file_name="waveform.wav", mime="audio/wav")
