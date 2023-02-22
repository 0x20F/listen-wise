import whisper, os
from dotenv import load_dotenv
from datatypes import File
from pipeline import PipelineUsable

load_dotenv()

WHISPER_SIZE = os.getenv('WHISPER_SIZE') or 'small'


class Transcriber(PipelineUsable):
    def setup(self) -> None:
        self.logger('Initializing Whisper neural net with size {}'.format(WHISPER_SIZE))
        self.model = whisper.load_model(WHISPER_SIZE)

    def transcribe_file(self, file: File) -> tuple[str, str]:
        name = file.filename
        info = file.media_info

        self.logger('Transcribing file content for file -> {}'.format(name))
        result = self.model.transcribe(name, fp16=False)

        title = 'No title'

        if info is not None:
            artist = ''

            if len(info.artist) > 0:
                artist = '{} - '.format(info.artist)

            title = '{}{}'.format(artist, info.title)

        return (title, result['text'])