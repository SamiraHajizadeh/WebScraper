import scrapy
from pathlib import Path
import yaml
from tutorials.items import CoinItem
import w3lib.html

def get_config(config):
  with open(config, 'r') as stream:
    return yaml.load(stream)

class QuoteSpider(scrapy.Spider):

  name = 'RPC_V4'
  start_urls = ['https://rpc.ashmus.ox.ac.uk/search/browse?volume_id=4']

  def parse(self, response):

    item = CoinItem()
    if response.status == 200:
      img = response.xpath("//img/@src")
      item['image_urls'] = self.url_join(img.extract(), response)
      data = response.xpath('translate(normalize-space(//div[@class="fieldrow"]/text()), " ", "")')
      item['volume'] = data
        #"//label[@for='volume']" )  #'//div[@class="label"][contains(text(), "Volume")]') #/following-sibling::div[@class="label"]//text()').get(default='')

    return item



#//span[@class='item-label' and .='Colored Mug:']/following-sibling::text()[1]



  def url_join(self, rel_img_urls, response):
    joined_urls = []
    for rel_img_url in rel_img_urls:
      joined_urls.append(response.urljoin(rel_img_url))

    return joined_urls


