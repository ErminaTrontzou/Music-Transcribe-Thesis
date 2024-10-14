import subprocess

class LilyPondConverter:
    def __init__(self, notes_info):
        self.notes_info = notes_info
        self.bass_notes = ''
        self.treble_notes = ''
    
    def note_to_lilypond_note(self, note, base_octave = 3):
        note_octave = int(note[-1])
        octave_offset = note_octave - base_octave

        octave_suffix = ''
        if octave_offset > 0:
            octave_suffix = octave_offset * "'"
        elif octave_offset < 0:
            octave_suffix = -octave_offset * ","
        
        if note[1] == '#':
            print (note[0].lower() + 'is' + octave_suffix)
            return note[0].lower() + 'is' + octave_suffix

        return note[0].lower() + octave_suffix


    def duration_to_lilypond(self, duration):
        if duration == 1.0:
            return '4'  # quarter note
        elif duration == 0.5:
            return '8'  # eighth note
        elif duration == 0.25:
            return '16' # sixteenth note
        elif duration == 2.0:
            return '2'  # half note
        elif duration == 4.0:
            return '1'  # whole note
        else:
            if duration < 0.375:
                return '16'
            elif duration < 0.75:
                return '8'
            elif duration < 1.5:
                return '4'
            elif duration < 3:
                return '2'
            else:
                return '1'
    
    def convert(self):
        lilypond_treble_notes = []
        lilypond_bass_notes = []
        use_bass_clef = False
        
        for note_info in self.notes_info:
            note = note_info['note']
            duration = note_info['duration']
            
            if note == 'pause':
                lilypond_treble_notes.append(f"r{self.duration_to_lilypond(duration)}")
                lilypond_bass_notes.append(f"r{self.duration_to_lilypond(duration)}")
                continue
            
            octave = int(note[-1])
            lp_duration = self.duration_to_lilypond(duration)
           
            if octave < 4:
                lp_note = self.note_to_lilypond_note(note)
                lilypond_treble_notes.append(f"r{self.duration_to_lilypond(duration)}")
                lilypond_bass_notes.append(f"{lp_note}{lp_duration}")
                use_bass_clef = True
            else:
                lp_note = self.note_to_lilypond_note(note)
                lilypond_treble_notes.append(f"{lp_note}{lp_duration}")
                lilypond_bass_notes.append(f"r{self.duration_to_lilypond(duration)}")

        if use_bass_clef:
                    treble_staff = "{ \\clef treble  " + " ".join(lilypond_treble_notes) + " }"
                    bass_staff = "{ \\clef bass " + " ".join(lilypond_bass_notes) + "}"
                    lilypond_string = "<<\n  \\new Staff " + treble_staff + "\n  \\new Staff " + bass_staff + "\n>>"
        else:
            lilypond_string = " ".join(lilypond_treble_notes)

        print(lilypond_string)
        return lilypond_string
    
    def write_to_file(self, file_name):
        lilypond_string = self.convert()
        with open(file_name, 'w') as file:
            file.write("\\version \"2.24.4\"\n")
            file.write("{\n")
            file.write(lilypond_string)
            file.write("\n}\n")
        print(f"LilyPond file written to {file_name}")
    
    def run_lilypond(self, file_name):
        lilypond_path = "lilypond/lilypond-2.24.4/bin/lilypond.exe"

        try:
            subprocess.run([lilypond_path, file_name], check=True)
            print(f"PDF successfully created for {file_name}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
