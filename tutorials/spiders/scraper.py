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

      item["volume"] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='volume' and .='Volume:']/following-sibling::text()[1]").extract()]
      item["no"] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='volume' and .='№:']/following-sibling::a[1]/text()").extract()]
      item['reign'] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='reign' and .='Reign:']/following-sibling::a[1]/text()").extract()]
      item['persons'] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='persons' and .='Persons:']/following-sibling::a[1]/text()").extract()]
      item['city'] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='city' and .='City:']/following-sibling::a[1]/text()").extract()]
      item['region'] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='region' and .='Region:']/following-sibling::a[1]/text()").extract()]
      item['province'] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='province' and .='Province:']/following-sibling::a[1]/text()").extract()]
      item['denomination'] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='denomination' and .='Denomination:']/following-sibling::text()[1]").extract()]
      item['average_weight'] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='average_weight' and .='Average weight:']/following-sibling::text()[1]").extract()]

      obverse_part1 = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='obverse' and .='Obverse:']/following-sibling::span[@class='inscription']/text()").extract()]
      obverse_part2 = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='obverse' and .='Obverse:']/following-sibling::span[@class='inscription']/following-sibling::text()[1]").extract()]
      item['obverse'] = [obverse_part1[i]+obverse_part2[i] for i in range(max([len(obverse_part1), len(obverse_part2)]))]

      reverse_part1 = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='reverse' and .='Reverse:']/following-sibling::span[@class='inscription']/text()").extract()]
      reverse_part2 = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='reverse' and .='Reverse:']/following-sibling::span[@class='inscription']/following-sibling::text()[1]").extract()]
      item['reverse'] = [reverse_part1[i]+reverse_part2[i] for i in range(max([len(reverse_part1), len(reverse_part2)]))]

      item['specimens'] = [ele.strip("\t\n\xa0 ") for ele in response.xpath("//label[@for='specimens' and .='Specimens:']/following-sibling::text()[1]").extract()]

    return item


  def url_join(self, rel_img_urls, response):
    joined_urls = []
    for rel_img_url in rel_img_urls:
      joined_urls.append(response.urljoin(rel_img_url))

    return joined_urls


