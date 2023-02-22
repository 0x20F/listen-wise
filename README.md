<h1>
listen-wise
</h1>

A simple program for avid listeners of audio content.

<br/>

## Why?
Because sometimes you just want to listen to the audiobook/podcast/youtube video without also rushing to take notes. This allows you to quickly mark the passages that you deemed important and continue listening.

Knowing well that you'll come back and review your saved notes later. The Ai won't be perfect.

Oh and also we want all this magic to happen without us needing an internet connection (unless you use notion, readwise, or other things). Transcription to a local file works without internet.
<br/>

## How?
A few things to keep in mind:
1. It only runs on Windows for the time being.
2. You need to figure out which device the recording should happen through on your own.
3. You need to figure out your own Notion (and other API) tokens.

With that in mind, here's how you get it going.

### 1. Clone the repo
```bash
git clone https://github.com/0x20F/listen-wise.git
cd listen-wise
```

### 2. Install dependencies
> Make sure you have poetry installed
```bash
poetry install
```

### 3. Configure
Copy the example environment file

(powershell)
```powershell
Copy .env.example .env
```

(bash)
```bash
cp .env.example .env
```

And update the contents of the file to suit your needs.
Remove any variables that you don't need.

If you don't want anything to do with notion, remove the whole notion section, and so on.

> The required variables are `HIGHLIGHT_LENGTH_IN_SECONDS`, `INPUT_DEVICE_INDEX` and `WHISPER_SIZE`

> If you don't know what index your input device is at you can run the program with the `--list-devices` parameter to get a list of all devices and their indexes.

### 4. Run
Once configured, you can run the entire program with the following:
```bash
poetry run python code/main.py
```

and you should be greeted with some information about all the modules that are being set up based on your configuration file. Something like this:
```
[transcribe] Initializing Whisper neural net with size small
[notion] Initializing Notion client. Tokens were provided!
[local-storage] Highlights will not be saved locally.
[~] Recorder started
...
```
> Note: On the first run, it might look like it's stuck on initializing the whisper neural net. That's because it's actually downloading the model that you asked for, it's purely dependent on your internet connection.

### 5. Use
You control the program through hotkeys (web interface might come later).
> Note: Do not press the keys at the same time. Press one, release it; press the second one, release it. If all required keys are pressed in order the command will be
executed.

#### 5.1 - Start transcribing
```
Ctrl + Alt + s
```
This will get the last specified amount of seconds, save it to an audio file, and queue it for transcription. The logs should tell you what's going on.

#### 5.2 - Clear buffer
```
Ctrl + Alt + c
```
The program will always keep just enough recorded data to always have the amount of seconds that you asked for in a highlight, nothing more. If you'd like to force a wipe of that data, this is the command for you.