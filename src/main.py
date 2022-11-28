from flask import Flask, render_template, request, jsonify
from pprint import pprint
import pickle

from .const import CSE_ID, DEVELOPER_KEY, DEV_MODE, NGRAM_SIZE
from .cache import Cache
from .search import search, get_url_text, create_model, tokenize_text, get_avg_score

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')
cache = Cache()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/search', methods=['POST'])
def app_search():
    try:
        text = request.json['text']
        model = create_model(text, NGRAM_SIZE)
        response = search(text)
        items = list(filter(lambda item: 'fileFormat' not in item, response['items']))
        results = []
        for item in items:
            text = get_url_text(cache, **item)
            score = get_avg_score(model, text, NGRAM_SIZE)
            results.append({
                'site': item['displayLink'],
                'link': item['link'],
                'title': item['title'],
                'score': score,
            })

        return jsonify({
            'status': 200,
            'results': results,
            'response': response,
        })
    except Exception as e:
        pprint(e)
        return jsonify({
            'status': 400,
            'error': e,
        })

"""
def main():
    cache = Cache()
    model = create_model(SEARCH_TEXT, NGRAM_SIZE)
    response = search(SEARCH_TEXT)
    for item in response["items"]:
        # dict_keys(['kind', 'title', 'htmlTitle', 'link', 'displayLink', 'snippet', 'htmlSnippet', 'cacheId', 'formattedUrl', 'htmlFormattedUrl', 'pagemap'])
        text = get_url_text(cache, **item)
        score1 = get_score(model, text, NGRAM_SIZE)
        m1 = numpy.average(score1, weights=score1)
        pprint(m1)
    cache.close()

if __name__ == "__main__":
    main()
"""
