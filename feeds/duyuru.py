#!/usr/bin/env python3
from urllib.request import urlopen
import os
import json
import datetime


def get_bulletin(title="", json_file="", feed_url="", json_url="", site_key="", url="", **kwargs):
    if os.path.exists(json_file):
        with open(json_file) as f:
            feed = json.load(f)
    else:
        feed = json.loads(f'{{"version": "https://jsonfeed.org/version/1", "title": "{title}", "icon": "https://micro.blog/jsonfeed/avatar.jpg", "home_page_url": "https://www.jsonfeed.org/", "feed_url": "{feed_url}", "items": []}}')

    response = urlopen(json_url)
    if response.status != 200:
        item = {
            "id": "Hata",
            "title": "Hata",
            "content_html": "Hata",
            "date_published": f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            "url": url
        }
        feed['items'].append(item)
    else:
        entries = json.loads(response.read())
        for entry in filter(lambda x: x['Header'] not in map(lambda x: x['id'], feed['items']), entries['Data']['Data']):
            content_url = f'https://service-cms.istanbul.edu.tr/api/webclient/f_getNoticeDetail?siteKey={site_key}&EID={entry["EID"]}'
            response = urlopen(content_url)
            content_link = ""
            if entry['Link']:
                content_link = f'<a href="{entry["Link"]}">Link için tıklayınız.</a></br>'
            if response.status != 200:
                content_html = f'No content. 😥 <a href="{url}"> Duyurular </a>'
            else:
                content = json.loads(response.read())
                content_html = f'<h1>{content["Data"]["Header"]}</h1> {content["Data"]["Content"]}'

            item = {
                "id": f"{entry['Header']}",
                "title": f"{entry['Header']}",
                "content_html": content_link + content_html,
                "date_published": f"{entry['Date']}",
                "url": url
            }
            feed['items'].append(item)
    with open(json_file, 'w', encoding='utf8') as f:
        json.dump(feed, f, ensure_ascii=False)


bulletins = [
    {
        'title': 'İ.Ü. DETAE Duyuruları',
        'json_file': 'detae.json',
        'feed_url': 'https://anadoluihalesi2020.com/detae.json',
        'url': 'https://deneyseltip.istanbul.edu.tr/tr/duyurular/1/1',
        'json_url': 'https://service-cms.istanbul.edu.tr/api/webclient/f_getNotices?siteKey=68768CE67AD24E3F8F15463A0BC509B7&Categoryid=1&Page=1',
        'site_key': '68768CE67AD24E3F8F15463A0BC509B7'
    },
    {
        'title': 'İ.Ü. Sağlık Bilimleri Enstitüsü Duyurular',
        'json_file': 'saglik.json',
        'feed_url': 'https://omics.sbs/feeds/saglik.json',
        'url': 'https://saglikbilimleri.istanbul.edu.tr/tr/duyuru/',
        'json_url': 'https://service-cms.istanbul.edu.tr/api/webclient/f_getNotices?siteKey=0655757D2F0042B5A13545C936EA6C07&Categoryid=1&Page=1',
        'site_key': '0655757D2F0042B5A13545C936EA6C07'
    },
    # {
    #     'title': 'İ.Ü. Hukuk Fakültesi Duyurular',
    #     'json_file': 'hukuk.json',
    #     'feed_url': 'https://anadoluihalesi2020.com/hukuk.json',
    #     'url': 'https://hukuk.istanbul.edu.tr/tr/duyurular/1/1',
    #     'json_url': 'https://service-cms.istanbul.edu.tr/api/webclient/f_getNotices?siteKey=CFF15DD1B5CD496892C7E57BAF0660A4&Categoryid=1&Page=1',
    #     'site_key': 'CFF15DD1B5CD496892C7E57BAF0660A4'
    # },
    # {
    #     'title': 'İ.Ü. Hukuk Fakültesi Öğrenci Duyuruları',
    #     'json_file': 'hukukogrenci.json',
    #     'feed_url': 'https://anadoluihalesi2020.com/hukukogrenci.json',
    #     'url': 'https://hukuk.istanbul.edu.tr/tr/duyurular/3/1',
    #     'json_url': 'https://service-cms.istanbul.edu.tr/api/webclient/f_getNotices?siteKey=CFF15DD1B5CD496892C7E57BAF0660A4&Categoryid=3&Page=1',
    #     'site_key': 'CFF15DD1B5CD496892C7E57BAF0660A4'
    # },
]

os.chdir(os.path.dirname(os.path.realpath(__file__)))
[get_bulletin(**bulletin) for bulletin in bulletins]
