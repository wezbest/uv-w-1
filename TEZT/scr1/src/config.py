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
    "rez": "screenshots",
    "rez": "videos",
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
