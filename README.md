mvid_dl
=======

Music video downloader for XBMC

Loads artist and track titles from various sources then uses http://theaudiodb.com to retrieve music video urls to pass to [youtube-dl](https://github.com/rg3/youtube-dl) which saves them in appropriately named video files for XBMC's [Music Video Scraper](http://wiki.xbmc.org/index.php?title=Add-on:TheAudioDb.com_for_Music_Videos).

## Sources
- [Australian Top 50 singles chart](http://ariacharts.com.au/chart/singles)
- [last.fm played tracks](http://last.fm)

## Planned features
- [ ] flexible configuration of other song chart sources
- [ ] command line switches to accept artist and/or song titles on command line or standard input
- [ ] (eventually) download all songs in XBMC's music collection

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

__NOTE__ - this project uses an alternative version of _pylast_ than the default installed by `pip` as the original project has not been updated for several years. If you have the original pylast installed, you will need to uninstall it first.

## Settings
Enable the desired sources in `settings.ini`.

If using the _last.fm played tracks_ feature, you will also need to enter your last.fm username and generate your own [API keys](http://www.last.fm/api/account/create)

## Usage
Currently, it only outputs the url and file name which needs to be passed as follows:
```
$ ./mvid_dl.py | while read url name; do youtube-dl --recode-video mp4 --output "${name}.mp4" --continue -f best "${url}"; done
```
