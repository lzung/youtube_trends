import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# NLP IMPORTS
nltk.download("vader_lexicon")
nltk.download("punkt")

sid = SentimentIntensityAnalyzer()

# Read in data
data = pd.read_csv('../data/CA_youtube_trending_data_processed.csv', parse_dates=True, index_col=0)
data['tags'] = data['tags'].str.replace(r'(?:[^\w\s]|_)+', ' ', regex=True).str.strip()

def get_relative_length(text, YOUTUBE_ALLOWED_CHARS=500.0):
    return len(text) / YOUTUBE_ALLOWED_CHARS

def get_length_in_words(text):
    return len(nltk.word_tokenize(text))

def get_sentiment(text):
    scores = sid.polarity_scores(text)
    return scores["compound"]

data = data.assign(rel_char_len=data['tags'].apply(get_relative_length))
data = data.assign(n_words=data['tags'].apply(get_length_in_words))
data = data.assign(vader_sentiment=data['tags'].apply(get_sentiment))

data.to_csv('../data/CA_youtube_nltk.csv')