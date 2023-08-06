## GusPI
A package to include statistical supports.

Quick start

```
$ python3 -m pip install -U GusPI
```

#### GusPI.scrape

The scrape package provides an easy way to scrape Yelp business info and Yelp reviews for specific business.

Function 1 - YelpBizInfo
The function collects business info and save it into a csv file.

```
#Example

#declare a list: https://www.yelp.com/biz/`artisan-ramen-milwaukee`
CUISINES = ['artisan-ramen-milwaukee','red-light-ramen-milwaukee-5']

#scrape the business info
scrape.YelpBizInfo(CUISINES)
```

Function 2 - YelpReview
The function collects reviews for respective business and save them into separate files by business names.
```
#Example

#declare a list: https://www.yelp.com/biz/`artisan-ramen-milwaukee`
CUISINES = ['artisan-ramen-milwaukee','red-light-ramen-milwaukee-5']

#scrape the business info
scrape.YelpReview(CUISINES)
```
