# -*- coding: utf-8 -*-
import os
import re
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
import sys
sys.path.append("..")

from job.items import JobItem


class TopdevSpider(scrapy.Spider):
    name = "topdev"
    allowed_domains = ["topdev.vn"]
    pages = [str(i) for i in range(1, 27)]
    list_urls = []
    for page in pages:
        link = "https://topdev.vn/it-jobs/?page={}".format(page)
        list_urls.append(link)
    start_urls = list_urls

    def parse(self, response):
        le = LinkExtractor()
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, self.parse_job)

    def parse_job(self, response):

        item = JobItem()

        item['LINK'] = response.url

        item['TITLE'] = response.xpath(
            '//h1[@class="job-title"]/text()').extract_first()
        if not item['TITLE']:
            return

        salary = response.xpath(
            '//div[contains(@class, "salary")]/span/text()').extract_first()
        if salary:
            item['SALARY'] = salary
        if 'Up to' in salary:
            item['SALARY'] = re.findall('Up to (.*)', salary)
        if 'From' in salary:
            item['SALARY'] = re.findall('From (.*)', salary)

        item['COMPANY'] = response.xpath(
            '//span[@class="company-name text-lg block"]/strong/text()'
        ).extract_first()
        if not item['COMPANY']:
            return

        item['ADDRESS'] = response.xpath(
            '//span[@itemprop="address"]/text()').extract_first()
        if not item['ADDRESS']:
            return

        item['SKILL'] = response.xpath(
            '//span[@class="tag-skill"]/text()').extract()
        if not item['SKILL']:
            return

        item['TYPE'] = response.xpath(
            '//*[@id="image-employer"]/div/div/div/div[1]/div[1]/div/div[2]/span[2]/strong/text()'
        ).extract_first()
        if not item['TYPE']:
            item['TYPE'] = 'Not Mentioned'

        req = response.xpath(
            '//*[@id="job-requirement"]/div/div/ul/li/text()').extract()
        if not req:
            return
        for text in req:
            year = re.findall(
                r"(\d.*) (?:years of experience|years of experiences|year of experience|years of work|year experience in|year experienced|years work experience|years experience|years of professional|years elevant|years of|year of|of working|years hands-on|year programing|years and|years proven|year or|years software|-year|years'|years’ experience|kinh nghiệm)",
                text)
            if year:
                if year:
                    item['EXP'] = year

            degree = re.findall(
                r'(?:Degree in|Trình độ tối thiểu (Degree):|Tốt nghiệp) (.*)',
                text)
            if degree:
                item['DEGREE'] = degree[0][1]

        yield item
