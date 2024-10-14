import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np

#Global Variables
FPB = 3200 #Frames per Buffer: number of data points processed (recorder and captured) in each buffer (second)
CHANNELS = 1 #Number of channels in the audio file (1 for mono, 2 for stereo)
RATE = 44100 #Sample rate of the audio file in Hz (44.1 kHz) or samples per second
FORMAT = pyaudio.paInt16 #Format of the audio file (16-bit signed integer) or bytes per sample (2 bytes per sample)


class Recorder(object):

    def __init__(self, channels=CHANNELS, rate=RATE, frames_per_buffer=FPB):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

    def open(self, fname, mode='wb'):
        return RecordingFile(fname, mode, self.channels, self.rate,
                            self.frames_per_buffer)
class RecordingFile(object):
    def __init__(self, fname, mode, channels, 
                rate, frames_per_buffer):
        self.fname = fname
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self.p = pyaudio.PyAudio()
        self.wavefile = self.prepare_file(self.fname, self.mode)
        self.stream = None

    def start_recording(self):
        self.stream = self.p.open(format=FORMAT,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer,
                                        stream_callback=self.get_callback())
        self.stream.start_stream()
        return self

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        return self.fname

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            return in_data, pyaudio.paContinue
        return callback


    def prepare_file(self, fname, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self.p.get_sample_size(FORMAT))
        wavefile.setframerate(self.rate)
        return wavefile
    
    def read_wave_file(self):
        wave_file = wave.open(self.fname, 'rb')
        signal = wave_file.readframes(-1)
        signal = np.frombuffer(signal, dtype=np.int16)
        return signal

