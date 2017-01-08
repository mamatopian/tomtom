from lxml import html
import re
import requests
from datetime import timedelta, datetime, date


class NrsrSpider:
    name = 'NRSRspider'
    from_date = date(2016, 3, 23)
    to_date = date(2016, 3, 27)
    period = '7'
    increment = timedelta(days=1)
    selector_class = '.alpha.omega'
    url = "https://www.nrsr.sk/web/Default.aspx?sid=schodze/rozprava/vyhladavanie&CisObdobia={}&CPT=&CisSchodze=0&PoslanecID=929&DatumOd={}%200:0:0&DatumDo={}%200:0:0&TypVystupenia="
    data = []
    output = 'tomtom.txt'
    pattern = re.compile("[^\w\p{L}(\w/.) ]")
    pattern2 = re.compile("(\d+.)")

    start_url = url.format(period, from_date.isoformat(), to_date.isoformat())

    def start_requests(self):
        print("Starting with {}".format(self.start_url))
        self.get(self.start_url)

    def get(self, address):
        page = requests.get(address)
        tree = html.fromstring(page.content)
        print("{} downloaded, ready to parse".format(address))
        self.parse(tree)

    def parse(self, htmldata):
        tomtom = htmldata.xpath("//div[contains(@class, 'alpha') and contains(@class, 'omega')]/span/text()")
        for tom in tomtom:
            tom = self.pattern.sub('', tom)
            tom = self.pattern2.sub('', tom)
            print(tom)
            self.data.append(tom)
            with open(self.output, "a") as output:
                output.write(tom)

        print("{} useful speeches added, going to get another ones".format(len(tomtom)))
        self.next()

    def next(self):
        self.from_date = self.to_date + timedelta(days=1)
        self.to_date = self.from_date + self.increment

        if self.from_date < date.today():
            self.get(self.url.format(self.period, self.from_date, self.to_date))
