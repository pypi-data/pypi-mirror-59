# MTSB

MTSB (Movie Tweet Sentiment Boxoffice) is a python module that collects tweets about movies, performs a sentiment analysis and correlates it with the boxoffice result of the week after the movie release.

## Features

* Collect tweets about movies
* Creates hashtags for each movie
* Performs sentiment analysis on those tweets using Google's API and returns a weighted geometric average of score and magnitude
* Gets boxoffice data from boxofficemojo
* Performs correlation between the sentiment analysis and boxoffice data

## Requirements

* Python >= 3.5 (Might work on older version but it has not been tested)
* All module dependencies are installed on installation, but you will also need:
    * You need to have set up correctly ntlk module: https://www.nltk.org/install.html
    * Performed at least once "ntlk.download()"
    * Already have API keys for tweet collection: https://developer.twitter.com/en.html
    * Already have API keys for Google Natural Language: https://cloud.google.com/natural-language/docs/setup
* You also need to have the following services installed (tested on Linux system)
    * Jupyter-lab
    * MongoDB
    * Nifi
    * Kafka
    
## Installation

In order to install MTSB you can simply:

```
pip install mtsb
```

## Docs

* tweet_collector()

Collect tweets about movies. It lets you choose between movies released in 2019 and releasing in 2020. It then creates a list of hashtags based on the movie's name and top actors and uses it to collect tweets from twitter.

```
import mtsb

mtsb.tweet_collector()
```

* sentiment()

Performs sentiment analysis on collected tweets using Google's API and returns a weighted geometric average of score and magnitude.

```
import mtsb
mtsb.sentiment()
```

* sentiment_boxoffice_all()

Creates a dataframe with the following info for each movie:
    * Movie title
    * Weighted geometric average of score and magnitude (from sentiment() )
    * Gross boxoffice for the week after the movie release

```
import mtsb

mtsb.sentiment_boxoffice_all()
```

* spearman_corr(df)

Performs a spearman correlation using the df returned by sentiment_boxoffice_all().

```
mtsb.spearman_corr(df)
```

## Acknowledgements

Useful python libraries used:
* [imdbpy library](https://github.com/alberanid/imdbpy/ "imdbpy library title")
* [ntlk library](https://github.com/nltk/nltk "ntlk library title")
* [beautifulSoup library](https://pypi.org/project/beautifulsoup4/ "beautifulSoup library title")

## Licence

MIT licensed. See the bundled [LICENSE](https://github.com/federicodeservi/mtsb-analyzer/blob/master/LICENSE "LICENSE title") file for more details. 
