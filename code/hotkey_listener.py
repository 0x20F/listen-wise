import asyncio
from pynput import keyboard
from recorder import Recorder
from transcription_queue import TranscriptionQueue
from win11toast import notify


class HotkeyListener():
    ctrl_pressed: bool = False
    alt_pressed: bool = False

    def __init__(self, recorder: Recorder, queue: TranscriptionQueue) -> None:
        self.recorder: Recorder = recorder
        self.queue: TranscriptionQueue = queue

    async def handle_save_press(self):
        print('[~] Saving buffer to file.')
        file = await self.recorder.buffer_to_wave()
        self.queue.add(file)
        notify('Sanguine', 'Highlight queued for transcription!', audio={'silent': 'true'})

    def handle_ctrl_press(self):
        self.ctrl_pressed = True

    def handle_alt_press(self):
        self.alt_pressed = True

    def on_press(self, key):
        try:
            if \
                key == keyboard.Key.ctrl_l or \
                key == keyboard.Key.ctrl_r:
                
                self.handle_ctrl_press()
                
            elif \
                key == keyboard.Key.alt_l or \
                key == keyboard.Key.alt_r or \
                key == keyboard.Key.alt_gr:
                
                self.handle_alt_press()
            
            elif \
                key.char == 's' and \
                self.ctrl_pressed and \
                self.alt_pressed:

                asyncio.run(self.handle_save_press())
            
            elif \
                key.char == 'c' and \
                self.ctrl_pressed and \
                self.alt_pressed:
                
                print('[i] Clearing saved frames')
                self.recorder.clear()
            
            elif \
                key.char == '\x03' and \
                self.ctrl_pressed:
                
                self.recorder.stop()
                self.queue.stop()
                exit()
            
            else:
                self.ctrl_pressed = False
                self.alt_pressed = False
        except Exception as e:
            pass

    async def listen(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            try:
                listener.join()
            except Exception as e:
                print('[!!] Program exited!')