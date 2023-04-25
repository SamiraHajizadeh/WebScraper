# Define your item pipelines here
# useful for handling different item types with a single interface

import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from pathlib import PurePosixPath
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline


class CoinPipeline:
  def process_item(self, item, spider):



    adapter = ItemAdapter(item)


    print('type is', adapter.keys())

    if adapter.get('Volume'):
      raise DropItem(f"Volume is not missing in {item}")
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


  def get_media_requests(self, item, info):
    for image_url in item['image_urls']:
      yield scrapy.Request(image_url)

  def item_completed(self, results, item, info):
    image_paths = [x['path'] for ok, x in results if ok]
    if not image_paths:
      raise DropItem("Item contains no images")
    adapter = ItemAdapter(item)
    adapter['image_paths'] = image_paths
    return item

