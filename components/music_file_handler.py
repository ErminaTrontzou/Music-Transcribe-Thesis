from customtkinter  import filedialog
from.fft import FFT

class MusicFileHandler:
    def __init__(self):
        self.fft = FFT()
        self.chosen_file = ""

    def choose_file(self):
        self.chosen_file = filedialog.askopenfilename(filetypes=[("wav files", "*.wav")])
        if self.chosen_file:
            print(self.chosen_file)
            return True
        return False

    def process_file(self):
        if self.chosen_file:
            self.fft.music_file_data_preparation(self.chosen_file)
            return True
        return False
