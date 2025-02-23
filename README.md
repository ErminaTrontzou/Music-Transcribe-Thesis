﻿# Music-Transcribe

## Overview
This project is an audio recognition and transcription application that detects musical notes from audio input and visualizes them on a musical staff. The application was developed as part of my thesis at the **Department of Computer, Informatics, and Telecommunication Engineering**, International Hellenic University.

The system leverages advanced computational techniques to recognize and transcribe notes played on different musical instruments, producing a sheet music representation.

## Features
- **Audio Processing**: Analyze audio from WAV files or live microphone recordings.
- **Frequency Analysis**: Utilizes the Fast Fourier Transform (FFT) algorithm for frequency spectrum analysis.
- **Note Recognition**: Identifies the pitch and duration of individual notes with support for multiple instruments.
- **Sheet Music Generation**: Transcribes recognized notes into sheet music using the LilyPond tool.
- **Interactive User Interface**: Easy-to-use interface for selecting and processing audio files or live input.

## Technologies Used
- **Programming Language**: Python
- **Libraries and Tools**:
  - NumPy: Numerical computations
  - SciPy: Signal processing
  - PyAudio: Microphone input processing
  - Matplotlib: Visualization
  - LilyPond: Music transcription and staff visualization

## Installation

### Option 1: Download Artifact
For a quick setup:
1. Download the pre-packaged artifact (a ZIP file containing the `.exe` application and a portable LilyPond executable).
2. Extract the ZIP file.
3. Run the application by double-clicking the `.exe` file.

### Option 2: Clone and Run from IDE
To set up the project on your local machine:

1. Clone the repository:
   ```bash
   git clone https://github.com/username/repository-name.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download and install LilyPond from [LilyPond's official website](https://lilypond.org/).
4. Update the download directory path in the code where LilyPond is invoked.
5. Run the application:
   ```bash
   python main.py
   ```

## How It Works
1. **Audio Input**: The user uploads a WAV file or records live audio via a microphone.
2. **Signal Processing**: The audio signal is segmented and processed using FFT for frequency analysis.
3. **Note Recognition**: The application identifies distinct notes by detecting peaks in the frequency domain.
4. **Transcription**: Recognized notes are converted into a readable musical staff using LilyPond.

## Results
The application has been tested with multiple audio sources, including recordings of classical pieces (e.g., *Für Elise*). While it achieves high accuracy in note detection for clear audio inputs, challenges remain in complex scenarios, such as overlapping sounds or noisy environments.

## Challenges and Future Work
- **Challenges**:
  - Handling polyphonic music with overlapping notes.
  - Achieving higher accuracy in noisy or live environments.
- **Future Work**:
  - Improving the noise filtering and peak detection algorithms.
  - Enabling recognition of chords in addition to single notes.

## Contributions
This project was guided by Dr. Dimitriadis Evangelos and is part of my academic thesis.

## License
This project is licensed under the MIT License.
