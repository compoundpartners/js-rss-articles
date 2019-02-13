# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.cache import cache
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from cms.models import CMSPlugin

import requests
from dateutil.parser import parse
from io import StringIO
from lxml import etree


@python_2_unicode_compatible
class RSSArticles(CMSPlugin):
    LAYOUT_CHOICES = [
        ('columns', _('Columns')),
        ('rows', _('Rows')),
        ('hero', _('Hero')),
        ('articles', _('Articles')),
    ]

    title = models.CharField(_('title'), max_length=255, blank=True, null=True)
    url = models.CharField(_('rss url'), max_length=255, blank=True, null=True)
    count = models.IntegerField(_('number of articles'))
    layout = models.CharField(_('layout'), max_length=30, choices=LAYOUT_CHOICES)

    def __str__(self):
        return self.title or _('RSS Articles')

    def get_rss(self):
        cache_key = 'rss-articles-%s' % self.pk
        rss = cache.get(cache_key)
        if not rss:
            rss = []
            if self.url:
                doc = requests.get(self.url)
                if doc.status_code == requests.codes.ok:
                    tree = etree.fromstring(doc.text.encode('utf-8'))
                    rows = tree.xpath('//item')
                    nsmap = tree.nsmap.copy()
                    for row in rows[:self.count]:
                        try:
                            item = {}
                            parser = etree.HTMLParser()
                            if not row.xpath('guid'):
                                continue
                            item['link'] = row.xpath('guid')[0].text
                            if not row.xpath('title'):
                                continue
                            item['title'] = row.xpath('title')[0].text
                            if not row.xpath('dc:date', namespaces=nsmap):
                                continue
                            item['date'] = parse(row.xpath('dc:date', namespaces=nsmap)[0].text, ignoretz=True)
                            if not row.xpath('description'):
                                continue
                            html = etree.parse(StringIO(row.xpath('description')[0].text), parser)
                            if not html.xpath('//img/@src'):
                                continue
                            item['image'] = str(html.xpath('//img/@src')[0])
                            etree.strip_tags(html, '*')
                            if not html.xpath('//html'):
                                continue
                            item['text'] = html.xpath('//html')[0].text.strip()
                            rss.append(item)
                        except:
                            pass

                    cache.set(cache_key, rss, 300)
        return rss
