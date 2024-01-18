import midi
import math
from random import random, choice, seed
from time import sleep
from random import choice
from listener import Listener
from neoscore.common import *

path_to_midi_file = "media/A_Sleepin_Bee.mid" #  <--- change this to your file

class UI:
    """INSERT DOCSTRING HERE"""

    def __init__(self):
        """INSERT DOCSTRING HERE"""

        #
        self.midilist = midi.get_midi_lists(path_to_midi_file)
        print(f"Midilist contents: {self.midilist}")

        #
        neoscore.setup()

        #
        annotation = "DEMO digital score BLAH BLAH"
        RichText((Mm(1), Mm(1)), None, annotation, width=Mm(170))

        #
        staff = Staff((ZERO, Mm(70)), None, Mm(180), line_spacing=Mm(5))
        unit = staff.unit
        clef = Clef(ZERO, staff, "treble")

        #
        self.center = unit(20)

        #
        self.n1 = Chordrest(self.center, staff, ["g"], Duration(1, 4))
        self.n2 = Chordrest(self.center, staff, ["b"], Duration(1, 4))
        self.n3 = Chordrest(self.center, staff, ["d'"], Duration(1, 4))
        self.n4 = Chordrest(self.center, staff, ["f'"], Duration(1, 4))

        #
        self.note_list = (self.n1, self.n2, self.n3, self.n4)

        #
        self.ear = Listener()
        self.ear.start()

    def refresh_func(self, time):
        """INSERT DOCSTRING HERE"""

        #
        self.n1.x = self.center + Mm(math.sin((time / 2)) * 10)
        self.n2.x = self.center + Mm(math.sin((time / 2) + 1) * 12)
        self.n3.x = self.center + Mm(math.sin((time / 2) + 1.7) * 7)
        self.n4.x = self.center + Mm(math.sin((time / 2) + 2.3) * 15)

        #
        if random() >= 0.95:
            rnd_note = choice(self.note_list)
            if random() >= 0.5:
                new_pitch = choice(self.midilist)
            else:
                new_pitch = self.ear.neonote

            #
            try:
                rnd_note.notes = [new_pitch]
            except:
                pass


if __name__ == "__main__":
    run = UI()
    neoscore.show(run.refresh_func,
                  display_page_geometry=False)
