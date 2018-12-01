from io import BytesIO
from PIL import Image
import scrapy
import os


# API key for Google Maps.
KEY = 'AIzaSyBcm6xXVf2H88_FExXWjn2HN8k9YOnSMJk'
ZOOM = 16
SIZE = 640


class satellite(scrapy.Spider):
    name = 'satellite'

    def start_requests(self):
        # Read map points.
        with open('geo_points.dat') as f:
            points = [_.split(',') for _ in f.read().split('\n') if _]

        # See if the directory exists.
        if not os.path.isdir('crawled'): os.mkdir('crawled')

        # Construct URLs.
        urls = [{
            'url': 'http://maps.googleapis.com/maps/api/staticmap?sensor=false'\
                   + '&size=' + str(SIZE) + 'x' + str(SIZE) + '&center='
                   + str(point[0]) + ',' + str(point[1]) + '&zoom=' + str(ZOOM)\
                   + '&maptype=satellite' + '&key=' + KEY,
            'pos': {
                    'lat': point[0],
                    'lon': point[1]
                }
            } for point in points
        ]

        # Construct requests.
        for url in urls:
            yield scrapy.Request(url=url.get('url'), callback=self.parse,
                                 meta=url.get('pos'))

    def parse(self, response):
        meta = response.meta
        image = Image.open(BytesIO(response.body))
        image.save('crawled/%s_%s.png' % (meta.get('lat'), meta.get('lon')),
                   'PNG')
