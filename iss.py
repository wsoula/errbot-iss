"""Facts about ISS, next flyover, etc"""
import urllib.request
import json
import datetime
import pytz
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
        risetime = ''
        if 'response' in response:
            for item in response['response']:
                if 'risetime' in item:
                    time = item['risetime']
                    risetime = risetime + datetime.datetime.fromtimestamp(time, tz=pytz.timezone('America/Denver')) + ' '
            return risetime
        return 'No timestamp in response: '+str(response)
