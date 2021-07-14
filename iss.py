"""Facts about ISS, next flyover, etc"""
import urllib.request
import json
import datetime
import pytz
from errbot import BotPlugin, botcmd, arg_botcmd, re_botcmd


class Iss(BotPlugin):
    """Facts about ISS"""

    @arg_botcmd('--latitude', dest='latitude', type=str, default='39.7392')
    @arg_botcmd('--longitude', dest='longitude', type=str, default='-104.9903')
    def iss(self, msg, latitude, longitude):
        """Return next flyover"""
        return self.iss_send(msg, latitude, longitude)

    def iss_send(self, msg, latitude, longitude):
        """Lookup fact about ISS and return it"""
        # api.open-notify.org/iss/v1/?lat=39.7392&lon=-104.9903&alt=1650&n=1
        url = 'http://api.open-notify.org/iss/v1/?lat='+latitude+'&lon='+longitude
        page = urllib.request.Request(url)
        response = json.loads(urllib.request.urlopen(page).read().decode('utf-8'))
        risetime = ''
        if 'response' in response:
            for item in response['response']:
                if 'risetime' in item:
                    time = item['risetime']
                    risetime = (risetime + str(datetime.datetime.fromtimestamp(
                                    time, tz=pytz.timezone('America/Denver'))) + '\n' +
                                ' for ' + str(item['duration']) + '\n')
            return risetime
        return 'No timestamp in response: '+str(response)
