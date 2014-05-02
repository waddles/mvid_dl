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
import json, requests, sys, time

for line in sys.stdin:
    line = line.rstrip()

    payload = {'s': line}
    r = requests.get('http://www.theaudiodb.com/api/v1/json/1/search.php', params=payload)
    
    data = json.loads(r.text)
    
    if data['artists'] is None:
        continue

    for a in data['artists']:
        artist = a['strArtist'].encode('utf8')
        # Katy Perry
 
        mbid = a['strMusicBrainzID']
        # 122d63fc-8671-43e4-9752-34e846d62a9c
 
        print("{0} {1}".format(artist, mbid), file=sys.stderr)
        # Katy Perry 122d63fc-8671-43e4-9752-34e846d62a9c
 
        time.sleep(2)
        r = requests.get('http://www.theaudiodb.com/api/v1/json/1/mvid-mb.php?i={0}'.format(mbid))
 
        vids = json.loads(r.text)
 
        if vids['mvids'] is None:
            continue

        for v in vids['mvids']:
            print("{0} {1} - {2}".format(v['strMusicVid'], artist, v['strTrack'].encode('utf8')))
