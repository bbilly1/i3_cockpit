""" prints the state of mpd to use as a notification """
import subprocess


def print_state(artist, album, song_title, mpd_status):
    """ print three lines for i3blocks """
    # setup based on mpd_status
    if mpd_status == 'play':
        print_main = f'{artist} - {album} - {song_title}'
        print_small = f'{artist} - {song_title}'
        print_color = '#FFFFFF'
    elif mpd_status == 'pause':
        print_main = f'{artist} - {song_title}'
        print_small = f'{song_title}'
        print_color = '#404040'
    # print
    print(print_main)
    print(print_small)
    print(print_color)


def get_state(client, cover_art_path):
    """ sends a notification of the current status """
    # read out status from client
    now_playing = client.currentsong()
    client_status = client.status()
    # parse status
    music_file = now_playing['file']
    artist = now_playing['artist']
    album = now_playing['album']
    song_title = now_playing['title']
    # try to write cover art to temp file
    cover_art_blob = client.readpicture(music_file)
    try:
        with open(cover_art_path, 'w+b') as cover_file:
            cover_file.write(cover_art_blob['binary'])
    except KeyError:
        cover_art_blob = False
    # set player status icon
    mpd_status = client_status['state']
    if mpd_status == 'play':
        icon = ""
    elif mpd_status == 'pause':
        icon = ""
    # print for i3blocks
    print_state(artist, album, song_title, mpd_status)
    # send message
    title = icon + '\t' + artist
    message = album + " - " + song_title
    subprocess.call(['notify-send', title, message, '-i', cover_art_path])
