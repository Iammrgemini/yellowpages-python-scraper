import scrapy


class B2bleadsSpider(scrapy.Spider):
    name = "B2Bleads"

    start_urls = [
        'https://www.yellowpages.com/search?search_terms=Investments&geo_location_terms=Los+Angeles%2C+CA',
        'https://www.yellowpages.com/search?search_terms=asset+management+companies&geo_location_terms=Los+Angeles%2C+CA',
        # Add more start URLs as needed
    ]

    def parse(self, response):
        # Extracting the URLs of the business listings on the current page
        listing_urls = response.xpath("//div[@class='search-results organic']/div[@class='result']//a[@class='business-name']/@href").extract()

        base_url = 'https://www.yellowpages.com'
        # Visiting each business listing page
        for listing_url in listing_urls:
            page_url = response.urljoin(base_url + listing_url)
            yield scrapy.Request(url=page_url, callback=self.parse_listing)

        # Extracting the URL of the next page, if available
        next_page_url = response.xpath("//div[@class='pagination']//li/a[@class='next ajax-page']/@href").get()

        # If a next page URL is found, follow it
        if next_page_url is not None:
            next_page = response.urljoin(base_url + next_page_url)
            yield response.follow(url=next_page, callback=self.parse)

    def parse_listing(self, response):
        # Extracting phone number
        phone_number = response.xpath("//a[@class='phone dockable']//strong/text()").get()

        # Extracting business name
        business_name = response.xpath("//div[@class='sales-info']//h1[@class='dockable business-name']/text()").get()

        # Extracting email
        try:
            email = response.xpath("substring-after(//a[@class='email-business']/@href, 'mailto:')").get()
        except:
            email = None

        # Extracting address
        address = response.xpath("string(//span[@class='address'])").get()



        # Extracting website
        website = response.xpath("//*[@class='website-link dockable']/@href").get()

        # Extracting general information
        general_info = response.xpath("//*[@class='general-info']/text()").get()

        # Extracting extra phone numbers (if available)
        try:
            extra_phones = response.xpath("//*[@class='extra-phones']//p/text()").extract()
        except:
            extra_phones = None

        yield {
            'phone_number': phone_number,
            'business_name': business_name,
            'email': email,
            'address': address,
            'website': website,
            'general_info': general_info,
            'extra_phones': extra_phones
        }
