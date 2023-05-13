import scrapy
from pathlib import Path
import yaml
from tutorials.items import CoinItem
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


class CoinSpider(CrawlSpider):

  name = 'RPC_V4'
  start_urls = ['https://rpc.ashmus.ox.ac.uk/search/browse?volume_id=4']
  rules = (Rule(LinkExtractor(allow=('//nav/ul/li[15]/a/@href',)), callback="parse_item", follow=True),)

  def parse_start_url(self, response):
    return self.parse_item(response)

  def parse_item(self, response):

    item = CoinItem()
    if response.status == 200:

      img = response.xpath("//img/@src")

      item['image_urls'] = self.url_join(img.extract(), response)

      item["volume"] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='volume' and .='Volume:']/following-sibling::text()[1]").extract()]
      item["no"] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='volume' and .='№:']/following-sibling::a[1]/text()").extract()]
      item['reign'] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='reign' and .='Reign:']/following-sibling::a[1]/text()").extract()]
      item['persons'] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='persons' and .='Persons:']/following-sibling::a[1]/text()").extract()]
      item['city'] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='city' and .='City:']/following-sibling::a[1]/text()").extract()]
      item['region'] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='region' and .='Region:']/following-sibling::a[1]/text()").extract()]
      item['province'] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='province' and .='Province:']/following-sibling::a[1]/text()").extract()]
      item['denomination'] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='denomination' and .='Denomination:']/following-sibling::text()[1]").extract()]
      item['average_weight'] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='average_weight' and .='Average weight:']/following-sibling::text()[1]").extract()]
      item['specimens'] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='specimens' and .='Specimens:']/following-sibling::text()[1]").extract()]

      obverse_part1 = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='obverse' and .='Obverse:']/following-sibling::span[@class='inscription']/text()").extract()]
      obverse_part2 = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='obverse' and .='Obverse:']/following-sibling::span[@class='inscription']/following-sibling::text()[1]").extract()]
      item['obverse'] = concat_lists(obverse_part1, obverse_part2)

      reverse_part1 = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='reverse' and .='Reverse:']/following-sibling::span[@class='inscription']/text()").extract()]
      reverse_part2 = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='reverse' and .='Reverse:']/following-sibling::span[@class='inscription']/following-sibling::text()[1]").extract()]
      item['reverse'] = concat_lists(reverse_part1, reverse_part2)

    next_url = response.xpath('//nav/ul/li[15]/a/@href').extract()

    if len(next_url):
      yield Request(next_url[0], callback=self.parse_item, meta={'item': item})

    yield item


  def url_join(self, rel_img_urls, response):
    joined_urls = []
    for rel_img_url in rel_img_urls:
      joined_urls.append(response.urljoin(rel_img_url))

    return joined_urls
  
