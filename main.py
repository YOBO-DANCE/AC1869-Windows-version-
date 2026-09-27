import os
import sys
from pathlib import Path

# 1. SETUP PATHS FIRST (Critical for PyInstaller to find local files)
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    bundle_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    exe_dir = Path(sys.executable).parent
    
    # Add bundle directory to sys.path so bundled widgets.py can be found
    if str(bundle_dir) not in sys.path:
        sys.path.insert(0, str(bundle_dir))
        
    # Add executable directory to sys.path so external songs_path.py can override
    if str(exe_dir) not in sys.path:
        sys.path.insert(0, str(exe_dir))
        
    os.chdir(exe_dir)
else:
    # Running as standard script
    exe_dir = Path(__file__).parent.resolve()
    if str(exe_dir) not in sys.path:
        sys.path.insert(0, str(exe_dir))
    os.chdir(exe_dir)

# 2. CREATE CONFIG FILE IF MISSING
songs_file_path = Path("songs_path.py")
if not songs_file_path.exists():
    songs_file_path.write_text("# Auto-imported playlist file\n", encoding="utf-8")

# 3. SUPPRESS TERMINAL ERRORS (Keeps UI clean)
stderr_fd = sys.stderr.fileno()
devnull = os.open(os.devnull, os.O_WRONLY)
os.dup2(devnull, stderr_fd)
os.close(devnull)

# 4. PERFORM IMPORTS NOW THAT SYS.PATH IS FIXED
import time
import importlib
import pygame
import widgets
import vlc
import songs_path

# --- REST OF THE APP ---
def import_songs():
    global continue_or_not
    with open("songs_path.py", "r") as song:
        if not song.read().strip():
            print("It seems like there are no songs added. Please paste a "
                  "directory path down below where all your music is located")
            user_directory = input("")
            print("please provide a name for the playlist:")
            user_directory_name = input("")
            continue_or_not = widgets.append_folder_to_songs_path(user_directory, user_directory_name)
            importlib.reload(songs_path)
        else:
            continue_or_not = True

with open("songs_path.py", "r") as song:
    if not song.read().strip():
        import_songs()

playlists_list = []

for variable_name in dir(songs_path):
    if not variable_name.startswith("__"):
        data = getattr(songs_path, variable_name)
        if isinstance(data, list):
            playlists_list.append(variable_name)

for index in range(0, len(playlists_list)):
    print(f"{index}. {playlists_list[index]}")

print("please enter the number next to the playlist you want to play:")
playlist_index = input("")

name_for_Playlist = playlists_list[int(playlist_index)]
playlist = getattr(songs_path, name_for_Playlist)

current_song_index = 0
current_song = playlist[current_song_index]
current_song_name = current_song.split("/")
continue_or_not = True

if continue_or_not:
    player = vlc.MediaPlayer(current_song)
    player.play()

    while player.get_length() <= 0:
        time.sleep(0.1)
    length_of_song = player.get_length() / 1000
    widget = widgets.UiWidgets(current_song_name[-1], player)

    print(f"\033[3J\033[H\033[2J")
    widget.loop_for_song(player, length_of_song, playlist, current_song_index)
else:
    print("please rerun the code to retry")
    sys.exit()
