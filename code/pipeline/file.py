from pipeline import PipelineUsable
from datatypes import File

class FileSystem(PipelineUsable):
    def setup(self) -> None:
        self.logger('Initializing file system events for .wav and .txt files.')

    def delete_file(self, file: File):
        self.logger('Deleting file: {}'.format(file.filename))
        file.delete()