from baseclasses.scrolltext import ScrollText

import requests

from opc.colors import rgb


class Art(ScrollText):

    description = "Get the news headlines"

    fg = (192, 192, 255)
    bg = rgb["firebrick"]

    def _fetchHeadlines(self):
        key = self.config["GUARDIAN_APIKEY"]
        reply = requests.get("http://content.guardianapis.com/search?section=news&limit=20&api-key="+key)
        if reply.status_code == 200:
            results = reply.json()["response"]["results"]
            return [result["webTitle"] for result in results]
        else:
            return ["No news is good news"]

    def _getText(self):
        try:
            return " +++ " + self.headlines.pop()
        except IndexError:
            self.headlines = self._fetchHeadlines()
            return " +++ " + self.headlines.pop()

    def _initText(self):
        self.headlines = ["News from The Guardian"]
