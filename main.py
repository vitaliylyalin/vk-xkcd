import os
import requests
from random import randint
from dotenv import load_dotenv




def make_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def download_image(url, title, path):
    make_dir(path)
    img_data = requests.get(url).content
    image_name = f'{title}.png'
    with open(os.path.join(path, image_name), 'wb') as handler:
        handler.write(img_data)
    return image_name


def delete_image(image_name):
    os.remove(os.path.join(path, image_name))


def make_post_request(url, params):
    request = requests.post(url, params)
    return request.json()


def get_random_comics():
    comics_number = randint(1, 2000)
    comics_url = f'http://xkcd.com/{comics_number}/info.0.json'
    response = requests.get(comics_url).json()
    url = response.get('img')
    title = response.get('title')
    return download_image(url, title, path)


def get_wall_upload_server():
    method = 'photos.getWallUploadServer'
    params = {
    'group_id': group_id,
    'album_id': album_id,
    'access_token': access_token,
    'v': api_version
    }
    url = f'https://api.vk.com/method/{method}'
    response = make_post_request(url, params)
    response_data = response.get('response')
    upload_url = response_data.get('upload_url')
    return upload_url


def upload_image(image):
    upload_url = get_wall_upload_server()
    image_name = os.path.join(path, image)
    multipart_form_data = {'photo': open(image_name, 'rb')}
    request = requests.post(upload_url, files = multipart_form_data)
    response = request.json()
    return response


def save_wall_photo(image_name):
    method = 'photos.saveWallPhoto'
    data = upload_image(image_name)
    keys = {
    'group_id': group_id,
    'access_token': access_token,
    'v': api_version
    }
    params = data.copy()
    params.update(keys)
    url = f'https://api.vk.com/method/{method}'
    request = make_post_request(url, params)
    response = request.get('response')
    return response


def publish_photo(owner_id, photo_id, title):
    method = 'wall.post'
    params = {
    'message': title,
    'attachments': f'photo{owner_id}_{photo_id}',
    'owner_id': f'-{group_id}',
    'access_token': access_token,
    'from_group': 1,
    'v': api_version
    }
    url = f'https://api.vk.com/method/{method}'
    response = make_post_request(url, params)
    print(response)


def main():
    image_name = get_random_comics()
    title = image_name.split('.')[0]
    data = save_wall_photo(image_name)[0]
    owner_id = data.get("owner_id")
    photo_id = data.get('id')
    publish_photo(owner_id, photo_id, title)
    delete_image(image_name)


if __name__ == '__main__':
    load_dotenv()
    group_id = os.getenv('GROUP_ID')
    album_id = os.getenv('ALBUM_ID')
    access_token = os.getenv('ACCESS_TOKEN')
    api_version = os.getenv('API_VERSION')
    path = os.getenv('IMAGES_PATH')
    main()
