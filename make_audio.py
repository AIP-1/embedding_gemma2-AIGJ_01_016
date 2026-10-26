import glob, numpy as np, soundfile as sf, librosa
SR = 16000
t = np.arange(3 * SR) / SR
sf.write("media/beep.wav", (0.5 * np.sin(2 * np.pi * 1000 * t)).astype("float32"), SR)
n = 5 * SR
spec = np.fft.rfft(np.random.randn(n))
freqs = np.fft.rfftfreq(n); freqs[0] = freqs[1]
pink = np.fft.irfft(spec / np.sqrt(freqs), n)
sf.write("media/noise.wav", (0.3 * pink / np.abs(pink).max()).astype("float32"), SR)
for raw in sorted(glob.glob("media/raw_*.wav")):
    y, _ = librosa.load(raw, sr=SR, mono=True)
    sf.write(raw.replace("raw_", ""), y, SR)
for f in sorted(glob.glob("media/*.wav")):
    i = sf.info(f); print(f, i.samplerate, i.channels, f"{i.duration:.1f}s")
