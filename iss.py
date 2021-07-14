"""Facts about ISS, next flyover, etc"""
import urllib.request
import json
import datetime
from errbot import BotPlugin, botcmd, arg_botcmd, re_botcmd


class Iss(BotPlugin):
    """Facts about ISS"""

    @botcmd
    def iss(self, msg, args):
        """Return next flyover"""
        return self.iss_send(msg, flyover=True)

    @botcmd
    def iss_random(self, msg, args):
        """Random ISS Fact"""
        return self.iss_send(msg, random=True)

    def iss_send(self, msg, random=False, flyover=False):
        """Lookup fact about ISS and return it"""
        # api.open-notify.org/iss/v1/?lat=39.7392&lon=-104.9903&alt=1650&n=1
        lat = '39.7392'
        lon = '-104.9903'
        url = 'http://api.open-notify.org/iss/v1/?lat='+lat+'&lon='+lon
        page = urllib.request.Request(url)
        response = json.loads(urllib.request.urlopen(page).read().decode('utf-8'))
        if 'response' in response:
            if 'risetime' in response['request']:
                time = response['response']['risetime']
                return datetime.datetime.fromtimestamp(time)
        return 'No timestamp in response: '+str(response)
