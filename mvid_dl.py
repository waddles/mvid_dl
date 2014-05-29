#!/usr/bin/env python
#
#
#   Author: Wade Fitzpatrick    wade.fitzpatrick@gmail.com
#
# Download ARIA top 50 singles music videos
#
# Output music video url and "Artist - Song Title"
#
# Eg. $ ./mvid_dl.py | while read url name; do youtube-dl --recode-video mp4 --output "${name}.mp4" --continue -f best "$url"; done

from __future__ import print_function
import ConfigParser
import pylast
import requests
import sys
import time
from lxml import html
from musicvid import MusicVideo

Config = ConfigParser.ConfigParser()
Config.read('settings.ini')

def ARIA_top_50():
    if Config.getboolean('ARIA top 50 singles', 'enabled'):
        page = requests.get('http://ariacharts.com.au/chart/singles')
        tree = html.fromstring(page.text)
        songs = tree.xpath('//div[@class="column col-6"]/h3/text()')
        artists = tree.xpath('//div[@class="column col-6"]/p[1]/text()[1]')

        assert(len(songs) == len(artists))
    return zip(artists, songs)

def LastFM_played_tracks():
    last_tracks = []
    if Config.getboolean('ARIA top 50 singles', 'enabled'):
        network = pylast.LastFMNetwork(api_key=Config.get('LastFM', 'API_KEY'),
                api_secret=Config.get('LastFM', 'API_SECRET'))
        recent_tracks = network.get_user(Config.get('LastFM', 'username')).get_recent_tracks(limit=None)
        for played_track in recent_tracks:
            last_tracks.append([played_track.track.artist.name, played_track.track.title])
    return last_tracks

for (artist, title) in ARIA_top_50() + LastFM_played_tracks():
    mvid = MusicVideo(artist, title)
    try:
        mvid.prepare_artist()
        time.sleep(1)
        mvid.prepare_title()
    except LookupError,e:
        print(e, file=sys.stderr)
        continue

    print("{0} {1}".format(mvid.url, mvid))
