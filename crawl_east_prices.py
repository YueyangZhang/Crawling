from SWSpider import *
from SWSpider.spiders.sw_spider import *
import SWSpider.settings

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

east_test = ['DTW', 'BOS', 'DCA', 'FLL', 'MDW']
runner = CrawlerRunner(get_project_settings())
dfs = set()
for x in xrange(0, len(east_test)):
    for y in xrange(0, len(east_test)):
    	if x==y:
    		continue
        d = runner.crawl(
            'sw_spider', depCity=east_test[x], arrCity=east_test[y], x=x, y=y, filename='east_prices')
        dfs.add(d)

defer.DeferredList(dfs).addBoth(lambda _: reactor.stop())
# the script will block here until all crawling jobs are finished
reactor.run()
