import scrapy
from pathlib import Path
import yaml
from CoinScraper.items import CoinItem
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

def get_config(config):
  with open(config, 'r') as stream:
    return yaml.load(stream)


def concat_lists(lst1, lst2):
  max_size = min([len(lst1), len(lst2)])
  lst1.extend([""] * (max_size - len(lst1)))
  lst2.extend([""] * (max_size - len(lst2)))
  return [lst1[i]+lst2[i] for i in range(max_size)]


def get_data(response, xpath_addresses, item, data_names):
  temp = {}
  for i in range(len(data_names)):
    temp[data_names[i]] = [ele.strip("\t\n\xa0 ") for ele in response.xpath(xpath_addresses[i]).extract()]
  return temp


class CoinSpider(CrawlSpider):

  name = 'RPC_V4'
  start_urls = ['https://rpc.ashmus.ox.ac.uk/search/browse?volume_id=4']
  rules = (Rule(LinkExtractor(allow=('//nav/ul/li[15]/a/@href',)), callback="parse_item", follow=True),)

  def parse_start_url(self, response):
    return self.parse_item(response)

  def parse_item(self, response):

    item = CoinItem()
    if response.status == 200:

      images_links = [self.url_join(u, response) for u in response.xpath("//img/@src").extract()]
      
      addresses = ["//label[@for='volume' and .='Volume:']/following-sibling::text()[1]",
                  "//label[@for='volume' and .='№:']/following-sibling::a[1]/text()",
                  "//label[@for='reign' and .='Reign:']/following-sibling::a[1]/text()", 
                  "//label[@for='persons' and .='Persons:']/following-sibling::a[1]/text()",
                  "//label[@for='city' and .='City:']/following-sibling::a[1]/text()",
                  "//label[@for='region' and .='Region:']/following-sibling::a[1]/text()",
                  "//label[@for='province' and .='Province:']/following-sibling::a[1]/text()",
                  "//label[@for='denomination' and .='Denomination:']/following-sibling::text()[1]",
                  "//label[@for='average_weight' and .='Average weight:']/following-sibling::text()[1]",
                  "//label[@for='specimens' and .='Specimens:']/following-sibling::text()[1]",
                  "//label[@for='obverse' and .='Obverse:']/following-sibling::span[@class='inscription']/text()",
                  "//label[@for='obverse' and .='Obverse:']/following-sibling::span[@class='inscription']/following-sibling::text()[1]",
                  "//label[@for='reverse' and .='Reverse:']/following-sibling::span[@class='inscription']/text()",
                  "//label[@for='reverse' and .='Reverse:']/following-sibling::span[@class='inscription']/following-sibling::text()[1]"
                  ]

      names = ["volume", "no", "reign", "persons", "city", "region", "province", "denomination", "average_weight", "specimens", "obverse1", "obverse2", "reverse1", "reverse2"]


      data = get_data(response, addresses, item, names)
      data["obverse"] = concat_lists(data["obverse1"], data["obverse2"])
      data["reverse"] = concat_lists(data["reverse1"], data["reverse2"])
      names = ["volume", "no", "reign", "persons", "city", "region", "province", "denomination", "average_weight", "specimens", "obverse", "reverse"]


      for i in range(20):
        item['image_urls'] = images_links[i]

        for name in names:
          if len(data[name]) > i:
            item[name] = data[name][i]

        yield item 

    next_url = response.xpath('//nav/ul/li[15]/a/@href').extract()

    if len(next_url):
      yield Request(next_url[0], callback=self.parse_item, meta={'item': item})


  def url_join(self, rel_img_urls, response):
    joined_urls = []
    for rel_img_url in rel_img_urls:
      joined_urls.append(response.urljoin(rel_img_url))

    return joined_urls
  
