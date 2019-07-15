from flask import Flask, render_template, request,redirect,url_for
from werkzeug import secure_filename
import os
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
import plotly
import plotly.graph_objs as go
import json
from collections import Counter


app = Flask(__name__)

from fbpostsapiscraper import getposts




@app.route("/")
def main():
    lim = 50
    postdat = getposts('nytimes',lim)
    posts = postdat['data']
    # print(posts)

    urls = ["https://www.facebook.com/5281959998/posts/"+p['id'].split('_')[1] for p in posts]
    texts = [p['message'] for p in posts]
    scores = [analyser.polarity_scores(sentence) for sentence in texts]
    pos = sum([score['pos'] for score in scores])
    neg = sum([score['neg'] for score in scores])
    neu = sum([score['neu'] for score in scores])

    labels = ['Positive', 'Negative', 'Neutral']
    values = [pos,neg,neu]

    layout = {
                'title': '<b>Sentiment and word cloud</b>',

    }
    graph_values = [{
                    'labels': labels,
                    'values': values,
                    'type': 'pie'}]

    layout_ts = {
                'title': '<b>Sentiment distribution in posts</b>',

    }

    '''values_ts = [score['compound'] for score in scores]
    times = [p['created_time'] for p in posts]


    trace = go.Scatter(
        x = times,
        y = values_ts
    )
 
    data = [trace]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)'''

    text = " ".join(texts)

    print(scores)

    stripped_text = []
    stripped_text = [word for word in text.split() if word.isalpha() and word.lower() not in open("stopwords.txt", "r").read() and len(word) >= 2]

    word_freqs = Counter(stripped_text)
    word_freqs = dict(word_freqs)

    word_freqs_js = []


    for key,value in word_freqs.items():
        temp = {"text": key, "size": value}
        word_freqs_js.append(temp)

    max_freq = max(word_freqs.values())


    return render_template('index.html', posts = posts, urls = urls, lim = lim, graph_values=graph_values, layout = layout,word_freqs=word_freqs_js, max_freq=max_freq)#,graphJSON=graphJSON)


if __name__ == "__main__":
    app.debug = True
    app.run()