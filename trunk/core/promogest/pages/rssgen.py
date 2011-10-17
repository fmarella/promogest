# -*- coding: utf-8 -*-

import datetime
import PyRSS2Gen
from core.dao.News import News
from core import Environment

def rssgen(req):
    itemss = []
    news = News().select(active=True, batchSize=20)
    for n in news:
        itemss.append(
        PyRSS2Gen.RSSItem(
            title = n.title,
            link = "http://www.promotux.it/promoGest/news_detail/%s" %str(n.permalink),
            description = n.abstract,
            guid = "http://www.promotux.it/promoGest/news_detail/%s"%str(n.permalink),
            author= str(n.user.username),
            pubDate = n.publication_date))
    rss = PyRSS2Gen.RSS2(
        title = "PromoTux news feed",
        link = "http://www.promotux.it",
        description = "Un sito di sviluppo software open source",

        lastBuildDate = datetime.datetime.now(),

        items = itemss)

    rss.write_xml(open(Environment.STATIC_PATH_FEED +"/newsfeed.xml", "w"))
#    rss.write_xml(open(Environment.STATIC_PATH_FEED +"/promoGest2/newsfeed.xml", "w"))
