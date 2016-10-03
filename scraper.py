from lxml import html
import requests
import urllib
import re

class GumScraper():
    """
    Scrape gum tree ads, add content constraints
    """
    def __init__(self):
        pass

    def do_search(
            self,
            search_term,
            max_pages=10,
            location=None,
            radius=0,
            min_price=0,
            max_price=10000):

        url = "http://www.gumtree.com.au/s-search-results.html?"
         
        params = {'keywords': search_term,
                  'locationStr': location,
                  'radius': radius,
                  'sortbyNama': 'date',
                  'minPrice': min_price,
                  'maxPrice': max_price,
                  'pageSize':100,
                  'pageNum':1}
        
        params = {k:v for k,v in params.items() if v is not None}
        full_url = url + urllib.parse.urlencode(params)
        
        request = requests.get(full_url)
        text = request.text

        last_page = self._find_last_page(text)
        ads = self._parse_ads(text)

        min_page = min(max_pages,last_page)

        for page_num in range(2,min_page+1):
            params['pageNum'] = page_num
            full_url = url + urllib.parse.urlencode(params) 
            request = requests.get(full_url)
            ads.extend(self._parse_ads(request.text))

        return ads

    def _find_last_page(self,page_text):
       tree = html.fromstring(page_text) 
       last_page_ref = tree.xpath('//a[@class="paginator__button paginator__button-last"]')

       if not last_page_ref:
           return 1

       relative_url = last_page_ref[0].attrib['href'] 

       return int(re.findall('page-(\d+)',relative_url)[0])

    def _parse_ads(self,page_text):
        # get title, cost, date
        #page = requests.get(url)
        tree = html.fromstring(page_text)

        ad_subtrees = tree.xpath('//div[@class="ad-listing__details"]')
        
        def _get_first_text(tree,search_string):
            return tree.xpath(search_string)[0].text_content().strip()
        
        ads = []
        for ad in ad_subtrees:
            title = _get_first_text(ad,'div/h6[@class="ad-listing__title"]/a/span[@itemprop="name"]')
            price = _get_first_text(ad,'div/div[@class="ad-listing__price"]/div/span[@class="j-original-price"]')
            date = _get_first_text(ad,'div/div[@class="ad-listing__date"]')
            url_relative = ad.xpath('div/h6[@class="ad-listing__title"]/a[@class="ad-listing__title-link"]')[0].attrib['href']
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
        description = tree.xpath('//div[@id="ad-description-details"]/text()')
        self.description= '\n\n'.join(description).strip()
        self.title = title
        self.cost = cost
    
