# dpod

Podcast downloader

## Setup

1. Requirements:
   * recent Python 3.x, tested with 3.10

2. Clone repo

3. Create venv and install required packages:
```
    python -m venv venv
    ./venv/Scripts/activate
    pip install -r requirements.txt
```

## Usage

```
> python .\dpod.py --help
usage: dpod.py [-h] [--home_dir HOME_DIR] [--url URL] [--urls URLS] [--limit_podcast LIMIT_PODCAST] [--limit_total LIMIT_TOTAL]

options:
  -h, --help            show this help message and exit
  --home_dir HOME_DIR   Path to download home directory, defaults to current directory
  --url URL             URL for a single RSS feed
  --urls URLS           Path for text file listing URLs for a multiple RSS feeds
  --limit_podcast LIMIT_PODCAST
                        episode limit per podcast
  --limit_total LIMIT_TOTAL
                        total episode limit for the batch

Either the --url or --urls must be provided
```

### Single URL

```
>python .\dpod.py --url https://example.com/path/to/podcast.rss
```

### Multiple URLS

If `podcasts.txt` contains a list of podcast RSS URLS:
```
https://example.com/path/to/podcast.rss
https://example.com/path/to/another/podcast.rss
```
Then they can be downloaded as a batch.
```
>python .\dpod.py --url /local/path/to/podcasts.txt
```
### Download output

1. HOME_DIR will default to current working directory but can be set with a parameter.
2. In the home directory a podcast directory will be created with the slugified title of the podcast.
3. In the podcast directory files with will be created with a leading `YYYYMMDD` timestamp and a slugified title of the episode.

For example:

````
HOME_DIR/podcast-title/20231231-episode-title.mp3
HOME_DIR/podcast-title/20240101-another-episode-title.mp3
HOME_DIR/another-podcast-title/20231231-episode-title.mp3
HOME_DIR/another-podcast-title/20240101-another-episode-title.mp3
````

Each episode also has a matching *.txt with brief episode metadata.
