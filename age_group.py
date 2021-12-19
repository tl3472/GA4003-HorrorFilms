import scrapy


class AgeGroupSpider(scrapy.Spider):
    name = 'age_group'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?genres=horror&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=EKJ8W5VMQD5XX6PT23RD&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_12']

    def parse(self, response):
        for movie_page_link in response.css("div.lister-item-content h3 a::attr(href)").getall():
            next_page = response.urljoin(movie_page_link)
            yield scrapy.Request(next_page,callback=self.parse_movie_page)

        next_page = response.css("div.desc a.next-page::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)

    def parse_movie_page(self,response):
        for main_page_link in response.css("div.RatingBarButtonBase__ContentWrap-sc-15v8ssr-0.jQXoLQ.rating-bar__base-button a::attr(href)").getall():
            main_page = response.urljoin(main_page_link)
            yield scrapy.Request(main_page,callback=self.parse_age_page)
        
    def parse_age_page(self,response):
        movie = response.css("div.parent h3 a::text").get()
        year = response.css("div.parent h3 span.nobr::text").get()[-19:-15]
        rate_all = float(response.css("table div.bigcell::text").getall()[0])
        rate_1 = float(response.css("table div.bigcell::text").getall()[1])
        rate_2 = float(response.css("table div.bigcell::text").getall()[2])
        rate_3 = float(response.css("table div.bigcell::text").getall()[3])
        rate_4 = float(response.css("table div.bigcell::text").getall()[4])
        number_all = int(response.css("table div.smallcell a::text").getall()[0][21:-17].replace(',',''))
        number_1 = int(response.css("table div.smallcell a::text").getall()[1][21:-17].replace(',',''))
        number_2 = int(response.css("table div.smallcell a::text").getall()[2][21:-17].replace(',',''))
        number_3 = int(response.css("table div.smallcell a::text").getall()[3][21:-17].replace(',',''))
        number_4 = int(response.css("table div.smallcell a::text").getall()[4][21:-17].replace(',',''))
        
        yield{
            "Movie" : movie,
            "Year" : year,
            "Rate_All Ages" : rate_all,
            "Rate_<18" : rate_1,
            "Rate_18-29" : rate_2,
            "Rate_30-44" : rate_3,
            "Rate_45+" : rate_4,
            "Number_All Ages" : number_all,
            "Number_<18" : number_1,
            "Number_18-29" : number_2,
            "Number_30-44" : number_3,
            "Number_45+" : number_4,
        }

