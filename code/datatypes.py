import typing, os
from pydantic import BaseModel
from datetime import datetime


class WindowsMediaInfo(BaseModel):
    artist: str
    title: str

class File(BaseModel):
    filename: str
    media_info: typing.Optional[WindowsMediaInfo] = None
    created_at: datetime = datetime.now()

    def delete(self):
        os.remove(self.filename)

    def format_created_at(self):
        return self.created_at.strftime('%m/%d/%Y - %H:%M:%S')