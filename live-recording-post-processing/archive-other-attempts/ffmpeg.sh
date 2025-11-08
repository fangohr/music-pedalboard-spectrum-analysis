# Works okay. Loudnorm seems to be fine
# added 6db of bass extra. Not sure this is good.

ffmpeg -i input.mp3 -filter:a "\
equalizer=f=57.446:t=q:w=0.718:g=6,\
equalizer=f=331.662:t=q:w=0.373:g=-3,\
equalizer=f=100:t=q:w=1.0:g=6,\
loudnorm=I=-16:TP=-1.5:LRA=11" \
-c:a libmp3lame -b:a 192k output.mp3


# acompressor=threshold=-18dB:ratio=3:attack=20:release=250:makeup=3" \

# first line: boost frequences

# boosts ~50–100 Hz (centered at 75 Hz),
# 	•	cuts ~200–500 Hz (centered at 350 Hz),
# 	•	then applies a compressor,
# 	•	writes an MP3.

