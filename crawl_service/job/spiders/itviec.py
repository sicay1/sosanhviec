# -*- coding: utf-8 -*-
import os
import re
import scrapy
import requests
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
import sys
sys.path.append("..")

from job.items import JobItem


def login():
    s = requests.Session()
    s.get('https://itviec.com')
    s.post('https://itviec.com/sign_in',
           data={
               "user[email]": "dactoan13396@gmail.com",
               "user[password]": "061028445",
               "sign_in_then_review": "false",
               "commit": "Sign in"})
    return dict(s.cookies)


class ItviecSpider(scrapy.Spider):
    name = "itviec"
    allowed_domains = ["itviec.com"]
    pages = [str(i) for i in range(1, 62)]
    list_urls = []
    for page in pages:
        link = "https://itviec.com/viec-lam-it?page={}".format(page)
        list_urls.append(link)
    start_urls = list_urls
    cookies = login()

    def parse(self, response):
        le = LinkExtractor()
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, self.parse_job, cookies=self.cookies)

    def parse_job(self, response):

        item = JobItem()

        item['LINK'] = response.url

        item['TITLE'] = response.xpath(
            '//h1[@class="job_title"]/text()').extract_first()
        if not item['TITLE']:
            return
        item['TITLE'] = response.xpath(
            '//h1[@class="job_title"]/text()').extract_first().replace('\n', ' ')

        item['SALARY'] = response.xpath(
            '//div[@class="salary"]/span[@class="salary-text"]/text()').extract_first()

        item['COMPANY'] = response.xpath(
            '//h3[@class="name"]/a/text()'
        ).extract_first()
        if not item['COMPANY']:
            return

        item['ADDRESS'] = response.xpath(
            '//div[@class="address__full-address"]/span/text()').extract_first().rsplit(',')[-1].strip()
        if not item['ADDRESS']:
            return

        skill = response.xpath(
            '//div[@class="tag-list"]/a[@class="big ilabel mkt-track"]/span/text()').extract()
        item['SKILL'] = ''.join(skill).replace('\n', ' ').split()
        if not item['SKILL']:
            return

        item['TYPE'] = response.xpath(
            '//p[@class="gear-icon"]/text()'
        ).extract_first().replace('\n', ' ')
        if not item['TYPE']:
            return

        req = response.xpath(
            '//div[@class="experience"]/ul/li/text()').extract()
        if not req:
            return
        for text in req:
            year = re.findall(
                r"(\d.*) (?:years of experience|years of|năm kinh nghiệm|of experience)", text)
            if year:
                if year:
                    item['EXP'] = year

            degree = re.findall(
                r'(?:Degree in|degree in|Tốt nghiệp) (.*)',
                text)
            if degree:
                item['DEGREE'] = degree[0]

        yield item
