import customtkinter as ctk
from .microphone_handler import MicrophoneHandler
from .music_file_handler import MusicFileHandler

class OptionsPageContent(ctk.CTkFrame):
    """Frame containing options for either selecting a music file or recording with a microphone."""
    def __init__(self, master, controller, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.controller = controller

        self.microphone_handler = MicrophoneHandler()
        self.music_file_handler = MusicFileHandler()

        self.chosen_file = ctk.StringVar()
        self.recorded_file_path = ""

        # Fonts
        self.tab_font_style = ctk.CTkFont(size=25)
        self.tab_content_style = ctk.CTkFont(size=20)
        self.chosen_file_name_style = ctk.CTkFont(size=12, slant="italic")

        self._setup_ui()

    def _setup_ui(self):
        self.options_container = ctk.CTkFrame(self)
        self.options_container.grid(row=0, column=0, pady=(0, 0))

        self._create_input_method_label()
        self._create_tabs()
        self._create_return_button()

        # Configure grid layout for proper centering
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.options_container.grid(columnspan=3, rowspan=3)

    def _create_input_method_label(self):
        self.frame_with_label = ctk.CTkFrame(self.options_container)
        self.frame_with_label.grid(row=0, column=0, sticky="nsew")

        self.choose_method_label = ctk.CTkLabel(self.frame_with_label, text="Choose an input method", font=("sans-serif", 30))
        self.choose_method_label.grid(row=0, column=0, padx=150, pady=(0, 20), sticky="w")

    def _create_tabs(self):
        self.options_tab = ctk.CTkTabview(self.frame_with_label)
        self.options_tab.grid(row=1, column=0, sticky="nsew")
        self.options_tab.configure(width=600)
        self.options_tab._segmented_button.configure(font=self.tab_font_style)

        # Add file and microphone tabs
        self._create_file_tab()
        self._create_microphone_tab()

    def _create_file_tab(self):
        """Create the MP3 file selection tab."""
        self.file_tab = self.options_tab.add("WAV File")
        
        self.file_tab_label = ctk.CTkLabel(self.file_tab, text="Choose a file to process", font=self.tab_content_style)
        self.file_tab_label.pack(fill="both", expand=True)

        self.file_button = ctk.CTkButton(self.file_tab, text="Choose File", command=self.choose_file)
        self.file_button.pack(side="bottom", padx=10, pady=10)

        self.chosen_file_name = ctk.CTkLabel(self.file_tab, textvariable=self.chosen_file, font=self.chosen_file_name_style, width=15, height=1)
        self.chosen_file_name.pack(fill="both", padx=10, pady=20)

        self.process_button = ctk.CTkButton(self.file_tab, text="Start process", state="disabled", command=self.process_chosen_file)
        self.process_button.pack(side="bottom", padx=20, pady=10)

        self.status_message_label = ctk.CTkLabel(self.file_tab, text="", font=self.tab_content_style)
        self.status_message_label.pack(fill="both", expand=True)

    def _create_microphone_tab(self):
        """Create the microphone recording tab."""
        self.mic_tab = self.options_tab.add("Microphone")
        
        self.mic_tab_label = ctk.CTkLabel(self.mic_tab, text="Click Start recording to start", font=self.tab_content_style)
        self.mic_tab_label.pack(fill="both", expand=True)

        self.button_frame = ctk.CTkFrame(self.mic_tab)
        self.button_frame.pack(side="top", pady=10)

        self.mic_tab_start_button = ctk.CTkButton(self.button_frame, text="Start Recording", command=self.start_recording)
        self.mic_tab_start_button.pack(side="left", padx=10)

        self.mic_tab_stop_button = ctk.CTkButton(self.button_frame, text="Stop Recording and Save", command=self.stop_recording, state="disabled")
        self.mic_tab_stop_button.pack(side="left", padx=10)

        self.mic_tab_process_button = ctk.CTkButton(self.button_frame, text="Process File", command=self.process_recording, state="disabled")
        self.mic_tab_process_button.pack(side="left", padx=10)

    def _create_return_button(self):
        """Create the Return button for going back to the StartPage."""
        self.return_button = ctk.CTkButton(self, text="Return", command=self.return_to_start)
        self.return_button.grid(row=0, column=1, padx=(0, 100), pady=(450, 5), sticky="w")

    def return_to_start(self):
        """Reset file selection and return to the StartPage."""
        self.chosen_file.set("")
        self.chosen_file_name.configure(text="")
        self.status_message_label.configure(text="")
        self.process_button.configure(state="disabled")

        self.mic_tab_stop_button.configure(state="disabled")
        self.mic_tab_process_button.configure(state="disabled")
        self.mic_tab_start_button.configure(state="normal")
        self.mic_tab_label.configure(text="Click Start recording to start")
        self.controller.show_frame("StartPage")

    def choose_file(self):
        """Open a file dialog for choosing a WAV file, and enable the process button if successful."""
        success = self.music_file_handler.choose_file()
        if success:
            self.chosen_file.set(self.music_file_handler.chosen_file)
            self.process_button.configure(state="normal")

    def process_chosen_file(self):
        """Process the selected WAV file and update the status."""
        success = self.music_file_handler.process_file()
        if success:
            self.status_message_label.configure(text="File processed successfully!")
            self.chosen_file.set("")
            self.chosen_file_name.configure(text="")
            self.process_button.configure(state="disabled")

    def start_recording(self):
        """Start recording audio and update button states."""
        self.microphone_handler.start_recording()
        self.mic_tab_start_button.configure(state="disabled")
        self.mic_tab_stop_button.configure(state="normal")
        self.mic_tab_process_button.configure(state="disabled")
        self.mic_tab_label.configure(text="Recording... Click Stop to save")

    def stop_recording(self):
        """Stop recording, enable the process button, and update UI states."""
        self.microphone_handler.stop_recording()
        self.mic_tab_stop_button.configure(state="disabled")
        self.mic_tab_process_button.configure(state="normal")
        self.mic_tab_start_button.configure(state="normal")
        self.mic_tab_start_button.configure(text="Start New Recording")
        self.mic_tab_label.configure(text="Recording stopped. Click Process to make it into a sheet!")

    def process_recording(self):
        """Process the recorded audio and update the UI status."""
        success = self.microphone_handler.process_recording()
        if success:
            self.mic_tab_label.configure(text="Recording processed successfully!")
            self.mic_tab_process_button.configure(state="disabled")
