import scrapy


class HorrormoviemainpagespiderSpider(scrapy.Spider):
    name = 'HorrormovieMainpageSpider'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?genres=horror&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=SE66BNSTQT060B1WZS2H&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_12']

    def parse(self, response):
        for movie_page_link in response.css("div.lister-item-content h3 a::attr(href)"):
            next_movie_page = response.urljoin(movie_page_link.get())
            yield scrapy.Request(next_movie_page, callback=self.parse_movie_page)

        next_page = response.css("div.desc a.next-page::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    
    def parse_movie_page(self, response):
        Name = response.css("h1::text").get()
        Year = response.css('li a::text').getall()[0]
        Rate = float(response.css("span.AggregateRatingButton__RatingScore-sc-1ll29m0-1.iTLWoV::text").get())
        genre = response.css("ul.ipc-metadata-list.ipc-metadata-list--dividers-all.Storyline__StorylineMetaDataList-sc-1b58ttw-1.esngIX.ipc-metadata-list--base li.ipc-metadata-list__item div ul li a.ipc-metadata-list-item__list-content-item.ipc-metadata-list-item__list-content-item--link::text").getall()
        country = response.css("div.styles__MetaDataContainer-sc-12uhu9s-0.cgqHBf ul.ipc-inline-list.ipc-inline-list--show-dividers.ipc-inline-list--inline.ipc-metadata-list-item__list-content.base li a::text").getall()[1]
        budget_0 = response.xpath('//li[@data-testid="title-boxoffice-budget"]//div/ul/li/span/text()').getall()[-1]
        budget = int(budget_0.replace('$','').replace(',','').replace('(estimated)',''))
        gross_world_0 = response.xpath('//li[@data-testid="title-boxoffice-cumulativeworldwidegross"]//div/ul/li/span/text()').getall()[-1]
        gross_world = int(gross_world_0.replace('$','').replace(',','').replace('(estimated)',''))

        yield {
                "Name": Name,
                "Year": Year,
                "Rate": Rate,
                "Genre": genre,
                "Country": country,
                "Budget": budget,
                "Gross Worldwide": gross_world
            }
