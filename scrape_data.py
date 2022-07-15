"""
Twint will need to be installed using the following command:

pip install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint

I ran it from the terminal in PyCharm. I am not sure why this needs to be done
as opposed to just installing like every other module in PyCharm, but here we
are
"""
import io
import re
import string
import sys

import pandas as pd
import twint

# https://www.adamsmith.haus/python/answers/how-to-redirect-print-output-to-a-variable-in-python
old_stdout = sys.stdout
new_stdout = io.StringIO()
sys.stdout = new_stdout

search_term = "Luke"
csv_name = f"{search_term}.csv"

with open('output.txt', 'r') as file:
    desired_output = file.read()

# This process has a tendency to die out midway through the search. As this is
# a proof of concept at the moment, I'm putting this inside a loop that will
# continue until I force it to stop, and adding the "resume" option to the
# search such that it will pick up where it left off. This isn't the most
# elegant solution, but will work in the near term.
while 1:
    try:
        c = twint.Config()
        c.Search = search_term  # topic
        c.Store_csv = True  # store tweets in a csv file
        c.Output = csv_name  # path to csv file
        c.Since = "2022-07-14 00:00:00"
        c.Lang = "en"
        c.Resume = "my_search_id_.txt"
        twint.run.Search(c)

        # If we're done scraping, exit our loop. We're done here.
        output = new_stdout.getvalue()

        if output == desired_output:
            # Print normally again
            sys.stdout = old_stdout
            break
    except:
        continue

df = pd.read_csv(csv_name)

# Drop rows with any non-available data
df.dropna()

# Retrieve all English tweets
english_tweets = df.query('language=="en"')['tweet']

# Remove the search term from our tweet such that it is not included in our
# output
clean_tweets = [x.lower() for x in english_tweets]
# Remove various data from tweets:
# - user names
# - hash tags
# - URLS
# - various punctuation (', ’, ampersand)
# - multiple spaces
# - single characters

clean_tweets = [re.sub("@[A-Za-z0-9_]+", "", x) for x in english_tweets]
clean_tweets = [re.sub("#[A-Za-z0-9_]+", "", x) for x in clean_tweets]
clean_tweets = [re.sub(r'http\S+', '', x) for x in clean_tweets]
#clean_tweets = [x.replace("'s", " ") for x in clean_tweets]
#clean_tweets = [x.replace("’s", " ") for x in clean_tweets]
#clean_tweets = [x.replace("&amp;", " ") for x in clean_tweets]
clean_tweets = [re.sub("\s+", " ", x) for x in clean_tweets]
clean_tweets = [re.sub("(^| ).( |$)", "", x) for x in clean_tweets]


# Iterate through each tweet, breaking it apart at the spaces and adding it
# to a string containing all words found in all tweets
text = ""
for tweet in clean_tweets:
    text += " ".join(tweet.split()) + " "

# Remove common words from the tweets:
with open("common_words.txt") as file:
    lines = file.readlines()
    stopwords = [line.rstrip() for line in lines]

# We also want to remove the search term from our text such that it is
# not included in any further processing
#stopwords.append(search_term.lower())


resultwords  = [word for word in text.lower().split() if word not in stopwords]
result = ' '.join(resultwords)

# String out punctuation from words
result = result.translate(str.maketrans('', '', string.punctuation))

# Output text to file for consumption elsewhere
text_file = open(f"clean_tweets_{search_term}.txt", "w")
n = text_file.write(result)
text_file.close()
