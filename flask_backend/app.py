from flask import Flask, request
from crawler_runner import run_crawler
from indexer import create_pickled_index_from_docs
from processor import process_query
from flask import jsonify

app = Flask(__name__)

@app.route('/crawl', methods=['GET'])
def crawl():
    run_crawler()
    return 'Crawling and scraping TMZ completed.'

@app.route('/build_index', methods=['GET'])
def build_index():
    create_pickled_index_from_docs()
    return 'Index has been built.'

@app.route('/query', methods=['POST'])
def query():
    query_data = request.json
    if not query_data or 'query' not in query_data:
        return 'Please provide a query.', 400
    
    query_text = query_data['query']
    docs = process_query(query_text)
    docs_output = [{'doc_index': i+1, 'doc_content': doc} for i, doc in enumerate(docs)]
    return jsonify(docs_output)

@app.route('/stop', methods=['GET'])
def stop():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(host='0.0.0.0')

