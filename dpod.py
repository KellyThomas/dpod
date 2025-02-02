"""
    (c) 2024 Kelly Thomas  
    This Source Code Form is subject to the terms of the Mozilla
    Public License, v. 2.0. If a copy of the MPL was not distributed
    with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import feedparser
from slugify import slugify
import os
from datetime import datetime as dt
import shutil
from urllib.request import urlopen, Request
import yaml
import argparse


mime_extentions = {"audio/mpeg": "mp3"}
headers =  {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0"}


def main():
    parser = argparse.ArgumentParser(
        epilog="Either the --url or --urls must be provided"
    )
    parser.add_argument(
        "--home_dir",
        help="Path to download home directory, defaults to current directory",
    )
    parser.add_argument("--url", help="URL for a single RSS feed")
    parser.add_argument(
        "--urls", help="Path for text file listing URLs for a multiple RSS feeds"
    )
    args = parser.parse_args()

    home_dir = args.home_dir if args.home_dir else "."
    home_dir = os.path.abspath(home_dir)

    urls = set()
    if args.url:
        urls.add(args.url)
    if args.urls:
        with open(args.urls, "r") as f:
            for url in f:
                urls.add(url)

    if len(urls) == 0:
        print("No URL(s) provided")
        parser.print_help()
        exit(1)

    download_podcasts(list(urls), home_dir)


def download_podcasts(urls: list, home_dir: str) -> None:
    for url in urls:
        fp = feedparser.parse(url)
        podslug = slugify(fp.feed.title)
        podcast_dir = os.path.join(home_dir, podslug)
        if not os.path.isdir(podcast_dir):
            os.makedirs(podcast_dir)

        for e in fp.entries:
            download_podcast_episode(e, podcast_dir)


def download_podcast_episode(episode, podcast_dir) -> None:
    episode_date = parse_rss_date(episode.published).strftime("%Y%m%d")
    episode_base_name = f"{episode_date}-{slugify(episode.title)}"
    episode_link = [l for l in episode.links if l["rel"] == "enclosure"][0]
    episode_ext = mime_extentions[episode_link["type"]]
    episode_audio_file = os.path.join(podcast_dir, f"{episode_base_name}.{episode_ext}")
    episode_txt_file = os.path.join(podcast_dir, f"{episode_base_name}.txt")

    if os.path.isfile(episode_audio_file):
        print(f"found: {episode_audio_file}")
    else:
        with urlopen(Request(episode_link["href"], headers=headers)) as response:
            with open(episode_audio_file, "wb") as af:
                shutil.copyfileobj(response, af)
                print(f"downloaded: {episode_audio_file}")

    with open(episode_txt_file, "w") as tf:
        metadata = {
            "title": episode.title if episode.title else "unknow",
            "duration":episode.itunes_duration if "itunes_duration" in episode else "unknown",
            "sumary": episode.summary if episode.summary else "unknown",
        }
        tf.write(yaml.dump(metadata))


def parse_rss_date(datestring: str) -> dt:
    # see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    try:
        return dt.strptime(datestring, "%a, %d %b %Y %H:%M:%S %z")
    except:
        pass
    try:
        return dt.strptime(datestring, "%a, %d %b %Y %H:%M:%S %Z")
    except:
        pass
    raise ValueError(f"ERROR WITH DATESTRING: {datestring}")


if __name__ == "__main__":
    main()
