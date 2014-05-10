#!/usr/bin/env python
#
#
#   Author: Wade Fitzpatrick    wade.fitzpatrick@gmail.com
#

import json
import re
import requests

class MusicVideo:
    """A class of music video objects to be downloaded"""

    # FIXME Change this to a valid api key
    apikey = 1

    def __init__(self, artist, title):
 
        self.full_artist = artist
 
        artist = re.sub(r' Feat\..*', r'', artist, flags=2)
        artist = re.sub(r' Vs.*', r'', artist, flags=2)
        artist = re.sub(r' &.*', r'', artist, flags=2)
        artist = re.sub(r'\|.*', r'', artist)
        self.artist = artist.rstrip().encode('utf8')
 
        self.title = title.encode('utf8')

    def __str__(self):
        return '{} - {}'.format(self.artist, self.title)

    def prepare_artist(self):
        """Search for artist in theaudiodb.com and get MusicBrainz ID"""

        payload = {'s': self.artist}
        r = requests.get('http://www.theaudiodb.com/api/v1/json/{0}/search.php'.format(MusicVideo.apikey), params=payload)
 
        data = json.loads(r.text)
 
        if data['artists'] is None:
            raise LookupError, "artist='{0}' not found in theaudiodb.com".format(self.artist)

        assert (len(data['artists']) == 1), "expected one result for artist='{0}'".format(self.artist)
        assert (data['artists'][0]['strMusicBrainzID']), "no MusicBrainzID for artist='{0}'".format(self.artist)

        self.mbid = data['artists'][0]['strMusicBrainzID']
 
    def prepare_title(self):
        """Search for title in theaudiodb.com and get the music video url"""

        # request all music videos for this artist
        payload = {'i': self.mbid}
        r = requests.get('http://www.theaudiodb.com/api/v1/json/{0}/mvid-mb.php'.format(MusicVideo.apikey), params=payload)
 
        vids = json.loads(r.text)
 
        if vids['mvids'] is None:
            raise LookupError, "no music videos available for artist='{0}'".format(self.artist)

        self.url = None
        for v in vids['mvids']:
            if self.title.lower() in v['strTrack'].lower():
                self.url = v['strMusicVid']

        if self.url is None:
            raise LookupError, "music video not found for artist='{0}' and title='{1}'".format(self.artist, self.title)
