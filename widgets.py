import os
import time
import sys
import select
import termios
import tty
import vlc
import datetime
import importlib.util
from pathlib import Path
from pygame import mixer
import random


def get_base_dir():
    """Folder the app is actually running from, whether it's a plain
    .py script or a compiled PyInstaller executable. Used to find the
    click-sound mp3 and songs_path.py next to wherever the app really
    lives, instead of assuming the current working directory."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def songs_path_file():
    """Absolute path to the live, editable songs_path.py sitting next
    to the app."""
    return os.path.join(get_base_dir(), "songs_path.py")


def load_playlists():
    """Read songs_path.py fresh off disk every time it's called, instead
    of relying on a cached `import songs_path`. A cached import gets
    frozen into a compiled exe at build time and never changes again,
    so playlists added later would never show up. This always reflects
    whatever is on disk right now. Returns {playlist_name: [song_paths]}."""
    songs_file = songs_path_file()
    spec = importlib.util.spec_from_file_location("songs_path_live", songs_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    playlists = {}
    for variable_name in dir(module):
        if not variable_name.startswith("__"):
            data = getattr(module, variable_name)
            if isinstance(data, list):
                playlists[variable_name] = data
    return playlists

class UiWidgets:

    def __init__(self, name_of_song, player):
        mixer.init()
        sound_path = os.path.join(get_base_dir(), "turning_pages-ui-toggle-off-confirmation-608627.mp3")
        self.click_sound = mixer.Sound(sound_path)
        self.song = name_of_song
        self.current_sec = 0
        self.current_min = 0
        self.current_timeline_part = 0
        self.seconds_for_vinyl = 0
        self.new_timeline = "-------------------------"
        self.vinyl = ["◐", "◓", "◑", "◒"]
        self.volume_level = 10
        self.volume_list = ["⏹"] * 10
        player.audio_set_volume(100)
        self.play_pause = "⏸"
        self.current_vinyl = "◐"
        self.current_vinyl_frame = 0
        self.line_list = ["-"] * 25
        self.shuffle = False
        self.shuffle_symbol = "⇉"
        self.shuffled_song_list = []
        self.loop_type = "auto"
        self.loop_type_symbol = "↬"

    # _________this snippet is made by AI sorry my brain was not braining__________
    def check_key_presses(self):
        """Checks for non-blocking keypresses."""
        if select.select([sys.stdin], [], [], 0)[0]:
            key = sys.stdin.read(1)
            if key == '\x1b':
                additional = sys.stdin.read(2)
                if additional == '[C':
                    return 'RIGHT'
                elif additional == '[D':
                    return 'LEFT'
            return key
        return None
    # _____________________________________________________________________________


    def loop_for_song(self, player, song_time, playlist, current_index):

        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        print("\033[?25l", end="")

        try:
            while True:
                self.now_real_time = datetime.datetime.now().strftime("%d %b %Y %I:%M")
                self.play_pause = "⏸"
                key = self.check_key_presses()
                if key:

                    if key in (' ',"k"):
                        self.play_pause = "▶"# Space = Pause/Play
                        self.click_sound.play()
                        player.pause()

                    elif key in ('d',"l"):
                        self.click_sound.play()
                        new_ms = min(player.get_time() + 10000, int(song_time * 1000))
                        player.set_time(new_ms)
                        self.sync_timeline(song_time, new_ms)

                    elif key in ('a',"j"):
                        self.click_sound.play()
                        new_ms = max(player.get_time() - 10000, 0)
                        player.set_time(new_ms)
                        self.sync_timeline(song_time, new_ms)

                    elif key == "p":
                        if self.volume_level < 10:
                            self.click_sound.play()
                            self.volume_level += 1
                            self.volume_list = ["⏹"] * self.volume_level + [" "] * (10 - self.volume_level)
                            player.audio_set_volume(self.volume_level * 10)

                    elif key == "o":
                        if self.volume_level > 0:
                            self.click_sound.play()
                            self.volume_level -= 1
                            self.volume_list = ["⏹"] * self.volume_level + [" "] * (10 - self.volume_level)
                            player.audio_set_volume(self.volume_level * 10)

                    elif key == "s":
                        self.click_sound.play()
                        if self.shuffle:
                            self.shuffle = False
                            self.shuffle_symbol = "⇉"
                        else:
                            self.shuffle = True
                            self.shuffle_symbol = "⤭"

                    elif key == "e":
                        self.click_sound.play()
                        if self.loop_type == "one":
                            self.loop_type = "auto"
                            self.loop_type_symbol = "↬"
                        else:
                            self.loop_type = "one"
                            self.loop_type_symbol = "⥁"

                    elif key == "m":
                        player, song_time, current_index = self.next_song(player, playlist, current_index, self.shuffle)

                    elif key == "n":
                        player, song_time, current_index = self.previous_song(player, playlist, current_index, self.shuffle)

                    elif key == 'q':  # Quit
                        player.stop()
                        self.click_sound.play()
                        self.play_pause = "▶"
                        self.render(song_time)
                        break


                if player.is_playing():
                    time.sleep(0.1)
                    current_ms = max(0, player.get_time())
                    total_sec = int(current_ms / 1000)
                    self.current_min = int(total_sec / 60)
                    self.current_sec = total_sec % 60
                    self.sync_timeline(song_time, current_ms)
                    self.seconds_for_vinyl += 0.1
                    if self.seconds_for_vinyl >= 1.0:
                        self.change_vinyl()
                        self.seconds_for_vinyl = 0
                    self.render(song_time)
                else:
                    time.sleep(0.1)

                if player.get_state() == vlc.State.Ended:
                    self.new_timeline = "========================="
                    self.play_pause = "▶"
                    self.render(song_time)
                    player, song_time, current_index = self.next_song(player, playlist, current_index, self.shuffle)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSANOW, old_settings)
            print("\033[?25h\n")

    def sync_timeline(self, song_time, current_ms):
        current_sec = max(0, min(current_ms / 1000, song_time))
        progress_ratio = current_sec / song_time if song_time > 0 else 0

        total_units = progress_ratio * len(self.line_list)
        filled_units = int(total_units)

        self.current_timeline_part = filled_units
        self.line_list = ["="] * filled_units + ["-"] * (len(self.line_list) - filled_units)
        self.new_timeline = "".join(self.line_list)

    def change_vinyl(self):
        self.current_vinyl = self.vinyl[self.current_vinyl_frame]
        if self.current_vinyl_frame < 3:
            self.current_vinyl_frame += 1
        else:
            self.current_vinyl_frame = 0

    def render(self, song_time):
        total_min = int(song_time // 60)
        total_sec = int(song_time % 60)
        total_time_str = f"{total_min}:{total_sec:02d}"
        lines = [
            f"[{self.new_timeline}] [{self.current_min}:{self.current_sec:02d}|{total_time_str}] [ {self.loop_type_symbol} {self.play_pause} {self.shuffle_symbol} ] [{''.join(self.volume_list)}]",
            f"[ {self.current_vinyl} {self.song}] [{self.now_real_time}]"
        ]
        for line in lines:
            print(f"\x1b[2K\r{line}")
        print(f"\x1b[{len(lines)}A", end="", flush=True)

    def reset(self, song_name):
        self.song = song_name
        self.current_sec = 0
        self.current_min = 0
        self.current_timeline_part = 0
        self.seconds_for_vinyl = 0
        self.new_timeline = "-------------------------"
        self.line_list = ["-"] * 25
        self.play_pause = "⏸"

    def next_song(self, player, playlist, current_index, shuffle):
        if shuffle:
            self.shuffled_song_list.append(current_index)
            next_index = random.randint(0, len(playlist) - 1)
        else:
            next_index = (current_index + 1) % len(playlist)
        player.stop()
        self.click_sound.play()
        next_song_path = playlist[next_index]

        path_parts = next_song_path.split('/')
        file_name_with_extension = path_parts[-1]

        next_song_name = file_name_with_extension
        new_player = vlc.MediaPlayer(next_song_path)
        new_player.audio_set_volume(self.volume_level * 10)
        new_player.play()

        while new_player.get_length() <= 0:
            time.sleep(0.1)

        new_song_time = new_player.get_length() / 1000
        self.reset(next_song_name)

        return new_player, new_song_time, next_index

    def previous_song(self, player, playlist, current_index, shuffle):
        if shuffle:
            if self.shuffled_song_list != []:
                previous_index = self.shuffled_song_list.pop(-1)
            else:
                previous_index = (current_index - 1) % len(playlist)
        else:
            previous_index = (current_index - 1) % len(playlist)
        player.stop()
        self.click_sound.play()
        previous_song_path = playlist[previous_index]

        path_parts = previous_song_path.split('/')
        file_name_with_extension = path_parts[-1]
        previous_song_name = file_name_with_extension

        new_player = vlc.MediaPlayer(previous_song_path)
        new_player.audio_set_volume(self.volume_level * 10)
        new_player.play()

        while new_player.get_length() <= 0:
            time.sleep(0.1)

        new_song_time = new_player.get_length() / 1000
        self.reset(previous_song_name)

        return new_player, new_song_time, previous_index

def append_folder_to_songs_path(folder_path, playlist_name):
    path = Path(folder_path).expanduser().resolve()
    if not path.is_dir():
        print(f"Error: Directory '{folder_path}' not found.")
        return False
    valid_exts = {'.mp3', '.wav', '.flac', '.m4a', '.ogg'}
    audio_files = [str(f) for f in path.rglob('*') if f.suffix.lower() in valid_exts]
    if not audio_files:
        print(f"No audio files found in '{folder_path}'.")
        return False
    python_code = f"\n# Auto-imported playlist from: {path}\n{playlist_name} = [\n"
    python_code += "".join(f"    {repr(audio)},\n" for audio in audio_files)
    python_code += "]\n"
    with open(songs_path_file(), "a", encoding="utf-8") as f:
        f.write(python_code)
    print(f"Added {len(audio_files)} songs to songs_path.py as list '{playlist_name}'.")
    return True
