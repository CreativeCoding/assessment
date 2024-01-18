from time import sleep
from random import random
import pyaudio
import numpy as np
import math
from threading import Thread

class Listener:
    def __init__(self):
        """INSERT DOC STRING HERE"""
        #
        # self.running = True
        # self.connected = False
        # self.logging = False

        #
        self.CHUNK = 2 ** 11
        self.RATE = 44100
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)

        # initiate the data dictionary
        self.notes = ['a', 'bf', 'b', 'c', 'df', 'd', 'ef', 'e', 'f', 'gf', 'g', 'af']
        self.audio_dict = {"amplitude": 0,
                           "freq": 0,
                           "midinote": []
                           }

    def start(self):
        print("mic listener: started!")
        # use threading to spin this plate
        audio_thread = Thread(target=self.audio_analyser)
        audio_thread.start()

    def audio_analyser(self):
        while self.running:
            data = np.frombuffer(self.stream.read(self.CHUNK,
                                                  exception_on_overflow=False),
                                 dtype=np.int16)
            peak = np.average(np.abs(data)) * 2
            if peak > 1000:
                bars = "#" * int(50 * peak / 2 ** 16)

                # Calculates the frequency from with the peak ws
                data = data * np.hanning(len(data))
                fft = abs(np.fft.fft(data).real)
                fft = fft[:int(len(fft) / 2)]
                freq = np.fft.fftfreq(self.CHUNK, 1.0 / self.RATE)
                freq = freq[:int(len(freq) / 2)]
                freqPeak = freq[np.where(fft == np.max(fft))[0][0]] + 1

                # get midinote from freqPeak
                midinote = self.freq_to_note(freqPeak)

                # Shows the peak frequency and the bars for the amplitude
                print(f"peak frequency: {freqPeak} Hz, mididnote {midinote}:\t {bars}")

                self.audio_dict['freq'] = freqPeak
                self.audio_dict['midinote'] = midinote
            self.audio_dict['amplitude'] = peak

    def freq_to_note(self, freq: float) -> list:
        """Converts frequency into midi note and octave.
        formula taken from https://en.wikipedia.org/wiki/Piano_key_frequencies

        returns: str neonote (neoscore format e.g. "fs''")
        """

        note_number = 12 * math.log2(freq / 440) + 49
        note_number = round(note_number)
        note_position = (note_number - 1) % len(self.notes)
        neonote = self.notes[note_position]
        octave = (note_number + 8) // len(self.notes)

        # if octave out of range then make it middle C octave
        if 2 <= octave <= 6:

            # add higher octave indicators "'"
            if octave > 4:
                ticks = octave - 4
                for tick in range(ticks):
                    neonote += "'"

            # add lower octave indicators ","
            elif octave < 4:
                if octave == 3:
                    neonote += ","
                elif octave == 2:
                    neonote += ",,"

        return [neonote]

    def read(self) -> list:
        """returns current dictionary as list, as a single quaver"""
        audio_list = []
        audio_list.append("midi")  # type
        if self.audio_dict['amplitude'] > 1000:
            audio_list.append(self.audio_dict.get("midinote"))  # pitch
        else:
            audio_list.append([])  # rest
        audio_list.append(0.5)  # duration
        return audio_list

    def terminate(self):
        """safely terminates all streams"""
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


if __name__ == "__main__":
    mic = Audio()
    mic.start()
    while True:
        data = mic.read()
        print(data)
        sleep(1)
