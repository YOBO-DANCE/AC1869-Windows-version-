# 1869AC

**1869AC** is a lightweight, terminal-based music player built in Python. It features an animated TUI (Terminal User Interface) complete with a live timeline progress bar, a spinning vinyl icon, time tracking, and interactive keyboard controls powered by `libvlc`.

---

## Features

- **Terminal UI Dashboard:** Displays real-time audio progress, elapsed vs. total time, and current playback status.
- **Spinning Vinyl Animation:** dynamic vinyl indicator (`◐` `◓` `◑` `◒`) that rotates during active playback ( *it is just half circles emojies rotating* ).
- **Interactive Playback Controls:** Non-blocking terminal input for real-time player manipulation without pressing Enter.
- **Seeking & Navigation:** Jump forward or backward by 10-second increments without freezing the ui or the terminal.
- **VLC Playback Engine:** Uses `python-vlc` for audio processing.

---

## Controls

| Key | Action |
| :--- | :--- |
| **`Space`** or **`k`** | Play / Pause |
| **`d`** or **`l`** | Seek Forward (10 seconds) |
| **`a`** or **`j`** | Seek Backward (10 seconds) |
| **`q`** | Quit application |

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
