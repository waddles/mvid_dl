#!/usr/bin/env python
#
#
#   Author: Wade Fitzpatrick    wade.fitzpatrick@gmail.com
#
# Accept artist names on stdin
# Output music video url and "Artist - Song Title"
#
# Eg. $ echo Jessica Mauboy | ~/projects/mvid_dl/mvid_dl.py | while read url name; do youtube-dl --recode-video mp4 --output "${name}.mp4" --continue -f best "$url"; done

from __future__ import print_function
import json, re, requests, sys, time
from lxml import html

# FIXME Change this to a valid api key
apikey = 1

page = requests.get('http://ariacharts.com.au/chart/singles')
tree = html.fromstring(page.text)
songs = tree.xpath('//div[@class="column col-6"]/h3/text()')
artists = tree.xpath('//div[@class="column col-6"]/p[1]/text()[1]')

#for line in sys.stdin:
#    line = line.rstrip()
#    payload = {'s': line}
for (artist,title) in zip(artists,songs):
    artist = re.sub(r' Feat\..*', r'', artist, flags=2)
    artist = re.sub(r' Vs.*', r'', artist, flags=2)
    artist = re.sub(r' &.*', r'', artist, flags=2)
    artist = re.sub(r'\|.*', r'', artist)
    artist = artist.rstrip()

    payload = {'s': artist}
    r = requests.get('http://www.theaudiodb.com/api/v1/json/{0}/search.php'.format(apikey), params=payload)
    
    data = json.loads(r.text)
    
    if data['artists'] is None:
        print("'{0}' - artist not found in theaudiodb.com".format(artist), file=sys.stderr)
        continue

    for a in data['artists']:
        found = False

        artist = a['strArtist'].encode('utf8')
        # Katy Perry
 
        mbid = a['strMusicBrainzID']
        # 122d63fc-8671-43e4-9752-34e846d62a9c
 
        time.sleep(2)
        # request all music videos for this artist
        r = requests.get('http://www.theaudiodb.com/api/v1/json/{0}/mvid-mb.php?i={1}'.format(apikey,mbid))
 
        vids = json.loads(r.text)
 
        if vids['mvids'] is None:
            continue

        for v in vids['mvids']:
            if title.lower() in v['strTrack'].lower():
                print("{0} {1} - {2}".format(v['strMusicVid'], artist, v['strTrack'].encode('utf8')))
                found = True

        if found is False:
            print("'{0} - {1}' - music video not found in theaudiodb.com".format(artist, title), file=sys.stderr)
