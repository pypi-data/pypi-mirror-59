# twipper - Twitter Wrapper written in Python

[![Python Version](https://img.shields.io/pypi/pyversions/twipper.svg)](https://pypi.org/project/twipper/)
[![PyPi Version](https://img.shields.io/pypi/v/twipper.svg)](https://pypi.org/project/twipper/)
[![Package Status](https://img.shields.io/pypi/status/twipper.svg)](https://pypi.org/project/twipper/)
[![Build Status](https://dev.azure.com/alvarob96/alvarob96/_apis/build/status/alvarob96.twipper?branchName=master)](https://dev.azure.com/alvarob96/alvarob96/_build?definitionId=1&_a=summary)
[![Build Status](https://img.shields.io/travis/alvarob96/twipper/master.svg?label=Travis%20CI&logo=travis&logoColor=white)](https://travis-ci.org/alvarob96/twipper)
[![Documentation Status](https://readthedocs.org/projects/twipper/badge/?version=latest)](https://twipper.readthedocs.io/)
[![Downloads](https://img.shields.io/pypi/dm/twipper.svg?style=flat)](https://pypistats.org/packages/twipper)

<p align="center">
  <img src="https://raw.githubusercontent.com/alvarob96/twipper/master/docs/twipper.jpg" width="300" height="350"/>
</p>

## Introduction

**twipper** is an acronym that stands for Twitter wrapper; so the package is made in order to cover Twitter API 
endpoints defined as Python functions for both Free and Premium plans, which they both include batch and stream 
processing functions.

## Installation

In order to get this package working you will need to install it using pip by typing on the terminal:

``$ python -m pip install twipper --upgrade``

Or just install the current release or a specific release version such as:

``$ python -m pip install twipper==0.1.6``

## Usage

As **twipper** is a Twitter Wrapper written in Python its main purpose is to wrap all the available endpoints listed on
the Twitter API for both versions (Free and Premium), so to use them from a simple function call. So on the main step is
to validate Twitter API credentials since they are mandatory in order to work with the Twitter API.

```python
import twipper

cred = twipper.Twipper(consumer_key='consumer_key',
                       consumer_secret='consumer_secret',
                       access_token='access_token',
                       access_token_secret='access_token_secret')
```

Now once the ``Twipper`` credentials object has been properly created we can use it in order to work with the Twitter
API using Python. In the case that we want to retrieve data from Twitter based on a query, e.g. we want to search `cat`
tweets to analyze its content to launch a cat campaign for our brand (random example because everybody loves cats).

```python
from twipper.batch import search_tweets

tweets = search_tweets(access=cred,
                       query='cats',
                       page_count=1,
                       filter_retweets=True,
                       verified_account=False,
                       language='en',
                       result_type='popular',
                       count=10)
```

So on, using ``batch`` functions you can retrieve historical *tweets* from the last 7-30 days matching the introduced
query, in this case the query is `cats` due to our cat campaign, remember it. Anyways, params can be adjusted to our
desires and/or needs as described on the API Reference.


## Contribute

As this is an open source project it is open to contributions, bug reports, bug fixes, documentation improvements, 
enhancements and ideas.

Also there is an open tab of [issues](https://github.com/alvarob96/twipper/issues) where anyone can contribute opening 
new issues if needed or navigate through them in order to solve them or contribute to its solving.

## Disclaimer

This package has been created in order to cover Premium Twipper API functions since [tweepy](https://www.tweepy.org/), 
the most used Python package working as a Twitter API wrapper. Anyways, [twipper](https://github.com/alvarob96/twipper)
also covers both Free and Premium functions, which include batch processing and stream processing.

Conclude that this is the result of a research project, so this package has been developed with research purposes and
no profit is intended.
