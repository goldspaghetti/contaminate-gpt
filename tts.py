import openai
import sounddevice as sd
from TTS.api import TTS
import numpy as np
import pyrubberband as pyrb
import queue, threading, time
from config import *
import torch
import soundfile as sf
from lipsync import Lipsync

# openai.api_key = OPEN_AI_KEY
class Sound():
    # curr_playing = False
    audio = []
    def __init__(self, save_audio=True, save_text=True, volume=1):
        # x = torch.rand(5, 3)
        # print(x)
        # print(torch.cuda.is_available())

        self.tts = TTS("tts_models/en/ljspeech/vits", gpu=False)
        # tts_models/en/vctk/vits"

        self.speak_queue = queue.Queue()

        self.client = openai.OpenAI(api_key=OPEN_AI_KEY)

        # audio stuff
        self.curr_playing = False
        self.delay = 1  #delay in secs before saying something new
        self.last_speak = time.time()

        self.audio = []
        self.volume = volume
        self.lipsync = Lipsync()
        devices = sd.query_devices()
        # print(devices)
        # self.audio_device = sd.default.device[1]
        # print(self.audio_device)
        # for device in devices:
        #     # print(device["name"])
        #     # print(device)
        #     if device["name"] == "virtual audio cable": # change name
        #         self.audio_device = device["index"]
        #         sd.default.device = device["index"]
        #         break
        self.audio_device = sd.default.device[1]
        self.music = sf.read("game_jam3.wav", dtype="float32")
        sd.play(self.music[0]*self.volume, samplerate=44100, loop=True)

        fish_thread = threading.Thread(target=self.try_speak_loop, daemon=True)
        fish_thread.start()
        # sd.default.device
        # print(self.audio_device.name)
        # self.audio_device = sd.query_devices("virtual audio cable") #change name to match actual device name!
        # if self.audio_device:
        #     self.audio_device = self.audio_device[0].name
        # else:
        #     self.audio_device = sd.default.device[1]
        # self.audio_stream = sd.OutputStream(samplerate=22050, device=self.audio_device, channels=2, finished_callback=self.set_audio_false)

    def audio_callback(self, outdata, frames, time, status):
        print("AAA")
        if TextToSpeech.curr_playing:
            
        # if self.curr_playing:
            outdata[:] = TextToSpeech.audio
            print(len(TextToSpeech.audio))

    def set_audio_false(self):
        self.curr_playing = False

    def nightcore(self, sample,sr):
        return pyrb.time_stretch(np.asarray(sample), sr, 2.0)

    def gpt(self, prompt):
        completion = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ]
        )

        print(completion.choices[0].message)
        # save to text.txt
        with open("text.txt", "w") as f:
            f.write(completion.choices[0].message)

        return completion.choices[0].text

    def try_speak(self, prompt):
        self.speak_queue.put(prompt)

    def try_speak_loop(self):
        while True:
            # print("AA")
            # print(self.speak_queue.empty())
            if not self.speak_queue.empty():
                print("A")
                prompt = self.speak_queue.get()
                # process_time does not count sleeping
                if time.time() - self.last_speak > self.delay and not self.curr_playing:
                    print("speaking ")
                    self.speak(prompt)
                else:
                    print("refuse to speak")
                    print(time.time() - self.last_speak)
                    print(self.curr_playing)
            time.sleep(0.01)
                
    def speak(self, prompt):    # returns a list of lipsync values
        self.curr_playing = True
        self.tts.tts_to_file(text=prompt, file_path="speech.wav")
        # array = self.tts.tts(text=prompt, speaker=self.tts.speakers[17])
        tts_speak = sf.read("speech.wav", dtype="float32")
        with open("text.txt", "w") as f:
            f.write(prompt)
        
        self.lipsync.get_features()
        # send info to change facial features

        sd.play(tts_speak[0]*self.volume, 22050)
        tatus = sd.wait()
        sd.stop()
        self.last_speak = time.time()
        self.curr_playing = False
        # array = self.nightcore(array, 22050)
        # print(self.audio)
        # TextToSpeech.curr_playing = True
        # make audio from gpt text
        # thisll take a while, you can do shit as it renders

        # array = self.tts.tts(text=gpt(prompt), speaker=tts.speakers[17])
        # self.audio = self.tts.tts(text=prompt, speaker=self.tts.speakers[17])
        # interesting sounding vctks: 3,13,14,17,
        # 75, 65, 74, 73, 98, 64

        # nightcore
        # array = nightcore(array,22050)

if __name__ == "__main__":
    tts = Sound ()
    # thread = threading.Thread(target=tts.try_fishspeak, daemon=True)
    # thread.start()
    time.sleep(1)
    # tts.speak_queue.put(tts.gpt("can you laugh?"))
    time.sleep(6)
    # tts.speak_queue.put(tts.gpt("What do you think about Xi Jinping"))
    tts.try_speak("What do you think about Xi Jinping")
    # tts.fishspeak("Can you laugh?")
    # tts.fishspeak("Can you laugh?")
    time.sleep(5)
    # sd.play(tts.tts(text="Check the manual build section if you wish to compile the bindings from source to enable additional modules such as CUDA.", speaker=tts.speakers[3]), 22050)
    status = sd.wait()
    sd.stop()