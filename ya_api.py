import requests
import json

class YaUploader:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def put_folder(self, folder):
        name_url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {"path": folder, "overwrite": "true"}
        headers = self.get_headers()
        response = requests.put(url=name_url, headers=headers, params=params)
        return

    def info(self, file, type_file):
        info = [{
            "file_name": f'{file}.jpg',
            "size": type_file
        }]
        json_object = json.dumps(info, indent=2)
        return json_object

    def get_upload(self, type_file, folder, file_path):
        analiz_url = "https://cloud-api.yandex.net/v1/disk/resources"
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        nomber = 0
        headers = self.get_headers()
        name = file_path
        params = {"path": f'{folder}/{name}{type_file}', "overwrite": "true"}
        response2 = requests.get(url=analiz_url, headers=headers, params=params)
        while response2.status_code != 404:
            nomber += 1
            name = f'{file_path}_{nomber}'
            params = {"path": f'{folder}/{name}{type_file}', "overwrite": "true"}
            response2 = requests.get(url=analiz_url, headers=headers, params=params)
        response = requests.get(url=upload_url, headers=headers, params=params)
        return response.json(), name

    def upload(self, folder, disk_file_path, filename):
        type_file = ".jpg"
        data, file = self.get_upload(type_file, folder, file_path=disk_file_path)
        url = data.get('href')
        req = requests.get(filename)
        response = requests.put(url=url, data=req)
        response.raise_for_status()

    def upload_json(self, folder, disk_file_path, file_type):
        type_file = ".json"
        data, file = self.get_upload(type_file, folder, file_path=disk_file_path)
        url = data.get('href')
        info_json = self.info(file, file_type)
        response = requests.put(url=url, data=info_json)
        response.raise_for_status()
