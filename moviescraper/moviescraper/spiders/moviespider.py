import scrapy
import requests
import json
import numpy as np

class MoviespiderSpider(scrapy.Spider):
    name = "moviespider"
    allowed_domains = ["www.imdb.com"]
    pop_sample = ["https://www.imdb.com/chart/top/", "https://www.imdb.com/chart/bottom/", "https://www.imdb.com/chart/moviemeter/"]
    stratified_sample = ["https://www.imdb.com/search/title/?explore=genres&title_type=feature&user_rating=" + str(i) + "&sort=user_rating,asc" for i in np.arange(1.0, 8.0, 0.1)]
    start_urls = pop_sample + stratified_sample
    
    def parse(self, response):
        movies = response.css('div.ipc-page-grid ul li')
        for movie in movies:
            url = movie.css('a ::attr(href)').get()
            full_url = "https://www.imdb.com" + url
            yield response.follow(full_url, self.parse_item)

    def parse_item(self, response):
        main_content = response.css('.ipc-page-content-container')
        header = main_content.css('section section .sc-4e4cc5f9-3 ul')
        
        # Subitems
        subitems = header[1].css('li')
        if len(subitems) < 3:
            p_rating = ""
            movie_duration = subitems[1].css('li::text').get()
        else:
            p_rating = subitems[1].css('a::text').get()
            movie_duration = subitems[2].css('li::text').get()

        # Get list of genres
        genre_content = main_content.css('.sc-b7c53eda-4 .ipc-chip__text')
        genres = [genre.css('::text').get() for genre in genre_content]
        
        # Address duplication in html
        num_genres = (int)(len(genres)/2)
        genres = genres[0:num_genres]
        
        # Box Office Data
        box_list = main_content.css("[data-testid='title-boxoffice-section'] ul li div span")
        box_count = (int)(len(box_list)/2)
                
        
        # Final output
        yield{
            'title': main_content.css('.hero__primary-text::text').get(),
            'release_year': subitems[0].css('a::text').get(),
            'parental_rating': p_rating,
            'movie_duration': movie_duration,
            'movie_rating': float(main_content.css('.sc-bde20123-1::text').get()),
            'description': main_content.css('span.sc-a31b0662-0::text').get(),
            'genres': genres,
            'budget': box_list[0].css('::text').get() if box_count > 0 else '',
            'gross_na': box_list[1].css('::text').get() if box_count > 1 else '',
            'gross_worldwide': box_list[-1].css('::text').get() if box_count > 2 else ''
        }