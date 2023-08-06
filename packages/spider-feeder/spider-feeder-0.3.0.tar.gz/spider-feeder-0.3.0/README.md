# spider-feeder
[![PyPI version](https://badge.fury.io/py/spider-feeder.svg)](https://badge.fury.io/py/spider-feeder)
[![Build Status](https://travis-ci.com/ejulio/spider-feeder.svg?branch=master)](https://travis-ci.com/ejulio/spider-feeder)

spider-feeder is a library to help loading inputs to scrapy spiders.

## Install

* `pip install spider-feeder` to load only local files
* `pip install spider-feeder[s3]` to load files from AWS S3
* `pip install spider-feeder[collections]` to load from Scrapinghub Collections

## Requirements

* If using `s3`, it requires `botocore`
* If using `collections`, it requires `python-scrapinghub`
* Otherwise, no requirements

## Usage (plain text)

Create a file `urls.txt` in your project with some urls (as in the example below).
```
https://url1.com
https://url2.com
https://url3.com
```

Then, in `settings.py`
```
EXTENSIONS = {
    'spider_feeder.loaders.StartUrlsLoader': 0
}

SPIDERFEEDER_INPUT_URI = './urls.txt'
```

And run the spider `scrapy crawl myspider.com`

Once the URLs were loaded, the total count will be stored in a stats 
`spider_feeder/<spider.name>/url_count`.
This value is simply `len(spider.start_urls)`.

## Usage (csv/json)

Create a file `urls.csv` in your project with some urls (as in the example below).
```
id,input_url
1,https://url1.com
2,https://url2.com
3,https://url3.com
```

Then, in `settings.py`
```
EXTENSIONS = {
    'spider_feeder.loaders.StartUrlsAndMetaLoader': 0
}

SPIDERFEEDER_INPUT_URI = './urls.csv'
SPIDERFEEDER_INPUT_FIELD = 'input_url'
```

The same applies for `json`, just requiring to update the file extension to `.json` instead of `.csv`.
This means that the input file format is inferred from the given file extension.

If you need the extra fields in the input files, you can write `start_requests` to get them.
```
# my_spider.py

class MySpider(scrapy.Spider):

    def start_requests(self):
        # super().start_requests() makes requests using URLs in self.start_urls
        # self.start_meta is populated with extra fields from input by StartUrlsAndMetaLoader
        for (request, meta) in zip(super().start_requests(), self.start_meta):
            request.meta.update(meta)
            yield request
```


## Extensions

There are two extensions to load input data to your spiders.

* `spider_feeder.loaders.StartUrlsLoader`: sets a list of urls to `spider.start_urls`
* `spider_feeder.loaders.StartUrlsAndMetaLoader`: overrides `spider.start_urls` and a custom attribute `spider.start_meta` with extra metadata parsed from `json`, `csv` or `collections`.

## Settings

`SPIDERFEEDER_INPUT_URI` is the URI to load URLs from.
* If _scheme_ (`file`, `s3`, `collections`) is not provided, it'll default to `file`
* It can be formatted using spider attributes like `%(param)s` (similar to `FEED_URI` in scrapy)
* Supported schemes are:
    * `''` or `file` for local files
    * `s3` for AWS S3 (requires `botocore`)
        * The URI can be formatted as `s3://key_id:secret_key@bucket/blob.txt`
        * If `key_id` and `secret_key` are not provided in the URI, they can be provided by the following settings: `SPIDERFEEDER_AWS_ACCESS_KEY_ID` and `SPIDERFEEDER_AWS_SECRET_ACCESS_KEY`.
        * If they are not provided by these settings, they will fall back to `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
        * If not set, they can be set as environment variables from `botocore`, but a warning will be logged by `spider-feeder`.
    * `collections` for [Scrapinghub Collections](https://doc.scrapinghub.com/api/collections.html)
    * `http` or `https` to load from any URI

`SPIDERFEEDER_INPUT_FILE_ENCODING` sets the file encoding. DEFAULT = `'utf-8'`.

`SPIDERFEEDER_INPUT_FORMAT` sets the file format (`txt`, `csv`, `json`). DEFAULT = `None`.
This setting is preferred over the file extension in `SPIDERFEEDER_INPUT_URI`.
So, if `SPIDERFEEDER_INPUT_FORMAT` is set, this is the one to be used, otherwise
it will fall back to the file extension in `SPIDERFEEDER_INPUT_URI`.

`SPIDERFEEDER_INPUT_FIELD` sets the url field when parsing `json` or `csv` files.

`SPIDERFEEDER_FILE_HANDLERS` is a set of functions to be matched with the given file scheme.
You can set your own and it'll be merged with the default one.
The interface is just a plain function with three arguments `file_uri`, `encoding` and `settings`.
```
# settings.py
SPIDERFEEDER_FILE_HANDLERS = {
    's3': 'myproject.my_custom_s3_reader.open'
}

# myproject.my_custom_s3_reader.py
def open(file_uri, encoding, settings):
    # my code here
    pass
```

`SPIDERFEEDER_FILE_PARSERS` is a set of parsers to be matched with the given file extension.
You can set your own and it'll be merged with the default one.
The interface is a `class` with `__init__(settings: scrapy.Settings)` and `parse(fd: file object) -> Union[List[str], List[dict]]` method.
Return `List[str]` if there is no extra `meta` to be returned.
Return `List[dict]` with a key `SPIDERFEEDER_INPUT_FIELD` and some extra `meta`.
```
# settings.py
SPIDERFEEDER_FILE_PARSERS = {
    's3': 'myproject.my_custom_parser.parse'
}

# myproject.my_custom_parser.py
def parse(fd, settings):
    # some parsing strategy
    return ['url1', 'url2']
```

`SPIDERFEEDER_STORES` is a set of absctractions to load URLs from.
Currently, `FileStore` for `file://`, `s3://`, `http://`, `https://`, and `ScrapinghubCollectionStore` for `collections://`.
Say you want to load URLs from an API, then you can add your custom `Store` and set it to an scheme.
```
# settings.py
SPIDERFEEDER_STORES = {
    'http': 'myproject.custom_store.HttpStore'
}

# myproject.custom_store.py
class HttpStore:
    def __init__(self, input_uri, settings):
        # do somethig here
        pass

    def __iter__(self):
        for url in self._api_request():
            yield (url, {})
            # the second tuple element is the extra data/fields from the API 

    def _api_request(self):
        # load URLs from the API and return them
        return []
```
