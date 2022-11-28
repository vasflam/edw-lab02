from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import requests
import numpy
import re
import pickle
import  nltk
from nltk.util import ngrams, everygrams, pad_sequence
from nltk.tokenize import word_tokenize
from nltk.lm import MLE, WittenBellInterpolated
from pprint import pprint
from .cache import Cache
from .const import DEV_MODE, DEVELOPER_KEY, CSE_ID

def search(query: str):
    if DEV_MODE:
        with open("response.p", "rb") as fp:
            return pickle.load(fp)

    service = build("customsearch", "v1", developerKey=DEVELOPER_KEY)
    response = (
        service.cse()
        .list(
            q=query,
            filter=0,
            cx=CSE_ID
        )
        .execute()
    )

    with open("response.p", "wb") as fp:
        pickle.dump(response, fp)

    return response

def cleanup_text(text):
    text = text.lower()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = re.sub(",|, ", " ", text)
    sentences = re.split("\. ", text)
    text = ' '.join(sentences)
    return text

def get_url_text(cache: Cache, link: str, **kwargs) -> str:
    html = cache.get(link)
    if html is None:
        r = requests.get(link)
        html = r.text
        cache.set(link, html)
    soup = BeautifulSoup(html, features="html.parser")
    for tag in soup(["script", "style", "iframe", "img", "path", "a"]):
        tag.extract()
    article = soup.find('article')
    if article:
        text = article.get_text()
    else:
        text = soup.get_text()

    #n = 10
    #tokens = tokenize_text(text, n)
    #grams = generate_grams(tokens, n)
    #freq = nltk.FreqDist(grams).most_common()
    #pprint(freq[0:30])

    return text

def tokenize_text(text, n):
    text = cleanup_text(text)
    tokens = list(pad_sequence(word_tokenize(text), n, pad_left=True, left_pad_symbol = "<s>"))
    filter_words = ['.', '``', '\'\'', '""', '-', ')', '(', ':', ' ', '', '...']
    tokens = list(filter(lambda word: word not in filter_words, tokens))
    tokens = list(filter(lambda word: len(word) > 2, tokens))
    return tokens

def generate_grams(tokenized_text, n):
    return list(everygrams(tokenized_text, max_len=n))

def create_model(text, n):
    tokenized_text = tokenize_text(text, n)
    ngrams = generate_grams(tokenized_text, n)
    model = WittenBellInterpolated(n)
    model.fit([ngrams], vocabulary_text=tokenized_text)
    return model

def get_score(model, text, n):
    data = tokenize_text(text, n)
    score = []
    for i, item in enumerate(data[n-1:]):
        s = model.score(item, data[i:i+n-1])
        score.append(s)
    return score

def get_avg_score(model, text, n):
    score = get_score(model, text, n)
    return numpy.average(score, weights=score)

