#
from music21 import converter

#
def get_midi_lists(mf: str) -> list:
    """INSERT DOCSTRING HERE"""

    #
    score_in = converter.parseFile(mf)

    #
    components = []

    #
    for msg in score_in.recurse().notesAndRests:

        #
        if msg.duration.quarterLength != 0:

            try:
                type = msg.name
            except:
                type = msg.pitchedCommonName

            #
            try:
                pitchlist = msg.pitches
                temp_pitch_list = []

                #
                for pitch in pitchlist:
                    neopitch = pitch.name.lower()
                    neooctave = pitch.octave

                    if neopitch[-1] == "#":
                        neopitch = f"{neopitch[0]}s"
                    elif neopitch[-1] == "-":
                        neopitch = f"{neopitch[0]}f"

                    #
                    if 2 <= neooctave <= 6:

                        #
                        if neooctave > 4:
                            ticks = neooctave - 4
                            for tick in range(ticks):
                                neopitch += "'"

                        #
                        elif neooctave < 4:
                            if neooctave == 3:
                                neopitch += ","
                            elif neooctave == 2:
                                neopitch += ",,"

                    #
                    temp_pitch_list.append(neopitch)

                #
                components.append([type, temp_pitch_list, msg.duration.quarterLength])

            #
            except:
                print("error:", msg)

    return components

if __name__ == "__main__":
    component_list = get_midi_lists("media/A_Sleepin_Bee.mid")
    for c in component_list:
        print(c)
