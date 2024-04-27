# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviescraperItem(scrapy.Item):
    title = scrapy.Field()
    release_year = scrapy.Field()
    parental_rating = scrapy.Field()
    movie_duration = scrapy.Field()
    movie_rating = scrapy.Field()
    description = scrapy.Field()
    genres = scrapy.Field()
    budget = scrapy.Field()
    gross_na = scrapy.Field()
    gross_worldwide = scrapy.Field()
