# pip install pedalboard  # https://github.com/spotify/pedalboard
from math import sqrt
from pedalboard import Pedalboard, PeakFilter, Compressor
from pedalboard.io import AudioFile

in_file  = "input.mp3"
out_file = "output-pedalboard.mp3"

# Helper: geometric centers + Q for “cover f1..f2” peaking bands
def band_peak(f1, f2, gain_db):
    f0 = sqrt(f1 * f2)
    q  = f0 / (f2 - f1)  # approx Q to span f1..f2
    return PeakFilter(cutoff_frequency_hz=f0, gain_db=gain_db, q=q)

# Build the chain
board = Pedalboard([
    # # High-pass @45 Hz, 12 dB/oct (biquad = 2nd order) and Q = 0.1
    # BiquadFilter(BiquadFilterType.HIGHPASS, cutoff_frequency_hz=45.0, q=0.1),

    # +6 dB between 30–110 Hz (broad peaking band)
    band_peak(30.0, 110.0, gain_db=+6.0),

    # −3 dB between 110 Hz–1 kHz (wide corrective dip)
    band_peak(110.0, 1000.0, gain_db=-3.0),

    # Additional parametric boost @100 Hz: +7 dB, Q = 1.0
    #PeakFilter(cutoff_frequency_hz=100.0, gain_db=+7.0, q=1.0),

    # Optional glue: gentle compressor
    #Compressor(threshold_db=-18.0, ratio=3.0, attack_ms=20.0, release_ms=250.0, makeup_gain_db=3.0),
    Compressor(threshold_db=-18.0, ratio=3.0, attack_ms=20.0, release_ms=250.0),
])

# I/O
with AudioFile(in_file) as f:
    audio = f.read(f.frames)
    sr = f.samplerate

processed = board(audio, sr)

with AudioFile(out_file, 'w', sr, processed.shape[0]) as f:
    f.write(processed)
