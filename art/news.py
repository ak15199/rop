from baseclasses.scrolltext import ScrollText

import requests

from opc.colors import rgb, WHITE

URL = "http://content.guardianapis.com/search?section=news&limit=20&api-key="


class Art(ScrollText):

    description = "Get the news headlines"

    fg = WHITE
    bg = rgb["firebrick"]

    def _fetchHeadlines(self):
        url = URL+self.config["GUARDIAN_APIKEY"]
        try:
            reply = requests.get(url)
            if reply.status_code == 200:
                results = reply.json()["response"]["results"]
                return [result["webTitle"] for result in results]
        except Exception:  # XXX: Have to catch everything?
            pass

        return ["No news is good news"]

    def _getText(self):
        try:
            return " +++ " + self.headlines.pop()
        except IndexError:
            self.headlines = self._fetchHeadlines()
            return " +++ " + self.headlines.pop()

    def _initText(self):
        self.headlines = ["News from The Guardian"]
