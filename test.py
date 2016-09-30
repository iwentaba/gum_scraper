import unittest
from scraper import GumScraper

class TestGumScraper(unittest.TestCase):
    def test_parse_page(self):
        url = 'http://www.gumtree.com.au/s-surfing/perth/kite/page-5/k0c18568l3008303'
        scrap = GumScraper(url)
        ads = scrap._parse_page(url)
        
        self.assertTrue(len(ads) > 0)
        self.assertTrue(type(ads[0].title) == type(''))
        self.assertTrue(type(ads[0].url) == type(''))
        self.assertTrue(type(ads[0].cost) == type(''))

        print(ads[0].title)
        

if __name__ == '__main__':
    unittest.main()
