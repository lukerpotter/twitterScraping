# twitterScraping

So this all started with some hubris. I thought "I wonder how I could scrape a bunch of tweets featuring my name, and then make a word cloud showing the results!" This was a bit of an exercise in "can I do this, and what can I do to produce a minimum viable 'product'?".

## Of Note

1) The real meat of this resides in the "scrape_data.py" and "word_cloud.py" files.
2) If you'd like to run this code for your own purposes, you'll need to import the Twint library using the following command. My current IDE is PyCharm, and I was unable to get Twint working properly using my standard practice of 

```
pip install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint
```
