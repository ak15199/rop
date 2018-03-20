from .baseclasses.scrolltext import ScrollText

from datetime import date
import requests


API_ENDPOINT = 'http://content.guardianapis.com/search'


class Art(ScrollText):

    description = "Get the news headlines"

    fg = (224, 224, 224)
    bg = (174, 0, 0)

    def _fetchHeadlines(self):
        today = date.today().strftime('%Y-%m-%d')
        params = {
            'from-date': today,
            'to-date': today,
            'order-by': "newest",
            'show-fields': 'all',
            'page-size': 200,
            'api-key': self.config["GUARDIAN_APIKEY"]
        }
        headlines = []

        current_page = 1
        total_pages = 1
        
        while current_page <= total_pages:
            params['page'] = current_page
            response = requests.get(API_ENDPOINT, params=params)
            if response.status_code == 200:
                data = response.json()
                headlines.extend(data['response']['results'])
                current_page += 1
                total_pages = data['response']['pages']
            else:
                return ["No news is good news"]

        return ["%s) %s"%(headline["sectionName"], headline["webTitle"])
                for headline in headlines
                if headline["sectionName"] != "Crosswords"
                ]

    def _getText(self):
        try:
            return " +++ " + self.headlines.pop()
        except IndexError:
            self.headlines = self._fetchHeadlines()
            return " +++ " + self.headlines.pop()

    def _initText(self):
        self.headlines = ["News from The Guardian"]







