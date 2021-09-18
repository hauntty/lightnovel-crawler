# -*- coding: utf-8 -*-
"""
Use this template to create new sources.

TODO: Read the TODOs carefully.
TODO: You should remove all TODOs tag.
TODO: You can safely delete all [OPTIONAL] methods if you do not need them
"""
import logging
from lncrawl.core.crawler import Crawler

logger = logging.getLogger(__name__)


class R18NovelCrawler(Crawler):

    # TODO: [REQUIRED] Provide the URLs supported by this crawler.
    base_url = [
        'https://r18novel.com/'
    ]

    def read_novel_info(self):
        # TODO: [REQUIRED] Get some necessary information about the novel.
        #       The current novel url is available at `self.novel_url`.
        #       Check the base lncrawl.core.crawler.Crawler class for useful methods.
        #
        #       `self.novel_title`: a string [required]
        #       `self.novel_autor`: a comma separated string. [optional]
        #       `self.novel_cover`: the cover image url [optional]
        #       `self.chapters`: A list of chapters. Each chapter should contain these keys:
        #          `id`     : the chapter number [required]
        #          `volume` : the volume number [required]
        #          `url`    : the link to download the chapter [required]
        #          `title`  : the title name [optional]
        #       `self.volumes`: Unique list of volumes used inside the chatpers.
        #          `id`     : the index of the volume [required]
        #          `title`  : the volume title [optional]
        #
        #       You may throw an Exception in case of failure
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('h1.g1-alpha-2nd').text.strip()
        self.novel_author = 'Unknown'
        soup, = soup.find_all("div", {"class": "entry-content"})
        urls = [url for url in soup.find_all('a') if url['href'].startswith('https://r18novel.com')]
        for chap_id,url in enumerate(urls):
            if len(self.chapters) % 100 == 0:
                 vol_id = chap_id//100 + 1
                 vol_title = 'Volume ' + str(vol_id)
                 self.volumes.append({
                                    'id': vol_id,
                                     'title': vol_title,
                                    })
            self.chapters.append({
                                 'id': chap_id+1,
                                 'volume': vol_id,
                                 'url':  url['href'],
                                 'title': url.text.strip(),
                             })

    def download_chapter_body(self, chapter):
        # TODO: [REQUIRED] Download content of a single chapter and return it in a
        #       clean html format. You can use `chapter['url']` to get the contents.
        #
        #       To keep it simple, check `self.extract_contents` in the parent `Crawler` class.
        #       It extracts chapter contents given a soup Tag, and returns a clean HTML.
        url=chapter['url']
        soup = self.get_soup(url)
        contents, = soup.find_all('div',{'class':'entry-content'})
        self.clean_contents(contents)
        return str(contents)

