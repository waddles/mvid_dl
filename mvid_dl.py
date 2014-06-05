#!/usr/bin/env python
# This file is part of the music video downloader project at
# https://github.com/waddles/mvid_dl
#
# Download music videos using artist and track titles from various sources
#
# Output music video url and "Artist - Song Title"
#
# Eg. $ ./mvid_dl.py | while read url name; do youtube-dl --recode-video mp4 --output "${name}.mp4" --continue -f best "$url"; done

from __future__ import print_function
import ConfigParser
import argparse
import pylast
import requests
import sys
import time
from lxml import html
from musicvid import MusicVideo

__version__ = '0.2.0'
__author__ = 'Wade Fitzpatrick'
__copyright__ = 'Copyright (C) 2014 Wade Fitzpatrick'
__license__ = 'MIT'
__email__ = 'wade.fitzpatrick@gmail.com'

parser = argparse.ArgumentParser(description='fetch music videos for XBMC')
group1 = parser.add_mutually_exclusive_group()
group1.add_argument('-v', '--verbose', action='store_true')
group1.add_argument('-q', '--quiet', action='store_true')
group2 = parser.add_argument_group()
group2.add_argument('-a', '--artist', help='artist name')
group2.add_argument('-t', '--title', help='track title')
args = parser.parse_args()
if args.title and not args.artist:
    parser.error('track title without artist name')

Config = ConfigParser.ConfigParser()
Config.read('settings.ini')

def ARIA_top_50():
    if Config.getboolean('ARIA top 50 singles', 'enabled'):
        page = requests.get('http://ariacharts.com.au/chart/singles')
        tree = html.fromstring(page.text)
        songs = tree.xpath('//div[@class="column col-6"]/h3/text()')
        artists = tree.xpath('//div[@class="column col-6"]/p[1]/text()[1]')

        assert(len(songs) == len(artists))
        return [MusicVideo(artist, title) for artist,title in zip(artists, songs)]

def LastFM_played_tracks():
    if Config.getboolean('LastFM', 'enabled'):
        try:
            limit = Config.getint('LastFM', 'limit')
            if limit <= 0:
                limit = None
        except ConfigParser.NoOptionError, e:
            print('{}... using limit=None'.format(e), file=sys.stderr)
            limit = None
        network = pylast.LastFMNetwork(api_key=Config.get('LastFM', 'API_KEY'),
                api_secret=Config.get('LastFM', 'API_SECRET'))
        recent_tracks = network.get_user(Config.get('LastFM', 'username')).get_recent_tracks(limit=limit)
        return [MusicVideo(t.track.artist.name, t.track.title) for t in recent_tracks]

to_fetch = set()
if args.title and args.artist:
    to_fetch.update([MusicVideo(args.artist, args.title)])
else:
    to_fetch.update(ARIA_top_50())
    to_fetch.update(LastFM_played_tracks())

for mvid in to_fetch:
    try:
        mvid.prepare_artist()
        time.sleep(1)
        mvid.prepare_title()
    except LookupError,e:
        print(e, file=sys.stderr)
        continue

    print("{0} {1}".format(mvid.url, mvid))
