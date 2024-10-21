# All configuation files are in here
# config.py

from rich.traceback import install

install(show_locals=True)

URLS = [
    "https://nhentai.net/",
    "https://www.ehentai.com/",
    "https://allporncomic.com/porncomic/my-bigger-half-amarsroshta/1-5-my-bigger-half-images-only-amarsroshta/",
    # Add more URLs here
]

BROWSER_SETTINGS = {
    "viewport": {"width": 1920, "height": 1080},
    "locale": "pt-BR",
}

GEOLOCATION = {"latitude": -22.9068, "longitude": -43.1729}

OUTPUT_DIRS = {
    "screenshots": "screenshots",
    "videos": "videos",
}
