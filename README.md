# KTVHome

## What is this?
When working on constructing the home network for my parents new home build, I made an effort to upgrade their Karaoke PC. After a brief look, I have discovered that the Karaoke software used is a propietary one, which doesn't allow user-submitted songs. Because of that, I wanted to create a new Karaoke software for my parents to use that's customizable to our needs. KTVHome is a result of that.

## How do I use this?
You need exactly the same set-up as I do because I have tailored the software to my needs. Those needs being:
* Chinese and English UI at the same time
* Able to create own song collection
* Software GUI on one screen, media player on the other
* Being able to be controlled by touchscreen
I am reusing a capacitive touchscreen (1366*768) from their previous karaoke setup.
However, I do plan on making the software more flexible for all screens in the future.

## Features
* Ability to search for
    * songs
    * artists
* ...with
    * search keyword terms
    * specific language
    * specific artist
* Make and edit playlists
* Favourite artists/songs
* TBC

## Requirements (for source code)
* <a href="https://pypi.org/project/PySide6/">PySide6</a>
* <a href="https://pypi.org/project/python-vlc/">python-vlc</a>
* <a href="https://www.python.org/downloads/">Python 3</a>
* <a href="https://www.microsoft.com/en-au/software-download/windows10">Windows 10</a>
Windows 10 is required for Tablet mode + on-screen keyboard

## Screenshots
![Home Screen](screenshots\\home-page.jpg)
![Grid Search](screenshots\\grid-search.jpg)
![List Search](screenshots\\list-search.jpg)
![Queue](screenshots\\queue.jpg)

## Future ToDos (order by priority):
- [ ] Config File
- [ ] Proper Resize
- [ ] Proper commenting of labelled files
- [ ] Statistics Window
- [ ] Themes

Note this software does **NOT** allow you to download karaoke songs. Nor do I support such acts.

## Resource Attributions
Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
These were edited with a fill-color from black to white.