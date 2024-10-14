import customtkinter as ctk
from components.input_options import OptionsPageContent

class AboutWindow(ctk.CTkToplevel):
    """A window to display information about the Music Transcribe application."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x450")
        self.resizable(False, False)
        self.attributes('-topmost', True)
        self.title("About")
        self._setup_ui()

    def _setup_ui(self):
        # Main content frame for better layout management
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        heading_label = ctk.CTkLabel(
            main_frame, 
            text="About this application", 
            font=("Helvetica", 28, "bold"),
            anchor="center"
        )
        heading_label.pack()

        about_text = (
            "Music Transcribe is a Python-based application developed as part of my bachelor's thesis. "
            "With a user-friendly interface, it focuses on the recognition of musical notes, "
            "distinguishing pitch and duration.\n\n"
            "The application supports sourcing notes from either .wav files or the sounds of various musical "
            "instruments directly from your microphone.\n\n"
            "Notably, Music Transcribe utilizes Fast Fourier Transform (FFT) for note recognition. It efficiently "
            "transcribes notes onto a pentagram and allows for the export of these files, offering a versatile tool "
            "for everyone, professional or not."
        )

        about_label = ctk.CTkLabel(main_frame, text=about_text, justify="left", anchor="w", font=("Helvetica", 14), wraplength=460)
        about_label.pack(fill="both", expand=True, padx=10, pady=20)

        close_button = ctk.CTkButton(main_frame, text="Close", command=self.destroy, width=100)
        close_button.pack(pady=10)
class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._setup_ui()
        
    def _setup_ui(self):
        self.pack_propagate(False)  #Prevent frame from auto-scaling
        self.configure(height=350)

        ctk.CTkLabel(self, text="Click Start to begin", font=("Roboto", 30)).pack(side="top", fill="x", pady=(110, 10))
        self._create_button("Start", self.controller.open_options_component).pack(side="top", padx=5, pady=15)

    def _create_button(self, text, command):
        return ctk.CTkButton(self, text=text, command=command, **self._button_config())

    def _button_config(self):
        """Return the configuration for buttons."""
        return {
            "width": 100,
            "height": 100,
            "corner_radius": 30,
            "font": ("Roboto", 30),
            "text_color": "black",
            "hover_color": "light grey",
        }


class InputOptions(ctk.CTkFrame):
    """The input options page allowing users to choose how to input audio."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._setup_ui()

    def _setup_ui(self):
        options_component = OptionsPageContent(self, self.controller)
        options_component.pack(side="top", fill="x", pady=(5, 5))  # Adjusted padding

class App(ctk.CTk):
    """Main application class managing navigation between pages and opening dialogs."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_app()

    def _setup_app(self):
        self._add_header()

        # Application theme and window setup
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.geometry("950x700")
        self.resizable(False, False)

        # Create the frame container that will hold the content
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Create frames (compact frame sizes to allow space for the footer)
        self.frames = {}
        for F in (StartPage, InputOptions):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

        self._add_footer()

    def _add_header(self):
        """Add the Title and Subtitle (Header) to the main window."""
        title_font = ctk.CTkFont(family="sans-serif", size=40, weight="bold")
        subtitle_font = ctk.CTkFont(family="Roboto", size=15, slant="italic")

        ctk.CTkLabel(self, text="Music Transcribe", font=title_font).pack(side="top", fill="x", pady=(10, 0))
        ctk.CTkLabel(self, text="Your Melodic Maestro – Turning Sound into Sheets Effortlessly!",
                     font=subtitle_font).pack(side="top", fill="x")

    def _add_footer(self):
        """Add the About button and copyright label to the main window."""
        footer_frame = ctk.CTkFrame(self)
        footer_frame.pack(side="bottom", fill="x", pady=(15, 20))

        ctk.CTkButton(footer_frame, text="About", command=self.open_about).pack(side="top", pady=5)
        ctk.CTkLabel(footer_frame, text="Copyright: Ermina Trontzou 2023").pack(side="top", pady=5)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def open_options_component(self):
        self.show_frame("InputOptions")

    def open_about(self):
        AboutWindow(self)


if __name__ == "__main__":
    app = App()
    app.title("Music Transcribe")
    app.mainloop()
