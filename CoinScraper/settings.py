BOT_NAME = "CoinScraper"

SPIDER_MODULES = ["CoinScraper.spiders"]
NEWSPIDER_MODULE = "CoinScraper.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
  "CoinScraper.pipelines.MyImagesPipeline": 100,
  "CoinScraper.pipelines.CoinPipeline": 300,
}


IMAGES_STORE = "./images"

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"