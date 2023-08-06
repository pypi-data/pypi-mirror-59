# InfiniteTrends

 [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwyl/esta/issues) [![Inline docs](http://inch-ci.org/github/ashernoel/infinitetrends.svg?branch=master)](http://inch-ci.org/github/ashernoel/infinitetrends) [![HitCount](http://hits.dwyl.io/ashernoel/infinitetrends.svg)](http://hits.dwyl.io/ashernoel/infinitetrends)

**InfiniteTrends** is a Python API built upon [pytrends](https://github.com/GeneralMills/pytrends) to query data from [trends.google.com](http://www.trends.google.com).

Installation
------------

To install with pip, run

```
pip install InfiniteTrends
```
You can also clone this repository and run `python setup.py install`.

Documentation
------------
### Interest Over Time For Many Keywords

Use the `get_interest_over_time(keywords, region, timeframe, topic_flag)` function to list all chart names:

```Python
>>> import InfiniteTrends
>>> output = InfiniteTrends.get_interest_over_time(["Harvard University", "Yale University"], "US", "2019-01-01 2020-01-01", True)
```

The arguments are:

* `keywords` &ndash; The input terms. 
    - Keywords cannot contain duplicates. 
    - There is no cap on the number of inputted keywords. 
    - All terms are scaled by the 1st (0th index) keyword.
* `region` &ndash; The geographic region of interest.   
  - This is usually a two letter country abbreviation
  - For example, the United States is ```'US'``` and the world is ```''```
  - There is more detail available for states, provinces, and cities by specifying additonal abbreviations. For example, Alabama is ```'US-AL'``` and England is ```'GB-ENG'```.
* `timeframe` &ndash; A string in "YYYY-MM-DD YYYY-MM-DD" that signifies the start and end of the interval of interest. 
* `topic_flag` &ndash; A boolean indicator. 
    - If this is FALSE, then keywords will be vanilla "Search Terms" in Google Trends. 
    - If this is TRUE, then results will use the first "Topic" that come up when typing in a keyword into the searchbar on the Google Trends website.


### Viral Terms Related to One Keyword

Use the `get_viral_keywords(keyword, region, timeframe, interval, cutoff)` function to return a list of all of the **'Viral'** terms that people searching for a keyword also searched for over a period of time. 

**Definition of a Viral Term:** Any keyword related to searches of a master `keyword` that saw an increase in Google Trends traffic of over `cutoff`% during at least one period of `interval` days in a specified `region` during a longer `timeframe`. A keyword is *related* to another if people searching for one often search for another. 

```Python
>>> import InfiniteTrends
>>> output = InfiniteTrends.get_viral_keywords("Netflix", "US", "2019-01-01 2020-01-01", 7, 300)
```


The arguments are:

* `keyword` &ndash; This is the ONE input term. 
* `region` &ndash; The geographic region of interest.   
  - This is usually a two letter country abbreviation
  - For example, the United States is ```'US'``` and the world is ```''```
  - There is more detail available for states, provinces, and cities by specifying additonal abbreviations. For example, Alabama is ```'US-AL'``` and England is ```'GB-ENG'```.
* `timeframe` &ndash; A string in "YYYY-MM-DD YYYY-MM-DD" that signifies the start and end of the total interval of interest. 
* `interval` &ndash; The length of time that a keyword has to increase in traffic a `cutoff` amount. See the **Definition of a Viral Term** above for a more precise wording. 
* `cutoff` &ndash; An integer indicating the percentage increase in traffic that a keyword related to the master `keyword` must experience to be recognized as a **Viral Term**. For example, 100 would indicate 100%. 

Made with InfiniteTrends
------------

["Analyzing College Prestige and Virality Through Google Trends"](https://medium.com/harvard-open-data-project/analyzing-college-prestige-and-virality-through-google-trends-218b9ea767e6). This project and accompanying [github repository](https://github.com/ashernoel/Viral-Trends-Clustering) analyzed interest in colleges and then the clustered viral keywords related to Harvard and MIT specifically. The unsupervised clusterings of the viral topics reflect a divergence in the cultures of the two Cambridge institutions.



Dependencies
------------
* [Pandas](https://pandas.pydata.org/)
* [Pytrends](https://github.com/GeneralMills/pytrends) 
