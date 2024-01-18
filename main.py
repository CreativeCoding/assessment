import midi
from random import random, choice, seed
from time import sleep
from random import choice
from listener import Listener
from neoscore.common import *

path_to_midi_file = "media/A_Sleepin_Bee.mid" #  <--- change this to your file

class UI(Listener):
    """INSERT DOCSTRING HERE"""

    def __init__(self):
        super(Listener).__init__()
        """INSERT DOCSTRING HERE"""

        #
        self.midilist = midi.get_midi_lists(path_to_midi_file)

        #
        neoscore.setup()

        #
        annotation = "DEMO digital score BLAH BLAH"
        RichText((Mm(1), Mm(1)), None, annotation, width=Mm(170))

        #
        self.staff_one = Staff((ZERO, Mm(70)), None, Mm(180))
        clef_one = Clef(ZERO, self.staff_one, 'treble')
        self.note1 = Chordrest(Mm(20), self.staff_one, ["c'"], (1, 4))

        #
        self.staff_two = Staff((ZERO, Mm(110)), None, Mm(180))
        clef_two = Clef(ZERO, self.staff_two, 'treble')
        self.note2 = Chordrest(Mm(20), self.staff_two, ["c'"], (1, 4))

    def refresh_func(self, time):
        """INSERT DOCSTRING HERE"""
        pass

if __name__ == "__main__":
    run = UI()
    neoscore.show(run.refresh_func,
                  display_page_geometry=False)




