# -*- coding: utf-8 -*-
import scrapy


class AutotalliSpider(scrapy.Spider):
    name = "autotalli"
    allowed_domains = ["autotalli.com"]
    current_page = 1
    start_url = 'https://www.autotalli.com/vaihtoautot/listaa/sivu/{}'
    start_urls = [start_url.format(1)]

    def parse(self, response):
        skelbimu_linkai = response.css('a.carsListItemNameLink::attr(href)').extract()
        for link in skelbimu_linkai:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_skelbimas)
        if skelbimu_linkai:
            self.current_page += 1
            yield scrapy.Request(url=self.start_url.format(self.current_page), callback=self.parse)

    def parse_skelbimas(self, response):
        kaina = response.css("div.carPrice span::text").extract_first()
        title = response.css('h1.carTitle::text').extract_first()

        kilometrazas = {}
        for carDetailsLine in response.css('div.carDetailsGroup div.carDetailsLine'):
            name = carDetailsLine.css('div.label::text').extract_first()
            if name == 'Mittarilukema':
                value = carDetailsLine.css('div.value::text').extract_first()
                kilometrazas.update({name.strip(): value.strip()})
        photo = response.css('div.image img::attr(src)').extract()
        yield {
            'kaina': kaina,
            'skelbimo_pavadinimas': title,
            'kilometrazas': kilometrazas,
            'fotkes': photo
        }