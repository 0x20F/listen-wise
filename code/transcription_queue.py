import time
from typing import Callable, List
from datatypes import File


class TranscriptionQueue():
    def __init__(self) -> None:
        self.should_exit = False
        self.items: List[File] = []

    def listen(self, on_next: Callable[[File], None]):
        while not self.should_exit:
            if len(self.items) == 0:
                time.sleep(1)
                continue

            file = self.items.pop()

            on_next(file)

            file.delete()

            print('[+] Done transcribing file -> {}'.format(file.filename))
            print('[i] Items left in queue: {}'.format(len(self.items)))
            print('\n\n\n\n')

    def add(self, file: File):
        self.items.append(file)

    def stop(self):
        self.should_exit = True