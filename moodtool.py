#!/usr/bin/python
# encoding=utf8
# This file is part of pymoodbar.
# Copyright 2016, szf <spezifisch@users.noreply.github.com>
#
# pymoodbar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pymoodbar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pymoodbar.  If not, see <http://www.gnu.org/licenses/>.

import sys
import numpy as np
from pydub import AudioSegment

from pymoodbar import MoodbarBuilder, Render

def clamp(value, min_, max_):
    return max(min(max_, value), min_)

def progress_bar(percent):
    if percent > 1:
        percent = 1

    width = 80
    progress = int(round(width*percent))
    bar = "\r%3d%% [%s>%s]" % (percent*100, "="*progress, " "*(width-progress))
    sys.stdout.write(bar)
    sys.stdout.flush()

class MusicIterable(object):

    def __init__(self, soundfile, step):
        print("Loading soundfile...")
        self.sound = AudioSegment.from_file(soundfile)

        self.frame_rate = self.sound.frame_rate
        self.frame_count = int(self.sound.frame_count())
        self.cur = 0
        self.step = step

        print("Sample rate:  %s Hz" % self.frame_rate)
        print("Sample count: %s samples" % self.frame_count)

    def __iter__(self):
        return self

    def __next__(self):
        percent_done = float(self.cur) / self.frame_count
        progress_bar(percent_done)

        if self.cur >= self.frame_count:
            print()
            raise StopIteration

        begin = self.cur
        end = self.cur + self.step
        if end > self.frame_count:
            end = self.frame_count

        segment = self.sound.get_sample_slice(begin, end)

        self.cur = end+1

        return self.get_samples(segment)

    # python2 compat
    next = __next__

    def get_samples(self, segment):
        samples_combined = segment.get_array_of_samples()
        samples = []
        for i in range(0, len(samples_combined), 2):
            left = samples_combined[i]
            right = samples_combined[i+1]
            samples.append((left+right)/2)

        return samples


if __name__ == "__main__":
    soundfile = sys.argv[1]

    # fft/sample chunk size
    kBands = 128

    # output image size
    width = 1000
    height = 50

    # open audio file
    music = MusicIterable(soundfile, kBands)

    print("\nCalculating moodbar ...")

    # calculate moodbar
    m = MoodbarBuilder()
    m.Init(kBands, music.frame_rate)

    for samples in music:
        # fft of chunk
        bins = np.fft.fft(samples, kBands)

        # calculate magnitude of bins
        # norm it (is it needed?)
        n = kBands * kBands
        mags = [(x.real*x.real+x.imag*x.imag)/n for x in bins]

        # add chunk to moodbar
        m.AddFrame(mags)

    # do normalization, get moodbar output as list
    mood = m.Finish(width)

    # write qt-rendered png
    filename = "foo.png"
    img = Render(mood, width, height, filename)
    print "saved image:", filename
