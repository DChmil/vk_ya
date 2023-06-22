import requests
import time
from operator import itemgetter
vk_api_vers = 5.131

class vk_init:
    def __init__(self, token):
        self.token = token

    def get_album(self, domain):
        return {
            'owner_id': domain,
            'access_token': {self.token},
            'v': vk_api_vers,
        }

    def album_pars(self, domain):
        headers = self.get_album(domain)
        url_album = 'https://api.vk.com/method/photos.getAlbums'
        response_albom = requests.get(url=url_album, params=headers)
        data = response_albom.json()
        return data

    def all_album(self, domain):
        data = self.album_pars(domain)
        albom_id_all = ['wall', 'profile']
        for albom in data["response"]["items"]:
            albom_id = albom["id"]
            albom_id_all.append(str(albom_id))
        return albom_id_all

    def get_photo(self, domain, album):
        return {
            'owner_id': domain,
            'album_id': album,
            'access_token': {self.token},
            'extended': 1,
            'photo_sizes': 1,
            'count': 1000,
            'v': vk_api_vers,
        }

    def photo_pars(self, domain, album):
        headers = self.get_photo(domain, album)
        url_album = 'https://api.vk.com/method/photos.get'
        response_albom = requests.get(url=url_album, params=headers)
        data = response_albom.json()
        return data

    def archiv(self, domain, album):
        data = self.photo_pars(domain, album)
        arhiv = []
        for photo in list(reversed(data["response"]["items"]))[0: 5]:
            photo["sizes"] = sorted(photo["sizes"], key=itemgetter('height'))
            katalog = {}
            katalog["url"] = photo["sizes"][-1]["url"]
            katalog["type"] = photo["sizes"][-1]["type"]
            katalog["like"] = str(photo["likes"]["count"])
            arhiv.append(katalog)
        time.sleep(0.1)
        return arhiv

