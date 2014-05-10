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
import requests
import sys
import time
from lxml import html
from musicvid import MusicVideo

page = requests.get('http://ariacharts.com.au/chart/singles')
tree = html.fromstring(page.text)
songs = tree.xpath('//div[@class="column col-6"]/h3/text()')
artists = tree.xpath('//div[@class="column col-6"]/p[1]/text()[1]')

for (artist, title) in zip(artists, songs):
    mvid = MusicVideo(artist, title)
    try:
        mvid.prepare_artist()
        time.sleep(2)
        mvid.prepare_title()
    except LookupError,e:
        print(e, file=sys.stderr)
        continue

    print("{0} {1}".format(mvid.url, mvid))
