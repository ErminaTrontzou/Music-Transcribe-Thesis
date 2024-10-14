import os
from CTkMessagebox import CTkMessagebox
from customtkinter  import filedialog
from .recorder import Recorder
from .fft import FFT

class MicrophoneHandler:
    def __init__(self):
        self.rec = Recorder()
        self.running = None
        self.fft = FFT()
        self.recorded_file_path = ""

    def start_recording(self):
        if self.running is not None:
            CTkMessagebox.showinfo("Error", "Already recording.")
        else:
            self.running = self.rec.open('instrument_recording.wav', 'wb')
            self.running.start_recording()

    def stop_recording(self):
        if self.running is not None:
            self.recorded_file_path = self.running.stop_recording()
            self.running.wavefile.close()
            self.running = None 
            print(f"Recorded file path: {self.recorded_file_path}")

            save_path = filedialog.asksaveasfilename(defaultextension=".wav",
                                                     filetypes=[("WAV files", "*.wav")],
                                                     title="Save the recording as")
            if save_path:
                if os.path.exists(save_path):
                    msg = CTkMessagebox(title="Overwrite?", message="File already exists. Do you want to overwrite it?",
                        icon="question", option_1="No", option_2="Yes")
                    overwrite = msg.get()
                    if overwrite=="No":
                        CTkMessagebox(title="Error", message="The recording is not saved.", icon="cancel")  
                        return
                    else:
                        os.remove(save_path)
                os.rename(self.recorded_file_path, save_path)
                self.recorded_file_path = save_path
                print(f"Recording saved to: {self.recorded_file_path}")
            else:
                CTkMessagebox(title="Error", message="The recording is not saved.", icon="cancel")  
        else:
            CTkMessagebox(title="Error", message="You are not recording.", icon="cancel")  

    def process_recording(self):
        if self.recorded_file_path and os.path.exists(self.recorded_file_path):
            self.fft.microphone_data_preparation(self.recorded_file_path)
            return True
        CTkMessagebox(title="Error", message="No recording found to process.", icon="cancel")
        return False
