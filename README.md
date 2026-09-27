# 1869AC

**1869AC** is an animated, terminal-based music player built in Python. Powered by `libvlc` and `pygame.mixer`, it features multi-playlist support, multiple folder importing, volume controls, shuffle queueing, and a custom ANSI terminal interface with UI sound effects.

---

## Features

- **Music Importer:** Scans any directory on your computer for audio files (`.mp3`, `.wav`, `.flac`, `.m4a`, `.ogg`) and saves them as custom named playlists.
  
- **Interactive Startup Menu:** Displays available playlists on launch for quick selection.
  
- **Track Navigation:** Next (`m`) and previous (`n`) song controls with history shuffle memory.
  
- **Volume & Sound Effects:** Real-time 10-level volume adjustments (`o`/`p`) complete with audio feedback using `pygame.mixer`.
  
- **Playback Modes:** Shuffle mode (`s`) and single-track with live visual status symbols.
  
- **Terminal UI Dashboard:** Renders a progress timeline bar, current date/clock, elapsed vs. total time, and an animated vinyl indicator.
  
- **Clean Console Output:** Automatically suppresses low-level VLC stderr logging to preserve terminal clean-ups.

---

## Key Controls

| Key | Action |
| :--- | :--- |
| **`Space`** or **`k`** | Play / Pause|
| **`m`** | Next Track|
| **`n`** | Previous Track|
| **`d`** or **`l`** | Seek Forward (10 seconds)|
| **`a`** or **`j`** | Seek Backward (10 seconds)|
| **`p`** | Volume Up 10%|
| **`o`** | Volume Down 10%|
| **`s`** | Toggle Shuffle Mode|
| **`e`** | Toggle Repeat Mode (Auto / Single Loop) (doesn't work for now, just the symbol changes)|
| **`q`** | Quit Player

---

## Requirements & Installation

### Prerequisites
1. **Python 3.8+**
2. **It requires `vlc` to run because the backend is just vlc media player 😅!!**
3. **System VLC Media Player** (Required by `python-vlc` bindings):
   - **macOS:** `brew install --cask vlc`
   - **Linux (Ubuntu):** `sudo apt install vlc`

### Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/mrpeng4/1869AC.git](https://github.com/mrpeng4/1869AC.git)
   cd 1869AC
