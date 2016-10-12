import unittest
from scraper import GumScraper

class TestGumScraper(unittest.TestCase):
    def test_parse_page(self):
        scrap = GumScraper()
        ads = scrap.do_search("kite",max_pages=1,min_price=400)
        
        self.assertTrue(len(ads) > 0)
        self.assertTrue(type(ads[0].title) == type(''))
        self.assertTrue(type(ads[0].url) == type(''))
        self.assertTrue(type(ads[0].cost) == type(''))

        print(ads[0].title)
        print(ads[0].cost)

if __name__ == '__main__':
    unittest.main()
