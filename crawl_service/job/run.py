from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet.error import ReactorNotRestartable
from spiders.topdev import TopdevSpider
from spiders.itviec import ItviecSpider


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(ItviecSpider)
    process.crawl(TopdevSpider)
    try:
        process.start()
    except ReactorNotRestartable as e:
        pass
    finally:
        process.stop()
