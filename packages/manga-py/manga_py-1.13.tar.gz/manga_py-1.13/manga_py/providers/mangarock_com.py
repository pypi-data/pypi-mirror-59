from manga_py.crypt import MangaRockComCrypt
from manga_py.fs import rename, unlink, basename
from manga_py.provider import Provider
from .helpers.std import Std

# api example:
"""
curl 'https://api.mangarockhd.com/query/web401/manga_detail?country=Japan' --compressed --data '{"oids":{"mrs-serie-100226981":0},"sections":["basic_info","summary","artworks","sub_genres","social_stats","author","character","publisher","scanlator","other_fact","chapters","related_series","same_author","feature_collections"]}'
"""


class MangaRockCom(Provider, Std):
    crypt = None
    __content = ''
    __api_uri = 'https://api.mangarockhd.com/query/'

    def get_chapter_index(self) -> str:
        return str(self.chapter_id)

    def get_main_content(self):
        name = self._get_name(r'/manga/([^/]+-\d+)')
        return self.http_get('{}/manga/{}'.format(
            self.domain,
            name
        ))

    def get_manga_name(self) -> str:
        return self.text_content(self.content, 'h1')

    def get_chapters(self):
        idx = self._get_name('/manga/([^/]+)')
        url = '{}info?oid={}&last=0&country=Japan'.format(self.__api_uri, idx)
        items = self.json.loads(self.http_get(url))
        return [(i.get('oid'),) for i in items.get('data', {}).get('chapters', [])][::-1]

    def __get_url(self):
        return '{}pages?oid={}&country=Japan'.format(self.__api_uri, self.chapter[0])

    def get_files(self):
        items = self.json.loads(self.http_get(self.__get_url()))
        return items.get('data')

    # decrypt
    def after_file_save(self, _path, idx: int):
        _path_wp = _path + 'wp'
        with open(_path, 'rb') as file_r:
            with open(_path_wp, 'wb') as file_w:
                file_w.write(self.crypt.decrypt(file_r.read()))
        unlink(_path)
        rename(_path_wp, _path)

    def save_file(self, idx=None, callback=None, url=None, in_arc_name=None):
        _path, idx, _url = self._save_file_params_helper(url, idx)
        in_arc_name = basename(_path) + '.webp'
        return super().save_file(idx, callback, _url, in_arc_name)

    def get_cover(self) -> str:
        selector = 'div:not([class]) > div[class] > div[class] > div[class] > div[class] > img'
        url = '{}{}'.format(self.domain, self._get_name('(/manga/[^/]+)'))
        img = self._elements(selector, self.http_get(url))
        if img and len(img):
            return img[0].get('src')

    def prepare_cookies(self):
        # patch api version
        v = self.re.compile(r'\bAJAX_MRAPI_VERSION\b\s*=\s*[\'"]?(web\d+)')
        self.__api_uri += v.search(self.content).group(1) + '/'

        self.crypt = MangaRockComCrypt()

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self.get_url()


main = MangaRockCom
