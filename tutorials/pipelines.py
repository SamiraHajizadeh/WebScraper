# Define your item pipelines here
# useful for handling different item types with a single interface


from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from pathlib import PurePosixPath
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline


class CoinPipeline:
  def process_item(self, item, spider):
    adapter = ItemAdapter(item)
        
    if adapter.get('price'):
      if adapter.get('price_excludes_vat'):
        adapter['price'] = adapter['price'] * self.vat_factor
      return item
    else:
      raise DropItem(f"Missing price in {item}")


class MyImagesPipeline(ImagesPipeline):

  def file_path(self, request, response=None, info=None, *, item=None):

    image_perspective = request.url.split('/')[-1]
    image_filename = f'{image_perspective}.jpg'

    return image_filename


