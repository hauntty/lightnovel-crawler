# -*- coding: utf-8 -*-
import logging
import re

from lncrawl.core.crawler import Crawler


logger = logging.getLogger(__name__)


class WolfPubCrawler(Crawler):
    base_url = ['http://www.wolfpub.org/']
    
    def read_novel_info(self):
        # TODO: [MUST IMPLEMENT] It is used to get the novel title and chapter list.
        #       Use the `self.novel_url` to get the following info:
        #
        #       `self.novel_title`: Must be set
        #       `self.novel_autor`: Comma separated list of author [optional]
        #       `self.novel_cover`: Cover image url [optional]
        #       `self.volumes`: A list of volumes. Each volume should contain these keys:
        #          `id`     : the index of the volume
        #          `title`  : the volume title [optional]
        #       `self.chapters`: A list of chapters. Each chapter should contain these keys:
        #          `id`     : the chapter number [required]
        #          `title`  : the title name [optional]
        #          `volume` : the volume number [required]
        #          `url`    : the link where to download the chapter [required]
        #
        #       You may throw an Exception in case of failure
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('h2.notice').text
        self.novel_author = soup.select_one('title').text.split('|')[1].strip()
        chapters = soup.select_one('select[name="unit_id]"').select('option')[1:]
        for chap_id,chapter in enumerate(chapters):
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
                                 'url':  (self.novel_url,chapter['value']),
                                 'title': chapter.text.strip(),
                             })
     
    def download_chapter_body(self, chapter):
        # TODO: [MUST IMPLEMENT] Download body of a single chapter and return a
        #       clean html format. You may use `chapter['url']` here.
        #
        # NOTE: Set `chapter['body_lock'] = True` to disable post-formatting.
        #       It can be useful in non-english sources, e.g. aixdzs, qidiancom, tiknovel
        #
        #       Return an empty body if anything goes wrong. But you should not return `None`.
        url,unit_id = chapter['url']
        retry_count=3
        response=self.submit_form(url,data={'unit_id':str(unit_id),'submit':'GO'},timeout=5)
        soup = self.make_soup(response)
        contents = soup.find("div", {"class": "storytext"})
        self.clean_contents(contents)
        return str(contents)
