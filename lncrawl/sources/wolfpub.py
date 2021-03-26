# -*- coding: utf-8 -*-
import logging
import re

from ..utils.crawler import Crawler


logger = logging.getLogger(__name__)


class WolfPubCrawler(Crawler):
    base_url = ['http://www.wolfpub.org/contributors/']

    
    def read_novel_info(self):
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('h2',{'class':'notice'}).text
        self.novel_author = soup.select_one('title').text.split('|')[1].strip()
        chapters = soup.select_one('select',{'name':'unit_id'}).select('option')[1:]
        for chap_id,chapter in enumerate(chapters):
            if len(self.chapters) % 100 == 0:
                 vol_id = chap_id//100 + 1
                 vol_title = 'Volume ' + str(vol_id)
                 self.volumes.append({
                                    'id': vol_id,
                                     'title': vol_title,
                                    })
            self.chapters.append({
                                 'id': chap_id,
                                 'volume': vol_id,
                                 'url':  (self.novel_url,chapter['value']),
                                 'title': chapter.text.strip(),
                             })
     
    def download_chapter_body(self, chapter):
        url,unit_id = chapter['url']
        response=self.submit_form(url,data={'unit_id':str(unit_id),'submit':'GO'})
        soup = self.make_soup(response)
        contents = soup.find("div", {"class": "storytext"})
        self.clean_contents(contents)
        return str(contents)
