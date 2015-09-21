from SWSpider import *
from SWSpider.spiders.sw_spider import *
import SWSpider.settings

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

west_test = ['LAX', 'SFO', 'DEN', 'LAS', 'SEA', 'SLC']
runner = CrawlerRunner(get_project_settings())
dfs = set()
for x in xrange(0, len(west_test)):
    for y in xrange(0, len(west_test)):
    	if x==y:
    		continue
        d = runner.crawl(
            'sw_spider', depCity=west_test[x], arrCity=west_test[y], x=x, y=y, filename='west_prices')
        dfs.add(d)

defer.DeferredList(dfs).addBoth(lambda _: reactor.stop())
# the script will block here until all crawling jobs are finished
reactor.run()
