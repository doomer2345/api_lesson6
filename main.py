import requests
from dotenv import load_dotenv
import os
import random


def get_comic():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    last_comic = response.json()["num"]
    random_comic_num = random.randint(1, last_comic)
    random_comic_url = f'https://xkcd.com/{random_comic_num}/info.0.json'
    random_comic = requests.get(random_comic_url)
    random_comic.raise_for_status()
    url_image = random_comic.json()["img"]
    comment = random_comic.json()["alt"]
    dowloand_image(url_image, "комикс.jpg")
    return comment


def dowloand_image(url, filepath, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(filepath, 'wb') as file:
        file.write(response.content)


def get_upload_url(vk_access_key):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': vk_access_key,
        'v': '5.131',
        'group_id': vk_group_id
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def save_wall_photo(vk_access_key, vk_photo, vk_hash, vk_server):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': vk_access_key,
        'group_id': vk_group_id,
        'hash': vk_hash,
        'photo': vk_photo,
        'server': vk_server,
        'v': '5.131'
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()['response'][0]['id'], response.json()['response'][0]['owner_id']


def send_photo_to_server(upload_url):
    with open('комикс.jpg', 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        return response.json()['hash'],response.json()['photo'],response.json()['server']


def upload_photo_to_wall(vk_media_id, vk_owner_id, vk_access_key):
    url = 'https://api.vk.com/method/wall.post'
    params = {
        'access_token': vk_access_key,
        'v': '5.131',
        'owner_id': f'-{vk_group_id}',
        'from_group': 1,
        'attachments': f'photo{vk_owner_id}_{vk_media_id}',
        'message': comment
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    load_dotenv()
    comment = get_comic()
    vk_group_id = os.getenv("VK_GROUP_ID")
    vk_access_key = os.getenv("VK_ACCESS_TOKEN")
    upload_url = get_upload_url(vk_access_key)
    vk_hash,vk_photo,vk_server = send_photo_to_server(upload_url)
    vk_media_id, vk_owner_id = save_wall_photo(vk_access_key,vk_photo, vk_hash, vk_server)
    upload_photo_to_wall(vk_media_id, vk_owner_id, vk_access_key)
    os.remove('комикс.jpg')

