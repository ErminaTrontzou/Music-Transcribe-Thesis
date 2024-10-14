import numpy as np
import scipy.io.wavfile as wavfile
import scipy.signal
import os
import math
from .lilypond_convert import LilyPondConverter

class PlayedNote:
    def __init__(self, note, duration):
        self.note = note
        self.duration = duration

class FFT:
    def __init__(self, fft_window_seconds=0.20, freq_min=27.5, freq_max=4186.0, cutoff_freq=27.5, filter_order=32):
        self.fft_window_seconds = fft_window_seconds
        self.freq_min = freq_min
        self.freq_max = freq_max
        self.cutoff_freq = cutoff_freq
        self.filter_order = filter_order
        
        self.fft_window_size = None
        self.energy_threshold = 1e5 
        self.rolling_window_size = 10

    def freq_to_number(self, f):
        return 12*np.log2(f/27.5) + 9
    
    def note_name(self, n):
        n = round(n)
        note = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"][n % 12]
        octave = str(int(n // 12))
        return note + octave

    def extract_sample(self, audio, frame_number):
        begin = frame_number * self.fft_window_size
        end = begin + self.fft_window_size
        if end > len(audio):
            end = len(audio)
            return np.concatenate([audio[begin:], np.zeros((self.fft_window_size - (end - begin)), dtype=float)])

        return audio[begin:end]
        
    def gcd(self, frequencies):
        """Calculate GCD among a list of frequencies."""
        if not frequencies:
            return None
        
        def euclidean_gcd(a, b):
            while b != 0:
                a, b = b, a % b
            return a
        
        int_frequencies = [round(freq * 1e6) for freq in frequencies]
        gcd_freq = int_frequencies[0]
        for freq in int_frequencies[1:]:
            gcd_freq = euclidean_gcd(gcd_freq, freq)
        return gcd_freq / 1e6
  
    def high_pass_filter(self, audio, fs):
        sos = scipy.signal.butter(N=self.filter_order, 
                                  Wn=self.cutoff_freq, 
                                  fs=fs, 
                                  btype='highpass', 
                                  analog=False, 
                                  output='sos')
        return scipy.signal.sosfiltfilt(sos=sos, x=audio)
    
    def microphone_data_preparation(self, file_path):
        fs, data = wavfile.read(file_path)

        if(np.abs(data.min())>np.abs(data.max())):
            data = (data/data.min())*32767
        else:
            data = (data/data.max())*32767

        self.process_audio_file(fs,data, file_path)

    def music_file_data_preparation(self, file_path):
        fs, data = wavfile.read(file_path)
        self.process_audio_file(fs,data, file_path)


    def process_audio_file(self, fs, data, file_path):
        if len(data.shape) == 1:
            audio = data
        else:
            audio = data.T[0]

        audio = self.high_pass_filter(audio, fs)
        
        self.fft_window_size = int(fs * self.fft_window_seconds)
        total_frames = math.ceil(len(audio) / self.fft_window_size)

        window = np.hamming(self.fft_window_size)        

        xf = np.fft.rfftfreq(self.fft_window_size, 1 / fs)

        energy_list = []
        notes_info = []
        notes = []

        for frame_number in range(total_frames):
            sample = self.extract_sample(audio, frame_number)
            fft_result = np.fft.rfft(sample * window)
            fft_magnitude = np.abs(fft_result).real

            frame_energy = np.sum(sample ** 2) / len(sample)
            energy_list.append(frame_energy)

            if len(energy_list) > self.rolling_window_size:
                energy_list.pop(0)

            avg_energy = np.mean(energy_list)

            current_note = None
            if frame_energy < self.energy_threshold or frame_energy < avg_energy * 0.1:
                current_note = "pause"
                print(f"Frame {frame_number}: Forced Pause with energy {frame_energy} < {self.energy_threshold}")
            else:
                peaks, properties = scipy.signal.find_peaks(fft_magnitude, height=50000.00)
            
                if len(peaks) == 0:
                    current_note = "pause"
                    print (f"Frame {frame_number}: Pause with no peaks")
                else:
                    main_peak_index = np.argmax(properties['peak_heights'])
                    fundamental_freq = xf[peaks[main_peak_index]]
                    fundamental_amplitude = properties['peak_heights'][main_peak_index]

                    dynamic_threshold = 0.04 * fundamental_amplitude
                    print(f"Frame {frame_number}: Fundamental frequency = {fundamental_freq}, Amplitude = {fundamental_amplitude}, Dynamic Threshold = {dynamic_threshold}")

                    close_harmonics = []
                    all_potential_harmonics = []  # Collect all potential harmonics for plotting

                    for peak in peaks:
                        potential_harmonic_freq = xf[peak]
                        all_potential_harmonics.append(potential_harmonic_freq)

                        if fft_magnitude[peak] < dynamic_threshold:
                            continue

                        if fundamental_freq < potential_harmonic_freq:
                            deviation_from_harmony = potential_harmonic_freq / fundamental_freq - round(potential_harmonic_freq / fundamental_freq)
                            if abs(deviation_from_harmony) <= 0.02:
                                theoretical_harmonic  = round(potential_harmonic_freq / fundamental_freq) * fundamental_freq
                                close_harmonics.append(theoretical_harmonic)
                        else:
                            deviation_from_harmony = fundamental_freq / potential_harmonic_freq - round(fundamental_freq / potential_harmonic_freq)
                            if abs(deviation_from_harmony) <= 0.04 and round(fundamental_freq/potential_harmonic_freq) <= 3:
                                theoretical_harmonic = fundamental_freq / round(fundamental_freq / potential_harmonic_freq)
                                close_harmonics.append(theoretical_harmonic)

                    print(f"After applying threshold, close harmonics for {fundamental_freq}: {close_harmonics}")                

                    base_frequency = self.gcd(close_harmonics + [fundamental_freq])

                    if base_frequency < self.freq_min or base_frequency > self.freq_max:
                        current_note = "pause"
                    else:
                        print(f"Assuming base frequency {base_frequency}")

                        note_number = self.freq_to_number(base_frequency)
                        print(f"Note number {note_number}")
                        current_note = self.note_name(note_number)
                        print(f"Current note {current_note}")

            if notes and current_note == notes[-1].note:
                notes[-1].duration += self.fft_window_seconds
            else:
                notes.append(PlayedNote(note=current_note, duration=self.fft_window_seconds))

        for note in notes:
            notes_info.append({"note": note.note, "duration": note.duration})
        
        print('Notes for : ', os.path.basename(file_path), '\n', notes_info)

        converter = LilyPondConverter(notes_info)
        lilypond_file_name = os.path.splitext(file_path)[0] + ".ly"
        converter.write_to_file(lilypond_file_name)
        converter.run_lilypond(lilypond_file_name)  