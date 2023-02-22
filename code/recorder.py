import numpy as np, pyaudio, time, wave, os
from system import get_media_info
from datatypes import File, WindowsMediaInfo
from dotenv import load_dotenv

load_dotenv()


# Recording constants
CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
HIGHLIGHT_SECONDS = int(os.getenv('HIGHLIGHT_LENGTH_IN_SECONDS', 30))
SILENCE_THRESHOLD = 1
TOTAL_ALLOWED_FRAMES = RATE * HIGHLIGHT_SECONDS / CHUNK
INPUT_DEVICE_INDEX=int(os.getenv('INPUT_DEVICE_INDEX') or 2)


def is_mostly_silence(audio_data, threshold):
    rms = np.sqrt(np.mean(np.square(audio_data)))
    return rms < threshold


class Recorder():
    def __init__(self) -> None:
        self.frames = []
        self.should_exit = False
        self.client = pyaudio.PyAudio()
        self.stream = self.client.open(
            channels=CHANNELS,
            format=FORMAT,
            rate=RATE,
            input=True,
            input_device_index=INPUT_DEVICE_INDEX, # Stereo mix on windows
            frames_per_buffer=CHUNK
        )

    def record(self):
        print('[~] Recorder started on device with id {}'.format(INPUT_DEVICE_INDEX))

        while not self.should_exit:
            data = self.stream.read(CHUNK)
            audio_data = np.frombuffer(data, dtype=np.int16)

            if not is_mostly_silence(audio_data, SILENCE_THRESHOLD):
                if len(self.frames) >= TOTAL_ALLOWED_FRAMES:
                    self.frames.pop(0)

                self.frames.append(data)

            time.sleep(CHUNK / RATE)

    def clear(self):
        self.frames = []

    def stop(self):
        self.should_exit = True
        self.stream.stop_stream()
        self.stream.close()
        self.client.terminate()

    async def buffer_to_wave(self) -> File:
        filename = 'sanguine-{}.wav'.format(time.time())
        media_info = await get_media_info()

        data = File(filename = filename)

        if media_info != None:
            data.media_info = WindowsMediaInfo(
                artist = media_info['artist'],
                title = media_info['title']
            )

        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.client.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        return data

    def enumerate_devices(self):
        info = self.client.get_host_api_info_by_index(0)
        numdevices = int(info.get('deviceCount') or 0)

        # for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
        for i in range (0, numdevices):
            if int(self.client.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels') or 0) > 0:
                print("Input Device id ", i, " - ", self.client.get_device_info_by_host_api_device_index(0, i).get('name'))

            if int(self.client.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels') or 0) > 0:
                print("Output Device id ", i, " - ", self.client.get_device_info_by_host_api_device_index(0, i).get('name'))