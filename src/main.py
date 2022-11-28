from flask import Flask, render_template, request, jsonify
from pprint import pprint
import asyncio
import pickle

from .const import CSE_ID, DEVELOPER_KEY, DEV_MODE, NGRAM_SIZE
#from .cache import Cache
from .search import search, get_url_text, create_model, tokenize_text, get_avg_score

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')
#cache = Cache()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/search', methods=['POST'])
def app_search():
    async def process_entry(item):
        try:
            text = get_url_text(**item)
            score = get_avg_score(model, text, NGRAM_SIZE)
            result = {
                'site': item['displayLink'],
                'link': item['link'],
                'title': item['title'],
                'score': score*100,
            }
            return result
        except:
            print('Failed to fetch data or calculate score from: ', item['link'])
            return None

    text = str(request.json['text']).strip()
    model = create_model(text, NGRAM_SIZE)
    responses = search(text)
    items = []
    batches = []
    for response in responses:
        batches.extend(list(filter(lambda item: 'fileFormat' not in item, response['items'])))

    loop = asyncio.new_event_loop()
    while len(batches) > 0:
        batch = batches[0:5]
        del batches[0:5]
        tasks = []
        for item in batch:
            tasks.append(loop.create_task(process_entry(item)))
        items.extend(loop.run_until_complete(asyncio.gather(*tasks)))
    loop.close()

    items = list(filter(lambda item: item is not None, items))

    return jsonify({
        'status': 200,
        'items': items,
    })

