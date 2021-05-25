class SongQueue:
    # Keeps track of added songs.
    def __init__(self):
        self.queue = []
        self.history = []

    def getQueue(self):
        return self.queue

    def addSong(self, song):
        # Add a song to the queue
        # song: (dict) information of the song
        self.queue.append(song)

    def removeSong(self, song):
        # Remove a song from the queue
        # song: (dict) information of the song
        self.queue.remove(song)

    def popSong(self):
        # Pop a song from the queue
        song = self.queue[0]
        self.queue = self.queue[1:]
        return song

    def moveUp(self, song):
        # Move a song up the queue
        # song: (dict) information of the song
        indx1 = self.queue.index(song)

        if not indx1:
            return
        self.swap(indx1, indx1 - 1)

    def moveDown(self, song):
        # Move a song down the queue
        # song: (dict) information of the song
        indx1 = self.queue.index(song)
        self.swap(indx1, indx1 + 1)

    def swap(self, indx1, indx2):
        # Swap the queue positions of two songs at the given indexes
        # indx1: (int) list index of first song
        # indx2: (int) list index of second song
        swapItem = self.queue[indx2]
        self.queue[indx2] = self.queue[indx1]
        self.queue[indx1] = swapItem
    
    def moveTop(self, song):
        # Move a song to the top of the queue
        # song: (dict) information of the song
        indx1 = self.queue.index(song)
        if not indx1:
            return
        self.queue = [song] + self.queue[:indx1] + self.queue[indx1 + 1:]

    def songInQueue(self, song):
        # Checks if a song is in the queue
        # song: (dict) information of the song
        return song in self.queue

    def addHistory(self, song):
        # Add song to history
        # song: (dict) information of the song
        self.history.append(song)