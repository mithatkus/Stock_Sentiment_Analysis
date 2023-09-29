# Correcting the views.py content


from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import nltk
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
import string
import json
import os

# Initializations
lemmatizer = WordNetLemmatizer()
sia = SentimentIntensityAnalyzer()

# TODO: Define API_TOKEN or fetch from environment variables
API_TOKEN = "API_TOKEN"

def home(request):
    return render(request, 'index.html')

def sentiment_route(request):
    symbols = request.GET.get('symbol')
    if not symbols:
        return JsonResponse({"error": "Please provide a 'symbol' parameter"}, status=400)

    news = get_news(API_TOKEN, symbols)
    all_sentiment_scores = []
    
    for item in news:
        try:
            bodies = scrape_website(item["url"])
            sentiment_scores = [get_sentiment(body) for body in bodies]
            all_sentiment_scores.extend(sentiment_scores)
        except Exception as e:
            print(f"Error processing {item['url']}: {e}")

    average_sentiment = aggregate_sentiments(all_sentiment_scores)
    return JsonResponse({"average_sentiment": average_sentiment})

def get_news(api_token, symbols):
    url = f"https://api.marketaux.com/v1/news/all?symbols={symbols}&must_have_entities=true&api_token={api_token}&language=en&min_match_score=0.7"
    response = requests.get(url)
    data = json.loads(response.text)
    return data["data"]

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    bodies = [body.text for body in soup.find_all('p')]
    return bodies

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stopwords.words('english')]
    return tokens

def get_sentiment(text):
    tokens = preprocess_text(text)
    scores = sia.polarity_scores(' '.join(tokens))
    return scores

def aggregate_sentiments(sentiment_scores):
    compound_scores = [score['compound'] for score in sentiment_scores]
    return sum(compound_scores) / len(compound_scores) if sentiment_scores else 0



