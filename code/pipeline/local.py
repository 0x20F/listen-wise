import os
from dotenv import load_dotenv
from pipeline import PipelineUsable
from datatypes import File

load_dotenv()

LOCAL_PATH = os.getenv('LOCAL_PATH')

class LocalSave(PipelineUsable):
    def __init__(self) -> None:
        super().__init__()

    def setup(self) -> None:
        if not LOCAL_PATH:
            self.logger('Highlights will not be saved locally.')
            return

        self.logger('Initializing local storage in: {}'.format(LOCAL_PATH))

    def save_highlight(self, info: tuple[str, str], file_data: File) -> None:
        if not LOCAL_PATH:
            return

        self.logger('Saving highlight to file: {}'.format(LOCAL_PATH))

        title, text = info

        file = open(LOCAL_PATH, 'a')
        file.write('{}\n'.format(title))
        file.write('{}\n'.format(text))
        file.write('created at: {}\n'.format(file_data.format_created_at()))
        file.write('\n\n')
        file.close()