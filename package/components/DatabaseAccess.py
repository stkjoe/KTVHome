import sqlite3

# Helper functions, not to be used outside of this
def connect():
    conn = sqlite3.connect("db/database.db")
    return conn

def disconnect(conn):
    conn.commit()
    conn.close()

def fetchResults(executeLine):
    conn = connect()
    cur = conn.cursor()
    cur.execute(executeLine)
    desc = cur.description
    column_names = ['type'] + [i[0] for i in desc[1:]]
    results = [dict(zip(column_names, row))
                for row in cur.fetchall()]
    disconnect(conn)
    return results

def execute(executeLine):
    conn = connect()
    cur = conn.cursor()
    cur.execute(executeLine)
    disconnect(conn)

# Function to create tables if they do not exist
def startUp():
    conn = connect()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS languages (
                    language_id INTEGER NOT NULL,
                    language_name TEXT NOT NULL,
                    language_path TEXT,
                    PRIMARY KEY (language_id)
                    )
                    ''')
    cur.execute('''CREATE TABLE IF NOT EXISTS artists (
                    artist_id INTEGER NOT NULL, 
                    artist_name TEXT NOT NULL,
                    artist_path TEXT,
                    language_id INTEGER NOT NULL,
                    favourited INTEGER DEFAULT 0,
                    PRIMARY KEY (artist_id),
                    FOREIGN KEY (language_id) REFERENCES language (language_id)
                        ON DELETE NO ACTION ON UPDATE CASCADE
                    )
                    ''')
    cur.execute('''CREATE TABLE IF NOT EXISTS songs (
                    song_id INTEGER NOT NULL,
                    song_title TEXT NOT NULL,
                    artist_id INTEGER NOT NULL,
                    playcount INTEGER DEFAULT 0,
                    favourited INTEGER DEFAULT 0,
                    song_path TEXT NOT NULL,
                    PRIMARY KEY (song_id),
                    FOREIGN KEY (artist_id) REFERENCES artist (artist_id)
                        ON DELETE NO ACTION ON UPDATE CASCADE
                    )
                    ''')
    cur.execute('''CREATE TABLE IF NOT EXISTS playlists (
                    playlist_id INTEGER NOT NULL,
                    playlist_name TEXT NOT NULL,
                    PRIMARY KEY (playlist_id)
                    )
                    ''')
    cur.execute('''CREATE TABLE IF NOT EXISTS playlist_videos (
                    id INTEGER NOT NULL,
                    playlist_id INTEGER NOT NULL,
                    song_id INTEGER NOT NULL,
                    PRIMARY KEY (id),
                    FOREIGN KEY (playlist_id) REFERENCES playlists (playlist_id)
                        ON DELETE CASCADE ON UPDATE NO ACTION,
                    FOREIGN KEY (song_id) REFERENCES songs (song_id)
                        ON DELETE CASCADE ON UPDATE NO ACTION
                    )
                    ''')
    disconnect(conn)

# Function for all languages
def getLanguages(keyword):
    return fetchResults("SELECT 'languages', * FROM languages WHERE language_name LIKE '%{}%'".format(
        keyword
        ))

# Function for all artists
def getSongArtists(keyword, language=""):
    return fetchResults("SELECT 'artists', * FROM artists WHERE artist_name LIKE '%{}%'{}".format(
        keyword, 
        " AND language_id = {}".format(language) if language != "" else ""
        ))

# Function for all titles
def getSongTitles(keyword, artist="", playlist=""):
    return fetchResults("SELECT 'songs', a.*, b.artist_name FROM songs a, artists b WHERE a.artist_id = b.artist_id AND song_title LIKE '%{}%'{}{}".format(
        keyword,
        " AND a.artist_id = {}".format(artist) if artist != "" else "",
        " AND a.song_id IN (SELECT song_id FROM playlist_videos WHERE playlist_id = {})".format(playlist) if playlist != "" else ""
        ))

# Function for all playlists
def getPlaylists(keyword):
    return fetchResults("SELECT 'playlists', * FROM playlists WHERE playlist_name LIKE '%{}%'".format(
        keyword
        ))

# Function for all favourited songs
def getFavouriteSongs(keyword):
    return fetchResults("SELECT 'songs', a.*, b.artist_name FROM songs a, artists b WHERE a.favourited = 1 AND a.artist_id = b.artist_id AND a.song_title LIKE '%{}%'".format(
        keyword
        ))

# Function for all favourited artiosts
def getFavouriteArtists(keyword):
    return fetchResults("SELECT 'artists', * FROM artists WHERE favourited = 1 AND artist_name LIKE '%{}%'".format(
        keyword
        ))

# Function for toggling favourite song
def setFavouriteSong(song_id):
    execute("UPDATE songs SET favourited = 1 - favourited WHERE song_id = {}".format(song_id))

# Function for toggling favourite artist
def setFavouriteArtist(artist_id):
    execute("UPDATE artists SET favourited = 1 - favourited WHERE artist_id = {}".format(artist_id))

# Function for adding playlists
def newPlaylist(name):
    execute("INSERT INTO playlists (playlist_name) VALUES (\"{}\")".format(name))
    return checkPlaylist(name)

# Function for checking if a playlist of the same name exists
def checkPlaylist(playlist_name):
    return fetchResults("SELECT 'playlists', playlist_id FROM playlists WHERE playlist_name = '{}'".format(playlist_name))

# Function to remove playlist
def removePlaylist(playlist_id):
    execute("DELETE FROM playlists WHERE playlist_id={}".format(playlist_id))

# Function for adding songs to existing playlists
def addPlaylistSong(playlist, song):
    execute("INSERT INTO playlist_videos (playlist_id, song_id) VALUES ({}, {})".format(playlist, song))
