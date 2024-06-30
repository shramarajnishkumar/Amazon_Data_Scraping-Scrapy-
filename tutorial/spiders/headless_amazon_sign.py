import scrapy
from scrapy_splash import SplashRequest
import base64

lua_script = """
function main(splash, args)
    splash:init_cookies(splash.args.cookies)

    assert(splash:go(args.url))
    assert(splash:wait(2))

    splash:set_viewport_full()

    local email_input = splash:select('input[name=email]')   
    email_input:send_text("YOUR AMAZON EMAIL OR MOBILE NO")
    assert(splash:wait(2))

    local email_submit = splash:select('input[id=continue]')
    email_submit:click()
    assert(splash:wait(3))

    local password_input = splash:select('input[name=password]')   
    password_input:send_text("YOUR AMAZON PASSWORD")
    assert(splash:wait(2))

    local password_submit = splash:select('input[id=signInSubmit]')
    password_submit:click()
    assert(splash:wait(3))

    return {
        html=splash:html(),
        url = splash:url(),
        png = splash:png(),
        cookies = splash:get_cookies(),
        }
    end
"""

class TwitterSpider(scrapy.Spider):
    name = "headless_amazon_sign"
    allowed_domains = ["amazon.com"]

    def start_requests(self):
        url = "https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"
        yield SplashRequest(
            url=url,
            callback=self.start_scrapping,
            endpoint='execute',
            args={
                'width': 1000,
                'lua_source': lua_script,  # Assuming lua_script is defined
                'ua': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            },
        )

    def start_scrapping(self, response):
        # Your existing code to save the response's PNG image and extract cookies
        imgdata = base64.b64decode(response.data['png'])
        filename = 'after_login.png'
        with open(filename, 'wb') as f:
            f.write(imgdata)

        cookies_dict = {cookie['name']: cookie['value'] for cookie in response.data['cookies']}
        
        # Define the list of URLs to scrape
        url_list = ['https://www.amazon.com/']
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.script_parse, cookies=cookies_dict)

    def script_parse(self, response):
        # Save the HTML content of the response to a file
        with open('response.html', 'wb') as f:
            f.write(response.body)

        # Scraping all the links on the page
        page_urls = response.css('a')
        for page_url in page_urls:
            if page_url.css('a::text').get() is not None:
                try:
                    yield {
                        'url_text': page_url.css('a::text').get(),
                        'url': page_url.css('a').attrib['href']
                    }
                except:
                    print("An error occurred when scraping a link")
