import requests
import os
from pyunsplash import PyUnsplash
from pynter import generate_captioned
from instagrapi import Client
from os.path import join, dirname, abspath
from dotenv import load_dotenv


dotenv_path = join(dirname(abspath("__file__")), '.env')
load_dotenv(dotenv_path)

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")
print(f"UNSPLASH_ACCESS_KEY: {UNSPLASH_ACCESS_KEY}")

INSTAGRAM_USERNAME = os.environ.get("INSTAGRAM_USERNAME")
print(f"INSTAGRAM_USERNAME: {INSTAGRAM_USERNAME}")
INSTAGRAM_PASSWORD = os.environ.get("INSTAGRAM_PASSWORD")
print(f"INSTAGRAM_PASSWORD: {INSTAGRAM_PASSWORD}")

IMAGE_OUTPUT_FILE = "RGB_IMAGE_OUTPUT.jpg"
font_path = './Roboto/Roboto-Regular.ttf'

cl = Client()

def get_client():
    cl.load_settings('dump.json')
    cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    cl.account_info().dict()

def convert_image(image_path, quote):
    im = generate_captioned(quote, image_path=image_path, size=(1080, 1350), font_path=font_path, filter_color=(0, 0, 0, 40))
    im.convert('RGB').save(IMAGE_OUTPUT_FILE)
    im.show()

def get_image_id():
    pu = PyUnsplash(api_key=UNSPLASH_ACCESS_KEY)
    photos = pu.photos(type_='random', count=1, featured=True, query="splash")
    [photo] = photos.entries
    print(f"photo_id: {photo.id} and download_link: {photo.link_download}")
    img_data = requests.get(photo.link_download).content
    with open(photo.id, 'wb') as handler:
        handler.write(img_data)
    return photo.id

def get_quotes():
    response = requests.get("https://api.quotable.io/random")
    print(f"received quote: {response.json()['content']}")
    return response.json()["content"]

def post_instagram(quote):
    get_client()
    hash_tags = "#bot #love #insta"
    # extract_hashtags(quote)
    cl.photo_upload(
        IMAGE_OUTPUT_FILE,
        hash_tags,
        extra_data={
            "custom_accessibility_caption": "alt text example",
            "like_and_view_counts_disabled": 0,
            "disable_comments": 0,
        }
    )

def main():
    quote =  get_quotes()
    image_id = get_image_id()
    convert_image(image_id, quote)
    post_instagram(quote)

if __name__ == "__main__":
    main()