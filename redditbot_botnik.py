"""
@author: Nicholas
"""
# Parse specified sub reddit
# Generate a word cloud based on hot submission, remove common words
# Save with date and sub in filename

# https://www.pythonforengineers.com/build-a-reddit-bot-part-1/
# https://praw.readthedocs.io/en/latest/


# Prerequisite
# ----------
# Pip install Praw (Python Reddit API Wrapper)
# Register for API on dev reddit, obtain ID & secret
# Update praw.ini
# for read only, no need for username, password

import praw

# Libraries below are for plotting word cloud
# https://www.datacamp.com/community/tutorials/wordcloud-python
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# libraries for getting date to name files
from datetime import date
today = date.today()

import nltk
from nltk.corpus import stopwords

reddit = praw.Reddit('Botnik')

# Select subreddit to lurk
sub = 'Futurology'
# sub = 'Technology'
# sub = 'news'

# filename based on dates
# Script will save wordcloud with date appended in filename
filename = today.strftime("%y%m%d-") + sub + "-Wordcloud"

subreddit = reddit.subreddit(sub)
# Declare list to store all entries to parse
submission_list = []

for submission in subreddit.hot(limit=202):
    submission_list.append(submission.title)
    print("Title: ", submission.title)
    print("Upvote: ", submission.score)

# mask to include reddit alien logo
# PNG Replace 0 with 255 values (Irfanview does this)
reddit_mask = np.array(Image.open("reddit_alien_mask.png"))
submission_list = submission_list[2:len(submission_list)] # remove first two entries which are gibberish
stopwords = set(stopwords.words('english')) # remove common english words


wordcloud = WordCloud(
        mask = reddit_mask, contour_width = 1, contour_color = 'firebrick', 
        stopwords = stopwords, max_words = 250, background_color = "white").generate(",".join(submission_list))
wordcloud.to_file(filename+".png")  # save entry

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
