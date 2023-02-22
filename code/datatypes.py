import typing, os
from pydantic import BaseModel


class WindowsMediaInfo(BaseModel):
    artist: str
    title: str

class File(BaseModel):
    filename: str
    media_info: typing.Optional[WindowsMediaInfo] = None

    def delete(self):
        os.remove(self.filename)