import scrapy
from pathlib import Path
import yaml

def get_config(config):
  with open(config, 'r') as stream:
    return yaml.load(stream)

class QuoteSpider(scrapy.Spider):

  #def __init__(self):
  name = 'RPC_V1' #get_config('config.yaml')['scraper_name']
  start_urls = ['https://rpc.ashmus.ox.ac.uk/search/browse?volume_id=4'] # get_config('config.yaml')['start_urls']

  def start_requests(self):
    for url in self.start_urls:
      yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    page = response.url.split("/")[-2]
    filename = f'quotes-{page}.html'
    Path(filename).write_bytes(response.body)
    self.log(f'Saved file {filename}')