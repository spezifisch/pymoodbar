# pymoodbar
Generate moodbar files and images in Python

![Example Moodbar](example/foo.png?raw=true "Example Moodbar")

This is a wrapper around Clementine's MoodbarBuilder and MoodbarRenderer classes.
So you can use it standalone and from Python.

# Deps

```
# apt-get install libboost-python-dev libqt4-dev python-pip cmake
# pip install pydub
```

# Build

```
% mkdir build; cd build
% cmake ..
% make
```

This generates pymoodbar.so in parent directory.
It's a Python module.

# Usage

Generate moodbar image:

```
% ./moodtool.py /tmp/Death+Grips+-+Get+Got.mp3
Loading soundfile...
Sample rate:  44100 Hz
Sample count: 7584768 samples

Calculating moodbar ...
100% [================================================================================>]()
saved image: foo.png
```

Use from your own Python code:
```
from pymoodbar import MoodbarBuilder, Render

# for FFT:
import numpy as np

fft_bins = 128
sample_rate = 44100

# create new instance for every song you process
m = MoodbarBuilder()

# initialize internal stuff
m.Init(fft_bins, sample_rate)

# process samples of music in chunks of $fft_binsize samples
# here, len(samples) is 128 long
for samples in music:
    # calculate fft of chunk
    bins = np.fft.fft(samples, fft_bins)

    # calculate magnitude of every frequency bin
    n = kBands * kBands
    mags = [(x.real*x.real+x.imag*x.imag)/n for x in bins]

    # add magnitudes of current chunk to moodbar
    m.AddFrame(mags)

# do normalization, get moodbar output as list
width = 1000 # image columns
mood = m.Finish(width)

# mood now contains a list with R, G, B values for every column.
# You can now put it in your own renderer or use something based on
# Clementine's renderer:

height = 50 # image height
img = Render(mood, width, height, "foo.png")
```
