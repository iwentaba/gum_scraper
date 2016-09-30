from lxml import html
import requests
import urllib

class GumScraper():
    """
    Scrape gum tree ads, add content constraints
    """
    def __init__(self,url):
        self.url = url

    def do_search(self,search_term):
        # Returns list of ads 
        pass
    
    def _parse_page(self,url):
        # get title, cost, date
        page = requests.get(url)
        tree = html.fromstring(page.content)

        ad_subtrees = tree.xpath('//div[@class="ad-listing__details"]')
        
        def _get_first_text(tree,search_string):
            return tree.xpath(search_string)[0].text_content().strip()
        
        ads = []
        for ad in ad_subtrees:
            title = _get_first_text(ad,'div/h6[@class="ad-listing__title"]/a/span[@itemprop="name"]')
            price = _get_first_text(ad,'div/div[@class="ad-listing__price"]/div/span[@class="j-original-price"]')
            date = _get_first_text(ad,'div/div[@class="ad-listing__date"]')
            url_relative = _get_first_text(ad,'div[@class="ad-listing__extra-info"]/div[@class="ad-listing__date"]')
            url = urllib.parse.urljoin('http://www.gumtree.com.au',url_relative)
            
            ads.append(Ad(url,title,price))
        return ads

class Ad:
    """
    Single gumtree Ad
    """

    def __init__(self,url,title=None,cost=None):
        self.url = url
        self.title = title
        self.cost = cost

        # Parse url
        page = requests.get(url)
        tree = html.fromstring(page.content) 

        # Parse description, title, price,  date listed/edited, address
        self.description = tree.xpath('//div[@id="ad-description-details"]/text()')
        self.title
    
