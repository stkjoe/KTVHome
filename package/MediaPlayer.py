import vlc

class MediaPlayer():
    def __init__(self, songQueue, marqueeFunc):
        self.player = vlc.MediaPlayer()
        self.songQueue = songQueue
        self.currentSong = None
        self.marqueeFunc = marqueeFunc

    def restartSong(self):
        if not self.currentSong:
            return
        self.player.set_media(vlc.Media(self.currentSong["song_path"]))
        self.player.play()

        if len(self.songQueue.getQueue()) > 1:
            text = []
            text.append("正在播放/Now Playing：{} - {}".format(self.currentSong["artist_name"], self.currentSong["song_title"]))
            text.append("下一首歌/Next Song: {} - {}".format(self.songQueue.getQueue()[0]["artist_name"], self.songQueue.getQueue()[0]["song_title"]))
            self.marqueeFunc(text)
        else:
            self.marqueeFunc("正在播放/Now Playing：{} - {}".format(self.currentSong["artist_name"], self.currentSong["song_title"]))

    def pauseSong(self):
        self.player.pause()

    def skipSong(self):
        if len(self.songQueue.getQueue()) == 0:
            return
        self.currentSong = self.songQueue.popSong()
        self.restartSong()

    def swapTrack(self):
        self.player.audio_set_track((self.player.audio_get_track() % (self.player.audio_get_track_count() - 1)) + 1)
