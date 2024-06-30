import scrapy


class LinkedInSpider(scrapy.Spider):
    name = "linkedin"
    allowed_domains = ["www.linkedin.com"]
    start_urls = ["https://www.linkedin.com/"]

    def parse(self, response):
        # print(f"==>> response: {response.body}")
        form = response.css("main section.flex-nowrap div div.hero-cta-form form")
        loginCsrfParam = form.css("input[name='loginCsrfParam']::attr(value)").extract_first()
        print(f"==>> loginCsrfParam: {loginCsrfParam}")
        print(f"==>> form: {form}")
        
        yield scrapy.FormRequest.from_response(response,
                                         formdata={'csrf_token': loginCsrfParam,
                                                   'session_password': '2608f12e-a9be-48ce-8e64-01cfcdd03fd1',
                                                   'session_key': 'rsh.globaliasoft@gmail.com'},callback=self.start_scraping)
        pass
    
    def start_scraping(self, response):
        print(f"==>> response: {response}")
        cookies = response.headers.getlist('Set-Cookie')
        print(f"==>> cookies: {cookies}")
        data = response.css("div.application-outlet")
        pass

