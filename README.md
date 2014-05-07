mvid_dl
=======

Music video downloader for XBMC

Scrapes the [Australian Top 50 singles chart](http://ariacharts.com.au/chart/singles) for songs then uses http://theaudiodb.com to retrieve music video urls to pass to [youtube-dl](https://github.com/rg3/youtube-dl) which saves them in appropriately named video files for XBMC's [Music Video Scraper](http://wiki.xbmc.org/index.php?title=Add-on:TheAudioDb.com_for_Music_Videos).

## Planned features:
- flexible configuration of other song chart sources
- command line switches to accept artist and/or song titles on command line or standard input

## Installation
- Install youtube-dl according to that project's instructions or your distro's instructions.
- Clone the repo from github
```
$ git clone https://github.com/waddles/mvid_dl mvid_dl
```
- Optionally create a [virtualenv](https://pypi.python.org/pypi/virtualenv)
```
$ virtualenv --python=python2.7 --verbose mvid_dl
$ cd mvid_dl
$ . bin/activate
```
- Install required python (2.7) packages
```
$ pip install -r requires.txt 
```

## Usage
Currently, it only outputs the url and file name which needs to be passed as follows:
```
$ ./mvid_dl.py | while read url name; do youtube-dl --recode-video mp4 --output "${name}.mp4" --continue -f best "${url}"; done
```
