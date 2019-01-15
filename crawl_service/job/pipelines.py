# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from job.items import JobItem


class CsvPipeline(object):

    def __init__(self):
        self.files = {}
        self.exporter = CsvItemExporter(
            fields_to_export=JobItem.fields.keys(), file=open("job.csv", 'wb'))

        @classmethod
        def from_crawler(cls, crawler):
            pipeline = cls()
            crawler.signals.connect(
                pipeline.spider_opened, signals.spider_opened)
            crawler.signals.connect(
                pipeline.spider_closed, signals.spider_closed)
            return pipeline

    def spider_opened(self, spider):
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
