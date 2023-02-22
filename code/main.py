import threading, asyncio
import sys
from dotenv import load_dotenv

# Our own imports
from recorder import Recorder
from transcription_queue import TranscriptionQueue
from hotkey_listener import HotkeyListener
from pipeline import pipeline, use, Transcriber, Notion, LocalSave, FileSystem

load_dotenv()


# Hotkey constants
ctrl_pressed = False
alt_pressed = False


recorder = Recorder()

if len(sys.argv) > 1:
    if sys.argv[1] == '--list-devices':
        recorder.enumerate_devices()
        exit()


queue = TranscriptionQueue()
hotkeys = HotkeyListener(recorder=recorder, queue=queue)

highline = pipeline(
    use(
        'transcribe', 
        Transcriber(), 
        method='transcribe_file'
    ),
    use(
        'notion', 
        Notion(), 
        method='append_highlight',
        needs=[ 'transcribe', 'pipeline' ]
    ),
    use(
        'local-storage',
        LocalSave(),
        method='save_highlight',
        needs=[ 'transcribe', 'pipeline' ]
    ),
    use(
        'cleanup',
        FileSystem(),
        method='delete_file',
        needs=[ 'pipeline' ]
    )
)


async def main():
    thread = threading.Thread(target=recorder.record)
    thread.start()

    queueThread = threading.Thread(
        target=queue.listen, 
        args=(highline.run,)
    )
    queueThread.start()

    await hotkeys.listen()
    thread.join()
    queueThread.join()


asyncio.get_event_loop().run_until_complete(main())
