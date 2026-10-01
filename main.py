# import os
# import sys

# stderr_fd = sys.stderr.fileno()
# devnull = os.open(os.devnull, os.O_WRONLY)
# os.dup2(devnull, stderr_fd)
# os.close(devnull)

import widgets
import vlc
import time
import songs_path

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
            exit()
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

print("please enter the number next to the playlist, for the playlist you want to play:")
playlist_index = input("")

name_for_Playlist = playlists_list[int(playlist_index)]
try:
    playlist = getattr(songs_path, name_for_Playlist)
except IndexError:
    print("tis playlist does not exists")


current_song_index = 0
current_song = playlist[current_song_index]
current_song_name = current_song.split("/")
continue_or_not = True

import_songs()

if continue_or_not:
    player = vlc.MediaPlayer(current_song)
    player.play()

    while player.get_length() <= 0:
        time.sleep(0.1)
    length_of_song = player.get_length()/1000
    widget = widgets.UiWidgets(current_song_name[-1], player)

    print(f"\033[3J\033[H\033[2J")
    widget.loop_for_song(player,length_of_song, playlist, current_song_index)
else:
    print("please rerun the code to retry")
    exit()
