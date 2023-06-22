import ya_api
import vk_api
from tqdm import tqdm

#Вместо многоточий указать соответствующие токины

vk_token = '...'
ya_token = "..."
domain = input('Введите ID пользователя: ')

# нечколько примеров ID пользователей:
# nutaloveis - 91503273
# nuta_id = 19439900,
# с очень большим числом альбомов = 2596709

if __name__ == '__main__':
    vk = vk_api.vk_init(token=vk_token)
    albums = vk.all_album(domain)
    ya = ya_api.YaUploader(token=ya_token)
    ya.put_folder(f'id_{domain}')
    for album in tqdm(albums):
        ya.put_folder(f'id_{domain}/{album}')
        grades = vk.archiv(domain, album)
        for grad in grades:
            ya.upload(f'id_{domain}/{album}', grad["like"], grad["url"])
            ya.upload_json(f'id_{domain}/{album}', grad["like"], grad["type"])
