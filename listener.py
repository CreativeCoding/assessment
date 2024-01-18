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
        self.running = True
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

        #
        self.list_of_notes = ['a', 'bf', 'b', 'c', 'df', 'd', 'ef', 'e', 'f', 'gf', 'g', 'af']
        self.amplitude = 0,
        self.freq = 0
        self.neonote = 'a'

    def start(self):
        print("mic listener: started!")

        #
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

                #
                data = data * np.hanning(len(data))
                fft = abs(np.fft.fft(data).real)
                fft = fft[:int(len(fft) / 2)]
                frq = np.fft.fftfreq(self.CHUNK, 1.0 / self.RATE)
                frq = frq[:int(len(frq) / 2)]
                self.freq = frq[np.where(fft == np.max(fft))[0][0]] + 1

                #
                self.neonote = self.freq_to_note(self.freq)

                # Shows the peak frequency and the bars for the amplitude
                print(f"peak frequency: {self.freq} Hz, mididnote {self.neonote}:\t {bars}")

            self.amplitude = peak

    def freq_to_note(self, freq: float) -> list:
        """INSERT DOC STRING HERE
        """

        #
        note_number = 12 * math.log2(freq / 440) + 49
        note_number = round(note_number)
        note_position = (note_number - 1) % len(self.list_of_notes)
        neonote = self.list_of_notes[note_position]
        octave = (note_number + 8) // len(self.list_of_notes)

        #
        if 2 <= octave <= 6:

            #
            if octave > 4:
                ticks = octave - 4
                for tick in range(ticks):
                    neonote += "'"

            #
            elif octave < 4:
                if octave == 3:
                    neonote += ","
                elif octave == 2:
                    neonote += ",,"

        return [neonote]

    def terminate(self):
        """safely terminates all streams"""
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


if __name__ == "__main__":
    mic = Listener()
    mic.start()
    while True:
        print(mic.freq,
              mic.amplitude,
              mic.neonote
              )
        sleep(1)
