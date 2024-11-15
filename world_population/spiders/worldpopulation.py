import scrapy
from ..items import WorldPopulationItem
import logging

#logger = logging.getLogger(__name__)

class WorldpopulationSpider(scrapy.Spider):
    name = "worldpopulation"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country/"]

    def parse(self, response):
        #logger.info("Started parsing the response for %s", response.url)
        items = WorldPopulationItem()
        title = response.xpath("//h1/text()").get()
        countries = response.xpath("//td/a")

        for country in countries:
            country_name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            #print("country==>", country_name)
            #print("link==>", link)
            """
            try:
                absolute_url1 = response.urljoin(link)
                absolute_url2 = response.follow(link)
            except:
                pass
            yield {"countryName":country_name,"link1":absolute_url1, "link2":absolute_url2}
            """
            yield  response.follow(link, callback=self.handling_country, meta = {"country":country_name})

    def handling_country(self,response):
        country = response.meta["country"]
        rows = response.xpath("(//table[contains(@class,'table')])[1]/tbody/tr")

        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()

            yield {"country":country,
                   "year":year,
                   "population":population,}


