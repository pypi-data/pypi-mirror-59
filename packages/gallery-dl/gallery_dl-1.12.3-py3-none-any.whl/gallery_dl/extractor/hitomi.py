# -*- coding: utf-8 -*-

# Copyright 2015-2020 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extract images from https://hitomi.la/"""

from .common import GalleryExtractor
from .. import text, util
import string
import json


class HitomiGalleryExtractor(GalleryExtractor):
    """Extractor for image galleries from hitomi.la"""
    category = "hitomi"
    root = "https://hitomi.la"
    pattern = (r"(?:https?://)?hitomi\.la"
               r"/(?:manga|doujinshi|cg|gamecg|galleries|reader)"
               r"/(?:[^/?&#]+-)?(\d+)")
    test = (
        ("https://hitomi.la/galleries/867789.html", {
            "pattern": r"https://[a-c]a.hitomi.la/images/./../[0-9a-f]+.jpg",
            "keyword": "6701f8f588f119ef84cd29bdf99a399417b0a6a2",
            "count": 16,
        }),
        ("https://hitomi.la/galleries/1401410.html", {
            # download test
            "range": "1",
            "content": "b3ca8c6c8cc5826cf8b4ceb7252943abad7b8b4c",
        }),
        ("https://hitomi.la/galleries/733697.html", {
            # Game CG with scenes (#321)
            "url": "21064f9e3c244aca87f1a91967a3fbe79032c4ce",
            "count": 210,
        }),
        ("https://hitomi.la/galleries/1045954.html", {
            # fallback for galleries only available through /reader/ URLs
            "url": "0a67f5e6c3c6a384b578e328f4817fa6ccdf856a",
            "count": 1413,
        }),
        ("https://hitomi.la/manga/amazon-no-hiyaku-867789.html"),
        ("https://hitomi.la/manga/867789.html"),
        ("https://hitomi.la/doujinshi/867789.html"),
        ("https://hitomi.la/cg/867789.html"),
        ("https://hitomi.la/gamecg/867789.html"),
        ("https://hitomi.la/reader/867789.html"),
    )

    def __init__(self, match):
        self.gallery_id = match.group(1)
        self.fallback = False
        url = "{}/galleries/{}.html".format(self.root, self.gallery_id)
        GalleryExtractor.__init__(self, match, url)

    def request(self, url, **kwargs):
        response = GalleryExtractor.request(self, url, fatal=False, **kwargs)
        if response.status_code == 404:
            self.fallback = True
            url = url.replace("/galleries/", "/reader/")
            response = GalleryExtractor.request(self, url, **kwargs)
        elif b"<title>Redirect</title>" in response.content:
            url = text.extract(response.text, "href='", "'")[0]
            if not url.startswith("http"):
                url = text.urljoin(self.root, url)
            response = self.request(url, **kwargs)
        return response

    def metadata(self, page):
        if self.fallback:
            return {
                "gallery_id": text.parse_int(self.gallery_id),
                "title": text.unescape(text.extract(
                    page, "<title>", "<")[0].rpartition(" | ")[0]),
            }

        extr = text.extract_from(page, page.index('<h1><a href="/reader/'))
        data = {
            "gallery_id": text.parse_int(self.gallery_id),
            "title"     : text.unescape(extr('.html">', '<').strip()),
            "artist"    : self._prep(extr('<h2>', '</h2>')),
            "group"     : self._prep(extr('<td>Group</td><td>', '</td>')),
            "type"      : self._prep_1(extr('<td>Type</td><td>', '</td>')),
            "language"  : self._prep_1(extr('<td>Language</td><td>', '</td>')),
            "parody"    : self._prep(extr('<td>Series</td><td>', '</td>')),
            "characters": self._prep(extr('<td>Characters</td><td>', '</td>')),
            "tags"      : self._prep(extr('<td>Tags</td><td>', '</td>')),
            "date"      : self._date(extr('<span class="date">', '</span>')),
        }
        if data["language"] == "N/a":
            data["language"] = None
        data["lang"] = util.language_to_code(data["language"])
        return data

    def images(self, page):
        # set Referer header before image downloads (#239)
        self.session.headers["Referer"] = self.gallery_url

        # get 'galleryinfo'
        url = "https://ltn.hitomi.la/galleries/{}.js".format(self.gallery_id)
        page = self.request(url).text

        result = []
        for image in json.loads(page.partition("=")[2]):
            ihash = image["hash"]
            idata = text.nameext_from_url(image["name"])

            # see https://ltn.hitomi.la/common.js
            offset = int(ihash[-3:-1], 16) % 3
            url = "https://{}a.hitomi.la/images/{}/{}/{}.{}".format(
                chr(97 + offset),
                ihash[-1], ihash[-3:-1], ihash,
                idata["extension"],
            )
            result.append((url, idata))
        return result

    @staticmethod
    def _prep(value):
        return [
            text.unescape(string.capwords(v))
            for v in text.extract_iter(value or "", '.html">', '<')
        ]

    @staticmethod
    def _prep_1(value):
        return text.remove_html(value).capitalize()

    @staticmethod
    def _date(value):
        return text.parse_datetime(value + ":00", "%Y-%m-%d %H:%M:%S%z")
