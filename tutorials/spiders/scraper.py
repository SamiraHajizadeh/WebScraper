import scrapy
from pathlib import Path
import yaml
from tutorials.items import CoinItem

def get_config(config):
  with open(config, 'r') as stream:
    return yaml.load(stream)

class QuoteSpider(scrapy.Spider):

  #def __init__(self):
  name = 'RPC_V4' #get_config('config.yaml')['scraper_name']
  start_urls = ['https://rpc.ashmus.ox.ac.uk/search/browse?volume_id=4'] # get_config('config.yaml')['start_urls']

#  def start_requests(self):
#    for url in self.start_urls:
#      yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):

    item = CoinItem()
    if response.status == 200:
      img = response.xpath("//img/@src")
      item['title'] = response.css(".content-main-aside h1::text").extract()
      item['volume'] = 
      item['image_urls'] = self.url_join(img.extract(), response) 
       
    return item

type1 = response.xpath('//div[@class="fieldrow"][contains(text(), "Reign")]/following-sibling::div[@class="carac-value"]//text()').get(default='')

    #rel_img_urls = response.xpath("//img/@src").extract()
		year = response.css(".content-main-aside h1 time a::text").extract_first()
		month = response.css(".content-main-aside h1 time::text").extract_first()[:-2]
		# parse the date
		date = "{} {}".format(month, year).replace(".", "")
		d = datetime.datetime.strptime(date, "%b %d %Y")
		pub = "{}-{}-{}".format(d.year, str(d.month).zfill(2), str(d.day).zfill(2))
		# yield the result
		yield MagazineCover(title=title, pubDate=pub, file_urls=[imageURL])


//span[@class='item-label' and .='Colored Mug:']/following-sibling::text()[1]


<label for="volume">


											<div class="fieldrow"><label for="reign">Reign:</label> <a href="/search/browse?reign_id=60">Marcus Aurelius</a>

																							<label for="persons">Persons:</label>
																							  		<a href="/search/browse?obverse_person_id[]=147">Marcus Aurelius (Augustus)</a>	


  def url_join(self, rel_img_urls, response):
    joined_urls = []
    for rel_img_url in rel_img_urls:
      joined_urls.append(response.urljoin(rel_img_url))

    return joined_urls


