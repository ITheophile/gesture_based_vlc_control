import vlc

media_pth = "E:/media/August.Rush.FRENCH.DVDRiP.XviD-iD.AVI"
media = vlc.MediaPlayer(media_pth)


def control_vlc(command, media):

    if command == 'Play':
        media.play()

    elif command == 'Pause' and media.is_playing() == 1:
        media.pause()

    elif command == 'Stop':
        media.stop()

    elif command == 'Volume_Up':
        current_vol = media.audio_get_volume()
        media.audio_set_volume(current_vol + 1)

    elif command == 'Volume_Down':
        current_vol = media.audio_get_volume()
        media.audio_set_volume(current_vol - 1)

    # Second condition checks if the media is muted(1) or not(0)
    elif command == 'Mute' and media.audio_get_mute() == 0:
        media.audio_toggle_mute()
    elif command == 'Unmute' and media.audio_get_mute() == 1:
        media.audio_toggle_mute()
